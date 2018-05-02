# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from pandas import date_range
from datetime import datetime as dt


# Reference period
START_REF_PERIOD = '2017-06-01'
END_REF_PERIOD = '2018-03-01'
START_DATE = dt.strptime(START_REF_PERIOD, '%Y-%m-%d')
END_DATE = dt.strptime(END_REF_PERIOD, '%Y-%m-%d')

# Pandas TimeRange index for reference period
REF_PERIOD_INDEX = date_range(START_DATE, END_DATE)

# Crypto
ALTCOINS = [
    'XRP',  # Ripple
    'LTC',  # Litecoin
    'XMR',  # Monero
    'DASH', # Dashcoin
    'LSK',  # Lisk
    'POT',  # Potcoin
    'NXT',  # NxT
    'ETC',  # Ethereum Classic
    'XEM'   # NEM
]

COINS = [
    'BTC',  # Bitcoin
    'ETH',  # Ethereum
].extend(ALTCOINS)

EXCHANGE = 'Poloniex'

# Utilities
def count_days_in(start_date, end_date):
    return (end_date - start_date).days
