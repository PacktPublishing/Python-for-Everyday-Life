# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib


def tree(root_path_obj):
    assert root_path_obj.is_dir()
    items = list()
    for item in root_path_obj.resolve().iterdir():
        if item.is_dir():
            items.extend(tree(item))  # recursion!
        else:
            items.append(item)
    return items


if __name__ == '__main__':
    # folder to be walked
    rel_myfolder = pathlib.Path('.') / 'myfolder'
    abs_myfolder = rel_myfolder.resolve()

    # --- WALK THE FOLDER USING ABSOLUTE PATHS ---
    print('\nWalking folder: {}'.format(abs_myfolder))
    items = tree(abs_myfolder)
    print('\n'.join([str(i) for i in items]))

    # --- FILTER ONLY TEXT FILES USING RELATIVE PATHS ---
    print('\nWalking text files in folder: {}'.format(rel_myfolder))
    for f in rel_myfolder.rglob('*.txt'):
        print(f)

    # --- FILTER ONLY FILES WHOSE NAME STARTS WITH 00 ---
    print('\nWalking files whose name starts with 00 in folder: {}'.format(rel_myfolder))
    for f in rel_myfolder.rglob('00*'):
        print(f)