# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import difflib

def unidiff_text_lines(left_lines, right_lines):
    diff_generator = difflib.unified_diff(left_lines, right_lines, lineterm='')
    diffs = list(diff_generator)
    return '\n'.join(diffs)


if __name__ == '__main__':
    import pathlib

    # read file contents
    foo_a = (pathlib.Path(__file__) / '..' / 'fileset_a' / 'foo.txt').resolve()
    with foo_a.open('r') as handle:
        content_a = handle.read()

    foo_b = (pathlib.Path(__file__) / '..' / 'fileset_b' / 'foo.txt').resolve()
    with foo_b.open('r') as handle:
        content_b = handle.read()

    # Let's check for diffs between fileset_a/foo.txt and itself
    unidiffs = unidiff_text_lines(content_a.splitlines(), content_a.splitlines())
    print('LEFT: {}, RIGHT: {}'.format('fileset_a/foo.txt', 'fileset_a/foo.txt'))
    print(unidiffs)

    # Now let's check for diffs between fileset_a/foo.txt and fileset_b/foo.txt
    unidiffs = unidiff_text_lines(content_a.splitlines(), content_b.splitlines())
    print('\nLEFT: {}, RIGHT: {}'.format('fileset_a/foo.txt', 'fileset_b/foo.txt'))
    print(unidiffs)