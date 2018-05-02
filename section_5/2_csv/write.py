# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import csv
import pathlib


if __name__ == '__main__':

    # write lists as CSV rows
    target = pathlib.Path('from_lists.csv')

    column_names = ['name', 'surname', 'country', 'email']
    row_data = [
        ['franz', 'liszt', 'HU', 'franz.liszt@gmail.com'],
        ['johann sebastian', 'bach', 'DE', 'jsbach@yahoo.de'],
        ['giuseppe', 'verdi', 'IT', 'giuseppeverdi@hotmail.com'],
        ['david', 'gilmour', 'GB', 'dgilmour@me.com']
    ]
    with open(str(target), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(column_names)
        for row in row_data:
            writer.writerow(row)

    # write dicts as CSV rows
    target = pathlib.Path('from_dicts.csv')
    dict_data = map(lambda values: dict(zip(column_names, values)),
                    row_data)
    with open(str(target), 'w') as f:
        writer = csv.DictWriter(f, fieldnames=column_names)
        writer.writeheader()
        for _dict in dict_data:
            writer.writerow(_dict)
