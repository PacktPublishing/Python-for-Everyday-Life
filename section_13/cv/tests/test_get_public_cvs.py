# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import requests
import unittest


class GetPublicCVsTestCase(unittest.TestCase):

    API_ROOT_URL = 'http://localhost:8000'
    API_TOKEN = '6913e309239a4e5a9c1f22eed1314412'

    def test_when_no_api_token_provided(self):
        resp = requests.get(self.API_ROOT_URL + '/cvs/public')
        self.assertEqual(200, resp.status_code)
        data = resp.json()
        self.assertIsNotNone(data)
        self.assertEqual(1, len(data))

    def test_when_api_token_is_provided(self):
        resp = requests.get(self.API_ROOT_URL + '/cvs/public', headers={
            'Authorization': self.API_TOKEN })
        self.assertEqual(200, resp.status_code)
        data = resp.json()
        self.assertIsNotNone(data)
        self.assertEqual(1, len(data))


if __name__ == '__main__':
    unittest.main()