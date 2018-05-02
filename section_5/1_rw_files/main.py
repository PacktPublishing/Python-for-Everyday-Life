# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib

if __name__ == '__main__':

    # --- READ A BINARY FILE ---

    source = pathlib.Path('.') / 'cat.png'
    with open(str(source.resolve()), mode='rb') as img:
        print('Reading stream {} with mode {} ...'.format(img.name, img.mode))
        byte = img.read(1)
        byte_position = img.tell()
        while byte != b'':
            print('Read byte {} at position {}'.format(byte, byte_position))
            byte = img.read(1)
            byte_position = img.tell()
        print('Done')


    # --- WRITE A BINARY FILE ---

    # create target file
    target = pathlib.Path('.') / 'output.png'
    target.touch()

    # contents for target file
    _bytes = bytearray([0x68, 0x65, 0x6c, 0x6c, 0x6f])  # ['h', 'e', 'l', 'l', 'o']

    with open(str(target.resolve()), mode='wb') as out:
        print('Writing to stream {} with mode {} ...'.format(out.name, out.mode))
        out.write(_bytes)
        print('Done')


    # ... READ BACK THE OUTPUT BIN FILE AS A TEXT FILE

    with open(str(target.resolve()), mode='r', encoding='utf-8') as binfile:
        print('Reading stream {} with mode {} ...'.format(img.name, img.mode))
        content = binfile.read()
        print('Text content read: {}'.format(content)) # we know the content is a str