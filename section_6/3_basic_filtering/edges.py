# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
from PIL import Image, ImageFilter


if __name__ == '__main__':
    # load source image
    src_img_path = (pathlib.Path('..') / 'images' / 'tiger.jpg').resolve()
    with Image.open(str(src_img_path)) as img:

        # create target file
        edges_img_path = pathlib.Path('edges.jpg')
        edges_img_path.touch()

        # extract edges and save
        edges_img = img.filter(ImageFilter.FIND_EDGES)
        edges_img.save(str(edges_img_path.resolve()))
