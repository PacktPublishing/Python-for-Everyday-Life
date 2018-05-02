# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import re
import pathlib
from fs_tools import relocate_contents_to, delete_folder, \
    rename_with_timestamp_and_place, create_folders_for_places, \
    relocate_according_to_places


'''
--- REORGANIZING PHOTOS OF MY LAST TRIP TO MEXICO --
Given this folder structure:

  images/
  |
  |__<place_1>_<epoch_1>.jpg
  |  ...
  |__<place_N>_<epoch_N>.jpg
  |
  |__images2/
    |__<place_1>_<epoch_1>.jpg
    |   ...
    |__<place_N>_<epoch_N>.jpg  

I want to:
  1. Relocate all photos into folder images/ and delete folder images2/
  2. Rename all photos with this pattern: YYYYMMDD_HHMMSS_place.jpg
  3. Create a folder for each visited place and move the corresponding photos into it
'''

if __name__ == '__main__':

    # 1. Relocate all photos into folder images/ and delete folder images2/
    src = pathlib.Path('images/images2').resolve()
    dest = pathlib.Path('images').resolve()
    relocate_contents_to(src, dest)
    delete_folder('images/images2')

    # 2. Rename all photos with this pattern: YYYY-MM-DDTHH:MM:SS_place.jpg
    folder = pathlib.Path('images').resolve()
    original_name_regex = re.compile(r'([A-z]*)[\d]?[\d]?_(\d*)\.jpg') # matches place and epoch
    rename_with_timestamp_and_place(folder, original_name_regex)


    # 3. Create a folder for each visited place and move the corresponding photos into it
    place_regex = re.compile(r'[0-9]{8}_[0-9]{6}_([A-z]*)\.jpg') # matches place
    create_folders_for_places(folder, place_regex)
    relocate_according_to_places(folder, place_regex)