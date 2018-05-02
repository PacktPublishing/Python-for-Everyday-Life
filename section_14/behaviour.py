# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import requests
import re

API_QUERY_URL = 'https://api.coinmarketcap.com/v1/ticker/{}/?convert={}'

REGEXES = [
    re.compile(r'([a-z]+)\sprice\svs\s([a-z]+).*'),        # ... coin price vs currency ...
    re.compile(r'([a-z]+)\sprice\sin\s([a-z]+).*'),        # ... coin price in currency ...
    re.compile(r'([a-z]+)\sprice\sversus\s([a-z]+).*'),    # ... coin price versus currency ...
    re.compile(r'([a-z]+)\sprice\sagainst\s([a-z]+).*'),    # ... coin price against currency ...
    re.compile(r'price\sof\s([a-z]+)\svs\s([a-z]+).*'),     # ... price of coin vs currency ...
    re.compile(r'price\sof\s([a-z]+)\sversus\s([a-z]+).*'), # ... price of coin versus currency ...
    re.compile(r'price\sof\s([a-z]+)\sin\s([a-z]+).*')  ,    # ... price of coin in currency ...
    re.compile(r'price\sof\s([a-z]+)\sagainst\s([a-z]+).*')      # ... price of coin against currency ...
]

FULL_STRING_REGEXES = [
    re.compile(r'^([a-z]+)$'),                   # coin
    re.compile(r'^([a-z]+)\sprice$'),            # coin price
    re.compile(r'^price of ([a-z]+)$'),          # price of coin
    re.compile(r'^([a-z]+)/([a-z]+)$'),          # coin/currency
    re.compile(r'^([a-z]+)-([a-z]+)$'),          # coin-currency
    re.compile(r'^([a-z]+)\sin\s([a-z]+)$'),     # coin in currency
    re.compile(r'^([a-z]+)\svs\s([a-z]+)$'),     # coin vs currency
    re.compile(r'^([a-z]+)\sversus\s([a-z]+)$'), # coin versus currency
    re.compile(r'^([a-z]+)\sagainst\s([a-z]+)$'), # coin against currency
]

KNOWN_CONVERSION_CURRENCIES = [
    "aud",
    "brl",
    "cad",
    "chf",
    "clp",
    "cny",
    "czk",
    "dkk",
    "eur",
    "gbp",
    "hkd",
    "huf",
    "idr",
    "ils",
    "inr",
    "jpy",
    "krw",
    "mxn",
    "myr",
    "nok",
    "nzd",
    "php",
    "pkr",
    "pln",
    "rub",
    "sek",
    "sgd",
    "thb",
    "try",
    "twd",
    "usd",
    "zar"
]

def understand_coin_and_conversion_currency(message_text):
    """
    Extracts from the input message the requested coin name and the symbol of
    the fiat currency in which the user wants price data to be expressed.
    The request can be expected in one of the following formats:
        - coin
        - what is the price of coin ?
        - price of coin ?
        - coin price
        - get coin price
        - coin/currency
        - coin-currency
        - coin versus currency
        - coin vs currency
        - coin against currency
        - coin in currency
        - what is the price of coin versus currency?
        - what is the price of coin vs currency?
        - what is the price of coin against currency?
        - what is the price of coin in currency?
        - price of coin versus currency?
        - price of coin vs currency?
        - price of coin against currency?
        - price of coin in currency?
        - coin price versus currency
        - coin price vs currency
        - coin price against currency
        - coin price in currency
        - get coin price versus currency
        - get coin price vs currency
        - get coin price against currency
        - get coin price in currency
    :param message_text: str
    :return: (coin_name, conversion_currency), both being either str or None
    """
    # clean input string (remove leading/trailing/repeated whitespaces and question marks
    message_text = message_text.lstrip().rstrip().replace("?", "")
    message_text = ' '.join(message_text.split())
    message_text = message_text.lower()

    # try to match a regex
    coin_name = None
    conversion_currency = None
    for r in REGEXES:
        matches = r.search(message_text)
        if matches is not None:
            g1 = matches.group(1)
            g2 = matches.group(2)
            if g1 is not None:
                coin_name = g1
            if g2 is not None:
                conversion_currency = g2
            if g1 is not None and g2 is not None:  # when we have them both
                return coin_name, conversion_currency

    for r in FULL_STRING_REGEXES:
        matches = r.search(message_text)
        if matches is not None:
            g1 = matches.group(1)
            try:
                g2 = matches.group(2)
            except IndexError:
                g2 = None
            if g1 is not None:
                coin_name = g1
            if g2 is not None:
                conversion_currency = g2
            if g1 is not None and g2 is not None:  # when we have them both
                return coin_name, conversion_currency

    return coin_name, conversion_currency  # we've tried our best! bye!

def is_conversion_currency_supported(conversion_currency):
    """
    Tells whether the provided fiat currency is supported or not
    :param conversion_currency: str
    :return: bool
    """
    return conversion_currency.lower() in KNOWN_CONVERSION_CURRENCIES

def fetch_cryptocurrency_data(coin_name, conversion_currency):
    """
    Fetches data about the specified coin from the Coinmarketcap API.
    :param coin_name: str
    :param conversion_currency: str
    :raises: IOError on 4xx and 5xx responses fromt he API
    :return: tuple (str, str): coin price vs the specified conversion currency
    and price percent change in the last 24 hours
    """
    assert coin_name is not None
    assert conversion_currency is not None
    url = API_QUERY_URL.format(coin_name, conversion_currency)
    price_key = 'price_{}'.format(conversion_currency.lower())
    response = requests.get(url)
    if response.status_code == 404:
        raise ValueError()
    if response.status_code != requests.codes.ok:
        raise IOError()
    coin = response.json()[0]
    price = coin.get(price_key, None)
    percent_change_24h = coin.get('percent_change_24h', None)
    return price, percent_change_24h

def answer(message_text):
    """
    Takes a message in natural language and tries to answer
    :param message_text: str
    :return: str
    """
    coin_name, conversion_currency = understand_coin_and_conversion_currency(message_text)

    # was unable to understand coin name
    if coin_name is None:
        return "Sorry I don't know that crypto. Can you specify it by full name?"

    # check if conversion currency is supported
    if conversion_currency is None:
        conversion_currency = 'usd'
    else:
        if not is_conversion_currency_supported(conversion_currency):
            return "I don't understand your own currency. Can you specify it by symbol?"

    # fetch data
    try:
        price, percent_change_24h = fetch_cryptocurrency_data(coin_name, conversion_currency)
    except ValueError:
        return "Sorry looks like your crypto does not exist. Did you type it correctly?"
    except IOError:
        return "Sorry my source of crypto prices is unavailable at the moment. Please try again in a while"

    # prepare answer about price
    if price is None:
        return "Sorry I was unable to find the price. Please try again in a while"
    else:
        answer_text = 'Current price for {} is {} {}'.format(
            coin_name.title(),
            price,
            conversion_currency.upper()
        )

    # add percent change info
    if percent_change_24h is not None:
        change = float(percent_change_24h)
        if change < 0.0:
            answer_text += ', with a loss of {}% in the last 24 hours'.format(abs(change))
        elif change > 0.0:
            answer_text += ', with a gain of {}% in the last 24 hours'.format(change)
        else:
            answer_text += ', unchanged in the last 24 hours'

    return answer_text
