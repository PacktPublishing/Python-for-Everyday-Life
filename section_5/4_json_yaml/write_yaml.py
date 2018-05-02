# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
import yaml


if __name__ == '__main__':
    target = pathlib.Path('output.yaml')
    composers_data = [
        {'surname': 'liszt', 'country': 'HU', 'name': 'franz', 'email': 'franz.liszt@gmail.com'},
        {'surname': 'bach', 'country': 'DE', 'name': 'johann sebastian', 'email': 'jsbach@yahoo.de'},
        {'surname': 'verdi', 'country': 'IT', 'name': 'giuseppe', 'email': 'giuseppeverdi@hotmail.com'},
        {'surname': 'gilmour', 'country': 'GB', 'name': 'david', 'email': 'dgilmour@me.com'}
    ]

    target.touch()
    with open(str(target.resolve()), 'w') as f:
        print('Writing data tp YAML file')
        yaml.dump(composers_data, f,  # serialize list using YAML block style
                  default_flow_style=False)
        print('Done')
