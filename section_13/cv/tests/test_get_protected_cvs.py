# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import requests
import unittest


class GetProtectedCVsTestCase(unittest.TestCase):

    API_ROOT_URL = 'http://localhost:8000'
    API_TOKEN = '6913e309239a4e5a9c1f22eed1314412'
    USER_PK = 2

    def test_when_no_api_token_provided(self):
        resp = requests.get(self.API_ROOT_URL + '/cvs')
        self.assertEqual(401, resp.status_code)

    def test_when_invalid_api_token_is_provided(self):
        resp = requests.get(self.API_ROOT_URL + '/cvs', headers={
            'Authorization': 'too_short_string'})
        self.assertEqual(400, resp.status_code)

    def test_when_valid_api_token_is_provided_but_not_found(self):
        resp = requests.get(self.API_ROOT_URL + '/cvs', headers={
            'Authorization': '7777e309239a4e5a9c1f22eed1313333'})
        self.assertEqual(401, resp.status_code)

    def test_get_my_curriculum_list(self):
        resp = requests.get(self.API_ROOT_URL + '/cvs', headers={
            'Authorization': self.API_TOKEN })
        self.assertEqual(200, resp.status_code)
        data = resp.json()
        self.assertIsNotNone(data)
        self.assertEqual(2, len(data))

    def test_get_specific_curriculum(self):
        resp = requests.get(self.API_ROOT_URL + '/cvs/2', headers={
            'Authorization': self.API_TOKEN })
        self.assertEqual(200, resp.status_code)
        data = resp.json()
        self.assertIsNotNone(data)
        self.assertEqual(data.get('owner', None), self.USER_PK)

    def test_get_accessing_someone_elses_curriculum(self):
        resp = requests.get(self.API_ROOT_URL + '/cvs/10', headers={
            'Authorization': self.API_TOKEN })
        self.assertEqual(404, resp.status_code)

if __name__ == '__main__':
    unittest.main()