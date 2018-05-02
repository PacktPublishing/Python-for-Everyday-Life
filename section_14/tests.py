# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import unittest
import random
import json
try:
    from behaviour import understand_coin_and_conversion_currency
    from bot import app
except ImportError:
    from .behaviour import understand_coin_and_conversion_currency
    from .bot import app

class BotRequestsUnderstandingTestCase(unittest.TestCase):

    SENTENCES = [
        "bitcoin vs eur",
        "bitcoin in eur",
        "what is the price of bitcoin versus eur?",
        "what is the price of bitcoin vs eur?",
        "what is the price of bitcoin against eur?",
        "what is the price of bitcoin in eur?",
        "price of bitcoin versus eur?",
        "price of bitcoin vs eur?",
        "price of bitcoin in eur?",
        "price of bitcoin against eur?",
        "bitcoin price versus eur",
        "bitcoin price vs eur",
        "bitcoin price in eur",
        "bitcoin price against eur",
        "get bitcoin price versus eur",
        "get bitcoin price vs eur",
        "get bitcoin price in eur",
        "get bitcoin price against eur",
        "bitcoin/eur",
        "bitcoin-eur",
        "bitcoin versus eur",
        "bitcoin against eur"
    ]

    SENTENCES_COINS_ONLY = [
        "bitcoin",
        "bitcoin price",
        "price of bitcoin",
    ]

    def test_understanding_all_items(self):
        for sentence in self.SENTENCES:
            coin, curr = understand_coin_and_conversion_currency(sentence)
            self.assertEqual(coin, 'bitcoin')
            self.assertEqual(curr, 'eur')

    def test_understanding_coins_only(self):
        for sentence in self.SENTENCES_COINS_ONLY:
            coin, curr = understand_coin_and_conversion_currency(sentence)
            self.assertEqual(coin, 'bitcoin')
            self.assertIsNone(curr)

    def test_robustness_to_question_marks_and_whitespaces(self):
        sentence = "What is    the price of  bitcoin versus eur ???"
        coin, curr = understand_coin_and_conversion_currency(sentence)
        self.assertEqual(coin, 'bitcoin')
        self.assertEqual(curr, 'eur')

    def test_rubbish_input(self):
        sentence = "Where is my beer?"
        coin, curr = understand_coin_and_conversion_currency(sentence)
        self.assertIsNone(coin)
        self.assertIsNone(curr)


class BotWebResponsesTestCase(unittest.TestCase):

    VERIFY_TOKEN = 'secret'
    PAGE_ACCESS_TOKEN = '1a2b3c4d5e6f7g8h9i'
    FACEBOOK_MESSAGING_ENDPOINT = 'https://httpbin.org/post'

    @classmethod
    def setUpClass(cls):
        app.config.update(VERIFY_TOKEN=cls.VERIFY_TOKEN,
                          PAGE_ACCESS_TOKEN=cls.PAGE_ACCESS_TOKEN)

    def setUp(self):
        self.client = app.test_client()

    def test_webhook_validation_is_successful(self):
        challenge = random.getrandbits(10)
        params = {
            'hub.mode': 'subscribe',
            'hub.challenge': challenge,
            'hub.verify_token': self.VERIFY_TOKEN
        }
        resp = self.client.get('/', query_string=params)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(str(challenge), resp.data.decode('utf-8'))

    def test_webhook_validation_fails(self):
        challenge = random.getrandbits(10)
        params = {
            'hub.mode': 'subscribe',
            'hub.challenge': challenge,
            'hub.verify_token': 'blablabla'
        }
        resp = self.client.get('/', query_string=params)
        self.assertEqual(403, resp.status_code)

    def test_webhook_validation_without_data(self):
        resp = self.client.get('/')
        self.assertEqual(200, resp.status_code)
        self.assertEqual("Hello, I am a bot!", resp.data.decode('utf-8'))

    def test_webhook_upon_non_page_events(self):
        data = dict(object="other")
        resp = self.client.post('/',
                                data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(200, resp.status_code)
        self.assertEqual("OK", resp.data.decode('utf-8'))

    def test_webhook_responds(self):
        data = {
          "object":"page",
          "entry":[
            {
                "id": "123456",
                "time": 123456789,
                "messaging":[
                    {
                        "sender":{
                            "id": "4395279582735"
                        },
                        "recipient":{
                            "id": "23208257235"
                        },
                        "timestamp": 123456700,
                        "message":{
                            "mid": "$mid.a23034g034g834g",
                            "seq": 45654,
                            "text": "Bitcoin price"
                        }
                    }]
            }]
        }
        resp = self.client.post('/',
                                data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(200, resp.status_code)
