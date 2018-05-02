# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import imaplib
import email
from section_9.accounts import GMAIL


def extract_text_payload(email_msg):
    main_type = email_msg.get_content_maintype()
    # some emails only have one data format type for their body...
    if main_type == 'text':
        # Gmail sends Base64 encoded email payloads: need to decode them
        return email_msg.get_payload(decode=True)
    # ...others have multiple bodies, each with a different data format type
    elif main_type == 'multipart':
        for part in email_msg.get_payload():  # find a text part in the body
            if part.get_content_maintype() == 'text':
                return part.get_payload(decode=True)
    else:
        raise ValueError('Email does not contain a text body')



if __name__ == '__main__':

    GMAIL_IMAP_SERVER = 'imap.gmail.com'

    # create a stateful IMAP-based Gmail API proxy object
    mail = imaplib.IMAP4_SSL(GMAIL_IMAP_SERVER)
    mail.login(GMAIL.get('address', None),
               GMAIL.get('password', None))

    # retrieve the list of mailboxes
    mailboxes = mail.list()
    print('Server contains {} mailboxes\n'.format(len(mailboxes)))

    # now select the mailbox called "inbox"
    result, inbox = mail.select("inbox")
    print('Inbox contains: {} messages\n'.format(int(inbox[0])))

    # search and return email UIDs
    result, raw_emails_ids = mail.uid('search', None, "ALL")
    emails_uids = raw_emails_ids[0].split()

    # retrieve email contents
    for uid in emails_uids:
        print('\n*** Email - UID: {}'.format(uid.decode("utf-8")))

        # fetch the raw email object and parse it
        result, data = mail.uid('fetch', uid, '(RFC822)')
        raw_email_object = data[0][1]  # IMAP gives lots of metadata!
        email_msg = email.message_from_bytes(raw_email_object)
        try:
            text_content = extract_text_payload(email_msg)
            print('Sent by: {}'.format(email_msg['From']))
            print('Sent to: {}'.format(email_msg['To']))
            print('Subject: {}'.format(email_msg['subject']))
            print('Body: {}'.format(text_content))
        except ValueError:
            continue
