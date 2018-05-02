# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import PyPDF2
import pathlib

# --- ROTATE CONTENTS OF A PDF FILE AND SAVE TO ANOTHER ---

def rotate_clockwise(src_pdf_path, target_pdf_path, rotation_angle):

    assert isinstance(src_pdf_path, str)
    assert isinstance(target_pdf_path, str)
    assert isinstance(rotation_angle, int)
    assert rotation_angle >= 0

    with open(src_pdf_path, 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        writer = PyPDF2.PdfFileWriter()

        # we need to rotate all pages
        for index in range(reader.numPages):
            page = reader.getPage(index)
            page.rotateClockwise(rotation_angle)
            writer.addPage(page)

        # saving to target file
        with open(target_pdf_path, 'wb') as g:
            writer.write(g)


if __name__ == '__main__':
    src = pathlib.Path('composers.pdf').resolve()
    target = pathlib.Path('output_rotated.pdf')
    target.touch()
    rotate_clockwise(str(src), str(target.resolve()), 180)
