# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
import yaml


if __name__ == '__main__':
    src = pathlib.Path('composers.yaml').resolve()
    with open(str(src), 'r') as f:
        composers = yaml.load(f)
        print('Read data from YAML file')
    for composer in composers:
        print('Found composer: {}'.format(composer))
