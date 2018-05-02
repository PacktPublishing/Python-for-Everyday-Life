# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import zipfile


# --- UNZIPPING FILES AND FOLDERS ---

def unzip(source_archive_path, target_path):
    """
    Unzips a zip archive.
    :param source_archive_path: str path of source zip archive
    :param target_path: str path of target folder where decomprssed data will be put
    :return: None
    """
    assert zipfile.is_zipfile(source_archive_path), 'Not a valid ZIP archive'
    print('Decompressing archive {} into {}'.format(source_archive_path, target_path))
    with zipfile.ZipFile(source_archive_path) as zf:
        zf.extractall(target_path)
    print('Done')



if __name__ == '__main__':
    import pathlib

    src_zip = src_file = (pathlib.Path('.') / 'testarchive.zip').resolve()

    # unzip
    unzip(str(src_zip), '.')
