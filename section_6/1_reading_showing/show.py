# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
from PIL import Image


if __name__ == '__main__':

    img_path = (pathlib.Path('..') / 'images' / 'tiger.jpg').resolve()

    # image load
    with Image.open(str(img_path)) as img:
        # image info
        print('IMAGE: {}'.format(str(img_path)))
        print('Image is in {} format'.format(img.format))
        print('Image size: width {} pixels, height {} pixels'.format(img.size[0], img.size[1]))
        print('Image color bands: {}'.format(img.mode))
        # image display
        img.show()
