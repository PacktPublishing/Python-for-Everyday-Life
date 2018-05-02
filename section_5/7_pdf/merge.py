# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
import PyPDF2

# --- MERGE TWO PDF FILES ---


def merge(source_pdf_paths, target_pdf_path):
    merger = PyPDF2.PdfFileMerger()

    # append PDF source files to merger
    for pdf_path in source_pdf_paths:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            merger.append(reader)

    # write to output file
    with open(target_pdf_path, 'wb') as g:
        merger.write(g)


if __name__ == '__main__':
    sources = [str(pathlib.Path('composers.pdf').resolve()),
               str(pathlib.Path('onepager.pdf').resolve())]
    target = pathlib.Path('output_merged.pdf')
    target.touch()

    merge(sources, str(target.resolve()))
