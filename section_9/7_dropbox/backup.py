# coding: utf-8 -*-
# !/usr/bin/env python3

import dropbox
import pathlib
from section_9.accounts import DROPBOX


def tree(root_path_obj):
    assert root_path_obj.is_dir()
    items = list()
    for item in root_path_obj.iterdir():
        if item.is_dir():
            items.extend(tree(item))  # recursion!
        else:
            items.append(item)
    return items


def backup_with_overwriting(dropbox, local_dir_path_obj, target_dropbox_dir):

    print('Backing up contents of local folder: {} to Dropbox folder {} ...\n'.format(
        local_dir_path_obj, target_dropbox_dir))

    print('Data will be overwritten\n')

    # Walk the local folder
    for path_obj in tree(local_dir_path_obj):
        if path_obj.is_file():
            # target paths on Dropbox must start with a "/"
            destination_path = '/' + target_dropbox_dir + '/' + str(path_obj)
            try:
                with path_obj.open('rb') as f:
                    print('UPLOAD: {} --> {}'.format(path_obj, destination_path))
                    dbx.files_upload(f.read(),
                                     destination_path,
                                     mode=dropbox.files.WriteMode.overwrite,
                                     mute=True)
            except Exception as e:
                print('Failed to upload {}, reason: {}\n'.format(path_obj, e))
                continue
    print('\nDone')

if __name__ == '__main__':

    # We want to implement a 1-way backup of folder "user_data" into a Dropbox
    # folder "backup_user_data" that will be placed in the root Dropbox space.
    # We also want Dropbox files to be overwritten with further modifications
    # coming from the local copies

    # Declare the paths
    local_dir = pathlib.Path('user_data')
    target_dropbox_dir = 'backup_user_data'

    # Instantiate the Dropbox local API proxy
    dbx = dropbox.Dropbox(DROPBOX.get('access_token', None))

    # Backup
    backup_with_overwriting(dropbox, local_dir, target_dropbox_dir)

