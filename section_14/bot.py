# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import os
import sys
import json
import logging
import requests
from flask import Flask, request
try:
    from behaviour import answer
except ImportError:
    from .behaviour import answer


app = Flask(__name__)

# setup logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

# store env variables value into app's config
app.config.update(VERIFY_TOKEN=os.getenv("VERIFY_TOKEN", None),
                  PAGE_ACCESS_TOKEN=os.getenv("PAGE_ACCESS_TOKEN", None),
                  FACEBOOK_MESSAGING_ENDPOINT="https://graph.facebook.com/v2.6/me/messages")


@app.route('/', methods=['GET'])
def webhook_verification():
    """
    This endpoint is invoked by Facebook as a test for the bot connectivity
    via webhooks. Requests by Facebook are in the form:

        GET /?hub.mode=subscribe&hub.challenge=1287013785&hub.verify_token=$VERIFY_TOKEN

    Notice that "hub.verify_token" contains the value for the VERIFY_TOKEN that
    Facebook and the bot should share. The bot should verify that token in order
    to authenticate Facebook as the appropriate caller.

    Whenever the webhook validation si OK, Facebook expects responses with:
      - status code: 200
      - payload: only containing the "hub.challenge" request query parameter value
        echoed back

    :return: HTTP 200 when verification is OK, 403 otherwise
    """
    if request.args.get("hub.mode", None) == "subscribe":
        if request.args.get("hub.challenge", None):
            if not request.args.get("hub.verify_token") == app.config['VERIFY_TOKEN']:
                # VERIFY_TOKEN does not match
                app.logger.warning('Webhook verification failed: {}'.format(str(request.args)))
                return "Unauthorized: VERIFY TOKEN is not matching", 403
            # webhook verification OK
            app.logger.info('Webhook verification successful: {}'.format(str(request.args)))
            return request.args["hub.challenge"], 200
    else:
        # in case it was a simple GET
        return "Hello, I am a bot!", 200


@app.route('/', methods=['POST'])
def webhook():
    """
    Facebook posts data to this endpoint whenever events that the bot subscribed
    (eg. page events, such as chat messages) occur.
    Event data has the following JSON format:

        {
          "object":"page",
          "entry":[   # each "entry" item is a page event
            {
                "id": <PAGE_ID>,
                "time": <TIMESTAMP>,
                "messaging":[   # each "messaging" item is a messaging event
                    {
                        "sender":{
                            "id": <PSID>
                        },
                        "recipient":{
                            "id": <PAGE_ID>
                        },
                        "timestamp": <TIMESTAMP>,
                        "message":{  # this is the actual text message
                            "mid": <MID>,
                            "seq": <SEQUENCE>,
                            "text": <MESSAGE_TEXT>
                        }
                    },
                    ...
                ]
            },
            ...
          ]
        }

    Facebook expects an HTTP 200 to be always returned

    :return: HTTP 200
    """

    # this list will queue the messages awaiting for response
    awaiting_messages = list()

    # extract messages from request data
    data = request.get_json()

    # if it was not a page event, quit
    if data["object"] != "page":
        return "OK", 200

    # iterate over page events
    for entry in data["entry"]:
        for message in entry["messaging"]:
            # check if there is a text message
            if message.get("message"):
                # Facebook ID of the user that sent the message
                sender_id = message["sender"]["id"]
                # Text of the message
                text = message["message"]["text"]
                app.logger.info('Received message from sender: {} with text: {}'.format(
                    sender_id, text))
                awaiting_messages.append((sender_id, text))

    # answer the questions
    for sender_id, text in awaiting_messages:
        response_str = answer(text)
        app.logger.info("Replying to sender: {} with text: {}".format(
            sender_id, response_str))
        reply(sender_id, response_str)

    return "OK", 200  # must always return 200


def reply(recipient_id, response_text):
    """
    This function understands the original user's question by invoking the bot
    algorithms and then POSTs back the answer to the Facebook messaging endpoint

    Our Facebook Page is registered as an app on Facebook: as this app is the
    actually the entity that replies to the user, Facebook expects that we
    send along a query parameter called "access_token" containing the
    PAGE_ACCESS_TOKEN value: this allows Facebook to authenticate the app.

    Also, Facebook expects POST data to be in JSON, with proper Content-Type
    and obeying the following format:

        {
            "recipient": {
                "id": <RECIPIENT_ID>
            },
            "message": {
                "text": <MESSAGE_TEXT>
            }
        }

    """
    params = {
        "access_token": app.config['PAGE_ACCESS_TOKEN']
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps(
        {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": response_text
            }
        }
    )
    r = requests.post(app.config['FACEBOOK_MESSAGING_ENDPOINT'],
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        app.logger.error('Error in sending response - status: {}, reason: {}'.format(
            r.status_code, r.text))


if __name__ == '__main__':
    app.run(debug=True)
