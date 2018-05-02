# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
import requests


def download(url, target_file_path):
    assert isinstance(url, str)
    assert isinstance(target_file_path, str)

    # if target file does not exist, create it
    target_file = pathlib.Path(target_file_path)
    if not target_file.exists():
        target_file.touch()

    # HTTP GET request
    print('Downloading: {} --> {}'.format(url, target_file.resolve()))
    response = requests.get(url)

    # check if everything went fine with the request
    response.raise_for_status()

    # write response payload data to target file
    with target_file.resolve().open('wb') as f:
        f.write(response.content)
    print('Done.\n')



if __name__ == '__main__':
    # some stuff to download
    google_home_url = 'http://www.google.com'  # a web page
    mnist_ds_url = 'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz'  # big file

    # download it
    download(google_home_url, 'google.html')
    download(mnist_ds_url, '../mnist.gz')


