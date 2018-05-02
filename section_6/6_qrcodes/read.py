# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
import zbarlight
from PIL import Image

def parse_to_dict(qr_raw_str):
    result = dict()
    entries = qr_raw_str.split('\n')[2:-1]
    for entry in entries:
        if entry.startswith('N'):
            result['name'] = entry.split(':')[1]
            continue
        if entry.startswith('EMAIL'):
            result['email'] = entry.split(':')[1]
            continue
        if entry.startswith('URL'):
            result['website'] = entry.split('URL:')[1]
            continue
        if entry.startswith('ADR'):
            tokens = entry.split(':')[1].split(';')
            address = dict()
            address['first_line'] = tokens[0]
            address['second_line'] = tokens[1]
            address['city'] = tokens[2]
            address['country'] = tokens[3]
            result['address'] = address
            continue
    return result


if __name__ == '__main__':
    # load source image
    qr_path = (pathlib.Path('..') / 'images' / 'qrcode.png').resolve()
    with Image.open(str(qr_path)) as img:
        # get data from QR
        qr_raw_bytes_list = zbarlight.scan_codes('qrcode', img)
        qr_raw_string = qr_raw_bytes_list[0].decode("utf-8")
        print('QR code raw content:\n{}\n'.format(qr_raw_string))

        # parse raw info into a dict
        qr_info_dict = parse_to_dict(qr_raw_string)
        print('QR parsed info:\n{}'.format(qr_info_dict))