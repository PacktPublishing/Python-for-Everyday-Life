# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import requests
from bs4 import BeautifulSoup


# Docs about the API can be found at: GET https://httpbin.org

if __name__ == '__main__':

    # --- TESTING HTTP METHODS ---

    # GET call: GET https://httpbin.org/ip
    res = requests.get('https://httpbin.org/ip')
    print('\nTested GET method - response: {}, content: {}'.format(
        res.status_code, res.json()))

    # POST call: POST https://httpbin.org/post
    post_data = dict(a=1, b=2)
    res = requests.post('https://httpbin.org/post', data=post_data)
    print('\nTested POST method - response: {}, posted data: {}'.format(
        res.status_code, res.json().get('form', dict())))

    # PUT call: PUT https://httpbin.org/put
    put_data = dict(n=123)
    res = requests.put('https://httpbin.org/put', data=put_data)
    print('\nTested PUT method - response: {}, put data: {}'.format(
        res.status_code, res.json().get('form', dict())))

    # DELETE call: DELETE https://httpbin.org/delete
    res = requests.delete('https://httpbin.org/delete')
    print('\nTested DELETE method - response: {}'.format(res.status_code))


    # --- TESTING HEADERS ---

    # Request headers reflection and response headers: GET https://httpbin.org/headers
    headers = {
        'X-Custom-Header': 'foo',
        'X-Very-Custom-Header': 'bar'
    }
    res = requests.get('https://httpbin.org/headers', headers=headers)
    print('\nTested GET method - response: {},\nrequest headers: {},\n'
          'response headers: {}'.format(res.status_code,
                                        res.json().get('headers', dict()),
                                        res.headers))


    # --- TESTING STATUS CODES ---

    # 200 OK: GET https://httpbin.org/status/200
    res = requests.get('https://httpbin.org/status/200')
    print('\nTested status code 200 OK - received: {},'.format(res.status_code))

    # 404 Not Found: GET https://httpbin.org/status/404
    res = requests.get('https://httpbin.org/status/404')
    print('\nTested status code 404 Not Found - received: {},'.format(
        res.status_code))

    # 500 Internal Server Error: GET https://httpbin.org/status/500
    res = requests.get('https://httpbin.org/status/500')
    print('\nTested status code 500 Internal Server - received: {},'.format(
        res.status_code))


    # --- TESTING RESPONSE MEDIA-TYPES ---

    # HTML: GET https://httpbin.org/xml
    res = requests.get('https://httpbin.org/html')
    html = BeautifulSoup(res.content, 'html.parser')
    print('\nTested HTML response media type - response: {},\n'
          'Content media-type: {}\n'
          'Number of paragraphs in the HTML: {}'.format(
                res.status_code,
                res.headers.get('Content-Type', None),
                len(html.find_all('p'))))

    # XML: GET https://httpbin.org/xml
    res = requests.get('https://httpbin.org/xml')
    xml = BeautifulSoup(res.content, 'xml')
    print('\nTested XML response media type - response: {},\n'
          'Content media-type: {}\n'
          'XML elements of type "slide": {}'.format(
                res.status_code,
                res.headers.get('Content-Type', None),
                len(xml.find_all('slide'))))