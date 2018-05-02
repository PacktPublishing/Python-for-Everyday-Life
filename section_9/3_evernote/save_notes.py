# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import hashlib
from evernote.edam.error.ttypes import EDAMUserException
from evernote.edam.type.ttypes import Note, Data, Resource
from evernote.api.client import EvernoteClient
from section_9.accounts import EVERNOTE


# --- ENML utilities ---

def enml_for_text_note(text):
    enml = '<?xml version="1.0" encoding="UTF-8"?>'
    enml += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    enml += '<en-note>{}</en-note>'.format(text)
    return enml


def enml_for_note_with_attachments(text, attachments):
    assert attachments
    enml = '<?xml version="1.0" encoding="UTF-8"?>'
    enml += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    enml += '<en-note>{}'.format(text)
    enml += '<br /><br />'
    for attachment in attachments:
        enml += 'Attachment with hash {}: <br />' \
                '<en-media type="{}" hash="{}" /><br />'.format(
                    attachment.data.bodyHash,
                    attachment.mime,
            attachment.data.bodyHash)
    enml += '</en-note>'
    return enml


# --- Note creation wrapper functions ---


def create_note(note_store, title, content):
    # Content of each Evernote note must be in a XML-derived format called ENML
    enml_content = enml_for_text_note(content)

    # Create and post a new note object
    note = Note()
    note.title = title
    note.content = enml_content
    created_note = None
    try:
        created_note = note_store.createNote(note)
    except EDAMUserException as e:
        print('Wrong ENML body: {}'.format(e))
    finally:
        return created_note


def create_note_with_image(note_store, title, content, image_path):
    # To include an attachment such as an image in a note, first create a Resource
    # for the attachment. The Resource must contain the binary attachment
    # data, an MD5 hash of such data, and the attachment MIME type.

    # read image data
    with open(image_path, 'rb') as f:
        img = f.read()

    # create image data hash
    md5 = hashlib.md5()
    md5.update(img)
    h = md5.hexdigest()

    # now create an Evernote's Data object...
    data = Data()
    data.size = len(img)
    data.bodyHash = h
    data.body = img

    # ...that gets packed into a Resource object
    img_resource = Resource()
    img_resource.mime = 'image/png'
    img_resource.data = data

    # Now, create ENML content for the note
    enml_content = enml_for_note_with_attachments(content, [img_resource])

    # Create and post a new note object
    note = Note()
    note.title = title
    note.content = enml_content
    note.resources = [img_resource]  # don't forget to attach resources!

    created_note = None
    try:
        created_note = note_store.createNote(note)
    except EDAMUserException as e:
        print('Wrong ENML body: {}'.format(e))
    finally:
        return created_note


if __name__ == '__main__':

    # Instantiate the Evernote Sandbox API local proxy
    token = EVERNOTE.get('developer_token', None)
    client = EvernoteClient(token=token,
                            sandbox=True)

    # Use a NoteStore object to create, update and delete notes
    note_store = client.get_note_store()

    # Create a text-only note
    print('Creating a text-only note...')
    text_note = create_note(note_store,
                            'Hello from Python',
                            'Python for Everyday life')
    print('Created text-only note: GUID={}\n'.format(
        getattr(text_note, 'guid', 'None')))

    # Create a note with an image attached
    print('Creating a note with attached image...')
    note_with_image = create_note_with_image(note_store,
                                             'Picture!',
                                             'This note contains an image also',
                                             'img.png')
    print('Created text-only note: GUID={}\n'.format(
        getattr(note_with_image, 'guid', 'None')))