# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import PyPDF2
import pathlib


if __name__ == '__main__':
    src = pathlib.Path('composers.pdf').resolve()
    with open(str(src), 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        print('This PDF has {} pages'.format(reader.numPages))
        page = reader.getPage(0)

        # Extract text - it's not going to be perfect
        raw_text = page.extractText()
        text = raw_text.replace('\n\n', '\n')
        print('Extracted text:\n{}'.format(text))