# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import shutil
from _datetime import datetime as dt


def relocate_contents_to(source_folder, destination_folder):
    print('\nRELOCATING FILES TO MAIN IMAGES FOLDER')
    assert source_folder.is_dir()
    assert destination_folder.is_dir()

    # walk the folder
    for file in source_folder.iterdir():
        if not file.is_file():
            continue
        # move file
        destination_file = destination_folder.resolve() / file.name
        shutil.move(str(file.resolve()), str(destination_file))

    print('Successfully moved {} contents to {}'.format(source_folder,
                                                        destination_folder))

def delete_folder(folder_path):
    print('\nDELETING EMPTY SUBFOLDER')
    shutil.rmtree(folder_path)
    print('Folder {} has been successfully deleted'.format(folder_path))


def epoch_to_formatted_string(epoch, string_format):
    assert isinstance(epoch, int)
    return dt.utcfromtimestamp(epoch).strftime(string_format)


def rename_with_timestamp_and_place(folder_path_obj, original_name_regex):
    assert folder_path_obj.is_dir()

    # walk the folder
    print('\nRENAMING FILES BASED ON TIMESTAMPS AND PLACES')
    for file in folder_path_obj.iterdir():

        if not file.is_file():
            continue

        # match photo's epoch and place from its name
        matches = original_name_regex.search(str(file))
        if matches is None:
            print('Impossible to find place and time for file {}: skipping'.format(file))
            continue
        place, epoch = matches.group(1), matches.group(2)

        # turn epoch into a human-readable format
        timestamp = epoch_to_formatted_string(int(epoch), '%Y%m%d_%H%M%S')

        # build the new filename
        renamed_file_name = '{}_{}.jpg'.format(timestamp, place)
        renamed_file = file.parent.resolve() / renamed_file_name

        # rename the file
        shutil.move(str(file.resolve()), str(renamed_file))
        print('Renamed {} --> {}'.format(file, renamed_file))


def create_folders_for_places(folder_path_obj, place_regex):
    assert folder_path_obj.is_dir()

    # walk the folder
    print('\nCREATING SUBFOLDERS BASED ON PLACES')
    for file in folder_path_obj.iterdir():

        if not file.is_file():
            continue

        # match photo's place from its name
        matches = place_regex.search(str(file))
        if matches is None:
            print('Impossible to read place from name of file {}: skipping'.format(file))
            continue
        place = matches.group(1)

        # create a subfolder for the place, if it is not in place yet
        new_subfolder = folder_path_obj.resolve() / place
        try:
            new_subfolder.mkdir()
            print('Created new folder {}'.format(new_subfolder))
        except FileExistsError:
            print('Folder {} already exist - will not create it'.format(new_subfolder))


def relocate_according_to_places(folder_path_obj, place_regex):
    assert folder_path_obj.is_dir()

    # walk the folder
    print('\nRELOCATING FILES TO SUBFOLDERS BASED ON PLACES')
    for file in folder_path_obj.iterdir():

        if not file.is_file():
            continue

        # match photo's place from its name
        matches = place_regex.search(str(file))
        if matches is None:
            print('Impossible to read place from name of file {}: skipping'.format(file))
            continue
        place = matches.group(1)

        # derive target subfolder and move file
        target_subfolder = folder_path_obj / place
        if target_subfolder.exists():
            target_file = target_subfolder.resolve() / file.name
            shutil.move(str(file.resolve()), str(target_file))
            print('Relocated {} --> {}'.format(file, target_file))
        else:
            print('Target subfolder {} does not exist: '
                  'skipping relocation'.format(target_subfolder))