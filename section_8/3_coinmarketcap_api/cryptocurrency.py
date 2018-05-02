# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import requests
import pprint


# Docs about the API can be found at: https://coinmarketcap.com/api/


def get_ltc_data_from_coinmarketcap_api(conversion_currency):
    print('\n*** Querying Coinmarketcap API for Litecoin data '
          'with respect to {}'.format(conversion_currency))
    url = 'https://api.coinmarketcap.com/v1/ticker/litecoin/?convert={}'.format(
        conversion_currency)
    response = requests.get(url)
    coins = response.json()
    litecoin = coins[0]  # we only have 1 coin item returned
    ltc_vs_eur = litecoin.get('price_eur', None)
    ltc_vs_usd = litecoin.get('price_usd', None)
    ltc_vs_btc = litecoin.get('price_btc', None)

    print('Litecoin prices vs:')
    print('EUR --> {}'.format(ltc_vs_eur))
    print('USD --> {}'.format(ltc_vs_usd))
    print('BTC --> {}'.format(ltc_vs_btc))

    return litecoin


def get_cryptos_data_from_coinmarketcap_api(conversion_currency):
    print('\n*** Querying Coinmarketcap API for all cryptos data '
          'with respect to {}'.format(conversion_currency))
    url = 'https://api.coinmarketcap.com/v1/ticker/?convert={}'.format(
        conversion_currency)
    response = requests.get(url)
    coins = response.json()
    return coins



if __name__ == '__main__':

    conversion_currency = 'EUR'

    #  Retrieve LTC data and prices
    get_ltc_data_from_coinmarketcap_api(conversion_currency)

    #  Retrieve all available cryptos data and prices
    cryptos = get_cryptos_data_from_coinmarketcap_api(conversion_currency)
    pprint.pprint(cryptos)