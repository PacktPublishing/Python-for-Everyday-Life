# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import requests
import unittest


class ManipulateRelatedResourcesTestCase(unittest.TestCase):

    API_ROOT_URL = 'http://localhost:8000'
    API_TOKEN = '6913e309239a4e5a9c1f22eed1314412'
    USER_PK = 2

    def test_create_and_manipulate_a_skill(self):
        # create a new SKill (POST)
        skill_data = dict(name='swimming', level=2)
        resp = requests.post(self.API_ROOT_URL + '/cvs/2/skills',
            headers={'Authorization': self.API_TOKEN,
                     'Content-Type': 'application/json'},
            json=skill_data)
        self.assertEqual(201, resp.status_code)
        new_skill = resp.json()
        self.assertIsNotNone(new_skill)
        skill_id = new_skill.get('id', None)
        self.assertIsNotNone(skill_id)

        # read it (GET)
        resp = requests.get(self.API_ROOT_URL+ '/cvs/2/skills/' + str(skill_id),
            headers={'Authorization': self.API_TOKEN})
        self.assertEqual(200, resp.status_code)
        read_skill = resp.json()
        self.assertEqual(new_skill, read_skill)

        # check that the new skill has been bound to the parent CV (GET)
        resp = requests.get(self.API_ROOT_URL + '/cvs/2',
            headers={'Authorization': self.API_TOKEN})
        self.assertEqual(200, resp.status_code)
        cv = resp.json()
        skills_of_cv = cv.get('skills', list())
        self.assertTrue(new_skill in skills_of_cv)

        # now delete the skill (DELETE)
        resp = requests.delete(self.API_ROOT_URL + '/cvs/2/skills/' + str(skill_id),
            headers={'Authorization': self.API_TOKEN})
        self.assertEqual(204, resp.status_code)

        # check again and this time the skill must not be in the parent CV (GET)
        resp = requests.get(self.API_ROOT_URL + '/cvs/2',
            headers={'Authorization': self.API_TOKEN})
        self.assertEqual(200, resp.status_code)
        cv = resp.json()
        skills_of_cv = cv.get('skills', list())
        self.assertFalse(new_skill in skills_of_cv)


if __name__ == '__main__':
    unittest.main()