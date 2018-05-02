# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import requests
import unittest


class PostProtectedCVsTestCase(unittest.TestCase):

    API_ROOT_URL = 'http://localhost:8000'
    API_TOKEN = '6913e309239a4e5a9c1f22eed1314412'
    USER_PK = 2

    def test_post_new_curriculum_with_wrong_content_type(self):
        resp = requests.post(self.API_ROOT_URL + '/cvs',
            headers={'Authorization': self.API_TOKEN,
                     'Content-Type': 'text/html'},
            json={})
        self.assertEqual(415, resp.status_code)


    def test_post_new_curriculum_with_bad_data(self):
        curriculum_data = {
            'address': 'another street',
            'birth_date': 'this_is_not_a_date',
            'birth_place': 'Nowhere',
            'email': None,
            'name': None,
            'schools': [],
            'skills': [],
            'surname': 'Sparpaglione'
        }
        resp = requests.post(self.API_ROOT_URL + '/cvs',
            headers={'Authorization': self.API_TOKEN,
                     'Content-Type': 'application/json'},
            json=curriculum_data)
        self.assertEqual(400, resp.status_code)


    def test_post_new_curriculum(self):
        curriculum_data = {
            'address': 'another street',
            'birth_date': '1983-07-03',
            'birth_place': 'Nowhere',
            'email': 'claudio2@claudio.me',
            'name': 'Claudio',
            'schools': [],
            'skills': [],
            'surname': 'Sparpaglione',
            'telephone': '0211223344',
            'website': None,
            'work_experiences': []
        }
        resp = requests.post(self.API_ROOT_URL + '/cvs',
            headers={'Authorization': self.API_TOKEN,
                     'Content-Type': 'application/json'},
            json=curriculum_data)
        self.assertEqual(201, resp.status_code)
        curriculum = resp.json()
        self.assertIsNotNone(curriculum)
        self.assertIsNotNone(curriculum.get('id', None))
        self.assertEqual(curriculum.get('owner', None), self.USER_PK)

if __name__ == '__main__':
    unittest.main()