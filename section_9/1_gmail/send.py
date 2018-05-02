# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from gmail import GMail, Message
from section_9.accounts import GMAIL


if __name__ == '__main__':

    # prepare attachments
    attachments = ['attachment.pdf']

    # proxy object for the Gmail API
    gmail = GMail(username=GMAIL.get('address', None),
                  password=GMAIL.get('password', None))

    # create an email message
    msg = Message(subject='Hello from the anonymous sender',
                  sender='anonymous@email.com',
                  to=GMAIL.get('address', None),
                  # cc='somebody@email.com',
                  # text='You will never know my name.. but you got a file!',
                  html='''<h2>You will never know my name..</h2><p>but you got a file!</p>''',
                  attachments=attachments)

    # send it
    print('Sending e-mail...')
    gmail.send(msg)
    print('Done')
