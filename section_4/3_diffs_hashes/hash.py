# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import hashlib


# --- CALCULATING HASHES OF FILE CONTENTS ---

def md5(text):
    """
    Computes the MD5 hash of a text string
    """
    h = hashlib.md5()
    h.update(text.encode('utf-8'))
    return h.hexdigest()


if __name__ == '__main__':
    import pathlib
    source_file = (pathlib.Path(__file__) / '..' / 'fileset_a' / 'foo.txt').resolve()
    with source_file.open('r') as handle:
        content = handle.read()

    # Compute MD5 hash of some file content
    original_md5 = md5(content)
    print('Original content MD5 hash: {}'.format(original_md5))

    # Now let's change the contents and recompute the MD5
    content += 'yohoo'
    modified_hash = md5(content)
    print('Modified content MD5 hash: {}'.format(modified_hash))
