# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import requests
import pathlib
import pandas as pd
from pandas.io.json import json_normalize
from section_16.config import START_DATE, END_DATE, START_REF_PERIOD, \
    END_REF_PERIOD, COINS, count_days_in

"""
Run to download crypto coin data (vs USD) to CSV files from the CryptoCompare API
"""


CRYPTOCOMPARE_API_URL = 'https://min-api.cryptocompare.com/data/histoday'
LIMIT = count_days_in(START_DATE, END_DATE)


def get_json_data(from_symbol, to_symbol):
    assert from_symbol is not None
    assert to_symbol is not None
    request = requests.get(CRYPTOCOMPARE_API_URL,
                           params={'fsym': from_symbol,
                                   'tsym': to_symbol,
                                   'limit': LIMIT,  # how many days in the past?
                                   'aggregate': 1,  # data is given day-by-day
                                   'e': 'CCCAGG'}   # CryptoCompare aggregated exchange data
    )
    return request.json()


def json_data_to_dataframe(json_data):
    assert json_data is not None
    # JSON response from CryptoCompare API are in the form:
    # {
    #   "Response":  "Success",
    #   "Type": 100,
    #   "Aggregated": false,
    #   "Data": [
    #     {
    #       "time": 1520553600,
    #       "high": 13.4,
    #       "low": 12.71,
    #       "open": 13.33,
    #       "volumefrom": 40892.17,
    #       "volumeto": 532059.47,
    #       "close": 12.75
    #     },
    #     ...
    #   ]
    # }
    df = pd.io.json.json_normalize(json_data, ['Data'])

    # add a TimeRange index based on the timestamp returned by the API
    df['day'] = pd.to_datetime(df.time, unit='s')

    # drop the "time" columns and sort the other ones
    df = df[['day', 'open', 'high', 'low', 'close', 'volumefrom', 'volumeto']]
    df.set_index('day', inplace=True)

    return df


def save_price_history_for(from_symbol, to_symbol):
    json_data = get_json_data(from_symbol, to_symbol)
    df = json_data_to_dataframe(json_data)
    datasets_folder = pathlib.Path('../datasets')
    if not datasets_folder.exists():
        datasets_folder.mkdir()
    csv_file = datasets_folder / pathlib.Path('{}_{}.csv'.format(
        from_symbol, to_symbol))
    csv_file.touch()
    df.to_csv(csv_file)


def download_dataset_from_cyptocompare_api():
    print('Reference period: {} --> {}'.format(START_REF_PERIOD, END_REF_PERIOD))
    for coin in COINS:
        print('Downloading data for couple: {}-USD ...'.format(coin))
        try:
            save_price_history_for(coin, 'USD')
        except Exception as e:
            print(e)
            continue
    print('Done')

if __name__ == '__main__':
    download_dataset_from_cyptocompare_api()
