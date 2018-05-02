# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import unittest
from section_11.site import app as website
from section_11.credentials import CREDENTIALS


class StaticWebsiteTestCase(unittest.TestCase):

    def setUp(self):
        # This is run before each test is executed
        self.client = website.test_client()  # instantiate an HTTP client

    def test_home_page_view(self):
        resp = self.client.get('/home')

        # check that we get an HTTP 200 and an HTML page
        assert resp.status_code == 200
        assert resp.mimetype == 'text/html'

        # check that the page contains the word "Welcome"
        assert 'Welcome' in resp.data.decode('utf-8')

    def test_bad_authentication(self):
        credentials = dict(username='wrong_username', password='wrong_pwd')
        resp = self.client.post('/login', data=credentials, follow_redirects=True)
        assert resp.status_code == 401

    def test_good_authentication(self):
        credentials = dict(username=CREDENTIALS.get('username', None),
                           password=CREDENTIALS.get('password', None))
        resp = self.client.post('/login', data=credentials, follow_redirects=True)

        # check that we get an HTTP 200 and an HTML page
        assert resp.status_code == 200
        assert resp.mimetype == 'text/html'

        # check that the page contains the word "secret"
        assert 'secret' in resp.data.decode('utf-8')

    def test_unauthenticated_access_to_private_page(self):
        resp = self.client.get('/private')

        # check that we are redirected (HTTP 302 along with a Location header)
        assert resp.status_code == 302
        location_header = resp.headers.get('Location', None)
        assert location_header is not None
        assert location_header.endswith('/login')


if __name__ == '__main__':
    unittest.main()