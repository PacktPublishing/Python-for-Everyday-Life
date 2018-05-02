# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
from PIL import Image


def crop(img_obj, top_left_pixel, bottom_right_pixel):
    """
    Crop an image with respect to fixed control points
    """
    left, upper = top_left_pixel
    right, lower = bottom_right_pixel
    assert all(map(lambda v: v >= 0, [left, upper, right, lower]))
    assert left <= right
    assert upper <= lower
    return img_obj.crop((left, upper, right, lower))


if __name__ == '__main__':
    # load source image
    src_img_path = (pathlib.Path('..') / 'images' / 'tiger.jpg').resolve()
    with Image.open(str(src_img_path)) as img:

        # create target file
        cropped_img_path = pathlib.Path('cropped.jpg')
        cropped_img_path.touch()

        # state crop control points
        # remember that origin of pixel coordinates is the top-left corner!
        top_left_pixel = (500, 300)
        bottom_right_pixel = (850, 450)

        # crop and save
        cropped_img = crop(img, top_left_pixel, bottom_right_pixel)
        cropped_img.save(str(cropped_img_path.resolve()))
        print('Source image has been cropped.')
