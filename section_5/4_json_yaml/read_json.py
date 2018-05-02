# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
import json


if __name__ == '__main__':
    src = pathlib.Path('composers.json').resolve()
    with open(str(src), 'r') as f:
        composers = json.load(f)
        print('Read data from JSON file')
    for composer in composers:
        print('Found composer: {}'.format(composer))
