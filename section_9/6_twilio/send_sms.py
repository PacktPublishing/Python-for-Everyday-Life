# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from twilio.rest import Client
from section_9.accounts import TWILIO


def send_sms(twilio, from_number, to_number):
    print('Sending SMS to {}...'.format(to_number))
    sms = twilio.api.account.messages.create(
            to=to_number,
            from_=from_number,
            body='Wonderful news: this text was sent by Python code!')
    print('Done')
    return sms



if __name__ == '__main__':

    # Instantiate Twilio API local proxy
    client = Client(TWILIO.get('account_sid', None),
                    TWILIO.get('auth_token', None))

    # Send the SMS
    send_sms(client,
             TWILIO.get('from_mobile', None),
             TWILIO.get('to_mobile', None))

