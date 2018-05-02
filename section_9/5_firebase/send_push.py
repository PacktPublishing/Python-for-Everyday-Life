# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from pyfcm import FCMNotification
from section_9.accounts import FIREBASE


if __name__ == '__main__':
    # instantiate Firebase Cloud Messaging API local proxy
    fcm = FCMNotification(api_key=FIREBASE.get('server_key', None))

    # Prepare title and content for the message to be pushed
    title = 'Python for Everyday Life'
    body = 'A warm welcome to all of you, friends!'

    # Push the message
    device_id = '<PUT-HERE-REGISTRATION-ID>'
    print('Sending message to device ID: {}'.format(device_id))
    result = fcm.notify_single_device(registration_id=device_id,
                                      message_title=title,
                                      message_body=body)
    # Check delivery outcome
    if result['failure'] == 1:
        for result in result['results']:
            reason = result.get('error', None)
            if reason is not None:
                print('Message delivery failed, reason: {}'.format(reason))
                break
    else:
        print('Message delivery was successful')
