# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
import json


if __name__ == '__main__':
    target = pathlib.Path('output.json')
    composers_data = [
        {'surname': 'liszt', 'country': 'HU', 'name': 'franz', 'email': 'franz.liszt@gmail.com'},
        {'surname': 'bach', 'country': 'DE', 'name': 'johann sebastian', 'email': 'jsbach@yahoo.de'},
        {'surname': 'verdi', 'country': 'IT', 'name': 'giuseppe', 'email': 'giuseppeverdi@hotmail.com'},
        {'surname': 'gilmour', 'country': 'GB', 'name': 'david', 'email': 'dgilmour@me.com'}
    ]

    target.touch()
    with open(str(target.resolve()), 'w') as f:
        print('Writing data tp JSON file')
        json.dump(composers_data, f)
        print('Done')
