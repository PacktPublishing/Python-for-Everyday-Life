# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
from lxml import etree


if __name__ == '__main__':

    target = pathlib.Path('output.xml')
    target.touch()
    composers_data = [
        {'surname': 'liszt', 'country': 'HU', 'name': 'franz', 'email': 'franz.liszt@gmail.com'},
        {'surname': 'bach', 'country': 'DE', 'name': 'johann sebastian', 'email': 'jsbach@yahoo.de'},
        {'surname': 'verdi', 'country': 'IT', 'name': 'giuseppe', 'email': 'giuseppeverdi@hotmail.com'},
        {'surname': 'gilmour', 'country': 'GB', 'name': 'david', 'email': 'dgilmour@me.com'}
    ]
    with open(str(target.resolve()), 'wb') as f:
        root = etree.Element("composers")  # the root element of the tree
        for composer in composers_data:    # add nodes for composers
            element = etree.SubElement(root, "composer")
            for key, value in composer.items():  # each node has children
                child = etree.SubElement(element, key)
                child.text = value
        et = etree.ElementTree(root)  # create element tree
        et.write(f, xml_declaration=True, encoding='utf-8', pretty_print=True)

