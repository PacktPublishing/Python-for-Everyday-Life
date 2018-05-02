# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import requests
import pathlib
import pandas as pd
from io import StringIO
from section_16.config import START_REF_PERIOD, END_REF_PERIOD, REF_PERIOD_INDEX,\
    ALTCOINS, EXCHANGE


"""
Run to download crypto coin data from cryptodatadownload.com website to CSV 
files
"""

CRYPTODATADOWNLOAD_URL = 'http://www.cryptodatadownload.com/cdd/{}_{}{}_d.csv'
DATASETS_FOLDER = pathlib.Path('../datasets')


def get_csv_string(from_symbol, to_symbol):
    assert from_symbol is not None
    assert to_symbol is not None
    url = CRYPTODATADOWNLOAD_URL.format(EXCHANGE, from_symbol, to_symbol)
    r = requests.get(url)
    payload = r.text
    # discard the very first line of the CSV payload as it's not useful
    csv_string = '\n'.join(payload.split('\r\n')[1:])
    return csv_string

def csv_string_to_dataframe(csv_string):
    assert csv_string is not None

    # The CSV string has the following columns:
    #   Date,Symbol,Open,High,Low,Close,Volume From,Volume To
    df = pd.read_csv(StringIO(csv_string), parse_dates=True)

    # add a TimeRange index based on the timestamp returned by the API
    # and prepare alias columns
    df['day'] = pd.to_datetime(df.Date).dt.date
    df['open'] = df['Open']
    df['high'] = df['High']
    df['low'] = df['Low']
    df['close'] = df['Close']
    df['volumefrom'] = df['Volume From']
    df['volumeto'] = df['Volume To']

    # drop unused columns and sort the other ones
    df = df[['day', 'open', 'high', 'low', 'close', 'volumefrom', 'volumeto']]

    # set index
    df.set_index('day', inplace=True)

    # rebase on the reference period
    df = df.reindex(REF_PERIOD_INDEX)

    return df


def refer_to_usd(df_altcoin_vs_btc, df_btc_vs_usd):
    result_df = pd.DataFrame({
        'day': df_altcoin_vs_btc.index,
        'open': df_altcoin_vs_btc.open * df_btc_vs_usd.open,
        'high': df_altcoin_vs_btc.high * df_btc_vs_usd.high,
        'low': df_altcoin_vs_btc.low * df_btc_vs_usd.low,
        'close': df_altcoin_vs_btc.close * df_btc_vs_usd.close,
        'volumefrom': df_altcoin_vs_btc.volumefrom * df_btc_vs_usd.volumefrom,
        'volumeto': df_altcoin_vs_btc.volumeto * df_btc_vs_usd.volumeto
    })
    result_df.set_index('day', inplace=True)
    return result_df


def df_to_file(df, filename):
    if not DATASETS_FOLDER.exists():
        DATASETS_FOLDER.mkdir()
    csv_file = DATASETS_FOLDER / pathlib.Path(filename)
    csv_file.touch()
    df.to_csv(csv_file, index_label='day')
    return df


def save_price_history(from_symbol, to_symbol):
    csv_string = get_csv_string(from_symbol, to_symbol)
    df = csv_string_to_dataframe(csv_string)
    df_to_file(df, '{}-{}.csv'.format(from_symbol, to_symbol))
    return df


def download_dataset_from_cyptodatadownload_website():
    print('Reference period: {} --> {}'.format(START_REF_PERIOD, END_REF_PERIOD))

    # download BTC-USD
    print('Downloading data for: BTC-USD ...')
    df_btc_vs_usd = save_price_history('BTC', 'USD')

    # download ETH-USD
    print('Downloading data for: ETH-USD ...')
    save_price_history('ETH', 'USD')

    # download the rest of altcoins
    for altcoin in ALTCOINS:
        print('Downloading data for: {}-BTC ...'.format(altcoin))
        try:
            # retrieve raw data
            csv_string = get_csv_string(altcoin, 'BTC')

            # obtain dataframes
            df_vs_btc = csv_string_to_dataframe(csv_string)
            df_vs_usd = refer_to_usd(df_vs_btc, df_btc_vs_usd)

            # save both BTC and USD based datasets for the altcoin
            df_to_file(df_vs_btc, '{}-BTC.csv'.format(altcoin))
            df_to_file(df_vs_usd, '{}-USD.csv'.format(altcoin))
        except Exception as e:
            print(e)
            continue
    print('Done')


if __name__ == '__main__':
    download_dataset_from_cyptodatadownload_website()
