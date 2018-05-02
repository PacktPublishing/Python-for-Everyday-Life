# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
import shutil


if __name__ == '__main__':

    # --- DELETE A FILE ---
    file = pathlib.Path('.') / 'myfolder' / '001.txt'
    print('Deleting file: {}'.format(file))
    file.unlink()

    # --- DELETE A NON EMPTY FOLDER ---
    folder = pathlib.Path('.') / 'myfolder' / 'mysubfolder'
    print('Deleting folder: {}'.format(folder))

    # rmtree accepts a string, not a Path object
    # WATCH OUT: deletion cannot be reverted!
    shutil.rmtree(str(folder))
