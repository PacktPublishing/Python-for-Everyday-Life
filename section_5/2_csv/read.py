# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import csv
import pathlib


if __name__ == '__main__':
    src = pathlib.Path('composers.csv').resolve()

    # let's grab CSV lines as lists
    with open(str(src), 'r') as f:
        reader = csv.reader(f)
        column_names = next(reader) # first line contains column names
        print('Column names are: {}'.format(column_names))
        for row_number, line in enumerate(reader):
            print('This is line number {} data: {}'.format(
                row_number+1, line))

    # let's now grab CSV lines as dictionarized data
    with open(str(src), 'r') as f:
        dict_reader = csv.DictReader(f)
        for row_number, _dict in enumerate(dict_reader):
            print('This is line number {} dictionarized data: {}'.format(
                row_number+1, _dict))