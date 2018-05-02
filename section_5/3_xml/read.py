# -*- coding: utf-8 -*-
# !/usr/bin/env python3


import pathlib
from lxml import etree


if __name__ == '__main__':
    src = pathlib.Path('composers.xml').resolve()
    with open(str(src), 'rb') as f:
        tree = etree.parse(f)
        root = tree.getroot()
        for composer in root:  # 'composer' is an Element
            print('Found composer')
            children = composer.getchildren()  # children nodes are composer's data
            data = map(lambda child: (child.tag, child.text),
                       children)
            print('Data: {}'.format(dict(data)))
