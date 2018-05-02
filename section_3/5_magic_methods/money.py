# -*- coding: utf-8 -*-
# !/usr/bin/env python3

class Money:

    def __init__(self, amount, currency):
        assert isinstance(amount, float)
        assert amount >= 0.0
        assert isinstance(currency, str)
        self.amount = amount
        self.currency = currency

    # Comparison
    def __eq__(self, other):
        assert isinstance(other, Money)
        assert self.currency == other.currency, 'Currencies must match'
        return self.amount == other.amount

    def __lt__(self, other):
        assert isinstance(other, Money)
        assert self.currency == other.currency, 'Currencies must match'
        return self.amount < other.amount

    def __gt__(self, other):
        assert isinstance(other, Money)
        assert self.currency == other.currency, 'Currencies must match'
        return self.amount > other.amount

    # Algebraic
    def __add__(self, other):
        assert isinstance(other, Money)
        assert self.currency == other.currency, 'Currencies must match'
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        assert isinstance(other, Money)
        assert self.currency == other.currency, 'Currencies must match'
        assert other.amount <= self.amount, 'Subtracting too much'
        return Money(self.amount - other.amount, self.currency)

    # String representation
    def __str__(self):
        return '{} {}'.format(self.amount, self.currency)


class Wallet:

    def __init__(self, name):
        self.name = name
        self.items = list()

    def add(self, money):
        assert isinstance(money, Money)
        self.items.append(money)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, position):
        return self.items[position]

    def __str__(self):
        return '{}'.format(self.name)