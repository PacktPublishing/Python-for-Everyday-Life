# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import uuid


class Account:
    def __init__(self, currency, logger):
        self.id = uuid.uuid4()
        self.currency = currency
        self.logger = logger
        self.balance = 0.0
        self.logger.info('Created new empty account: {}'.format(self.id))

    def deposit(self, amount):
        try:
            assert isinstance(amount, float), 'Amount must be a float'
            assert amount > 0.0, 'Amount must be non-negative'
            self.balance += amount
        except AssertionError as e:
            self.logger.error('Account {}: {}'.format(
                self.id, e))

    def withdraw(self, amount):
        try:
            assert isinstance(amount, float), 'Amount must be a float'
            assert amount > 0.0, 'Amount must be non-negative'
            assert self.balance >= amount, 'Trying to withdraw too much'
            self.balance -= amount
        except AssertionError as e:
            self.logger.error('Account {}: {}'.format(
                self.id, e))