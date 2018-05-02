# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import filecmp


if __name__ == '__main__':
    import pathlib

    # -- COMPARING FILES ---

    print('COMPARING FILES')

    # Let's first compare files "fileset_a/bar.txt" with itself
    bar_a = (pathlib.Path(__file__) / '..' / 'fileset_a' / 'bar.txt').resolve()
    outcome = filecmp.cmp(str(bar_a), str(bar_a))
    print('{} == {} ? {}'.format('fileset_a/bar.txt', 'fileset_a/bar.txt', outcome))

    # Now let's compare "fileset_a/bar.txt" with "fileset_b/bar.txt"
    bar_b = (pathlib.Path(__file__) / '..' / 'fileset_b' / 'bar.txt').resolve()
    outcome = filecmp.cmp(str(bar_a), str(bar_b))
    print('{} == {} ? {}'.format('fileset_a/bar.txt', 'fileset_b/bar.txt', outcome))


    # --- COMPARING FOLDERS ---

    print('\nCOMPARING FOLDERS')

    # Let's first compare dir "fileset_a" with itself
    dir_a = (pathlib.Path(__file__) / '..' / 'fileset_a').resolve()
    dc = filecmp.dircmp(str(dir_a), str(dir_a))
    print('Comparing: fileset_a with itself')
    print(dc.report())

    # Let's now compare dir "fileset_a" with dir "fileset_b"
    dir_b = (pathlib.Path(__file__) / '..' / 'fileset_b').resolve()
    dc = filecmp.dircmp(str(dir_a), str(dir_b))
    print('\nComparing: fileset_a with fileset_b')
    print(dc.report())

    # We can also choose what info to show
    print('\nCustomizing the last comparison report')
    print('Files both in fileset_a and fileset_b: {}'.format(dc.common_files))
    print('Files differing: {}'.format(dc.diff_files))
    print('Files only existing in fileset_b: {}'.format(dc.right_only))