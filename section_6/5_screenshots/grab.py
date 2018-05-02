# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
import pyscreenshot as ImageGrab


def grab_whole_screen_to(file_path):
    img = ImageGrab.grab()
    img.save(file_path)

def grab_screen_area_to(left, upper, right, bottom, file_path):
    img = ImageGrab.grab(bbox=(left, upper, right, bottom))
    img.save(file_path)

if __name__ == '__main__':
    # grab the whole screen
    target_file_path = pathlib.Path('whole_screen.jpg')
    target_file_path.touch()
    grab_whole_screen_to(str(target_file_path.resolve()))

    # grab the a specific rectangular area of the screen
    target_file_path = pathlib.Path('screen_section.jpg')
    target_file_path.touch()
    grab_screen_area_to(100, 100, 500, 500, str(target_file_path.resolve()))