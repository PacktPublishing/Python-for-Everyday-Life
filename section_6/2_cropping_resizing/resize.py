# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
from PIL import Image
from math import floor


def resize_to(img_obj, new_height, new_width):
    """
    Resize an image to the specified dimensions
    """
    assert isinstance(new_height, int)
    assert isinstance(new_width, int)
    assert new_height > 0
    assert new_width > 0
    return img_obj.resize((new_width, new_height))

def resize_width_to_percent(img_obj, percent):
    """
    Resize the width of an image to the specified percentage of the original size
    """
    assert isinstance(percent, int)
    assert 0 < percent < 100
    new_width = percent * img_obj.width / 100.0
    new_height = img_obj.height * new_width / img_obj.width
    return img_obj.resize((floor(new_width), floor(new_height)))


if __name__ == '__main__':

    # load source image
    src_img_path = (pathlib.Path('..') / 'images' / 'tiger.jpg').resolve()
    with Image.open(str(src_img_path)) as img:

        # --- RESIZE TO FIXED SIZE --
        resized_fixed_img_path = pathlib.Path('resized_fixed.jpg')
        resized_fixed_img_path.touch()
        resized_fixed_img = resize_to(img, 256, 178)
        resized_fixed_img.save(str(resized_fixed_img_path.resolve()))
        print('Source image was w:{} h:{} and has been resized to w:{} h:{}'.format(
            img.width, img.height, resized_fixed_img.width, resized_fixed_img.height))

        # --- PROPORTIONAL RESIZE (RESIZE BY %) --
        resized_proportional_img_path = pathlib.Path('resized_proportional.jpg')
        resized_proportional_img_path.touch()
        resized_proportional_img = resize_width_to_percent(img, 20)
        resized_proportional_img.save(str(resized_proportional_img_path.resolve()))
        print('Source image was w:{} h:{} and has been resized to w:{} h:{}'.format(
            img.width, img.height, resized_proportional_img.width,
            resized_proportional_img.height))
