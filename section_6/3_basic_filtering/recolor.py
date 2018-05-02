# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
from PIL import Image


if __name__ == '__main__':
    # load source image
    src_img_path = (pathlib.Path('..') / 'images' / 'tiger.jpg').resolve()
    with Image.open(str(src_img_path)) as img:

        # create target file
        grayscale_img_path = pathlib.Path('grayscale.jpg')
        grayscale_img_path.touch()

        # Turn to grayscale and save
        grayscale_img = img.convert("L")
        grayscale_img.save(str(grayscale_img_path.resolve()))