#!/usr/bin/env python
# -*- coding: utf-8 -*-
from restful.apis.basic_api import *
from restful.utils.mysql_utils import MySQL
import time

database = MySQL()
# 保存火币支持的交易对
def save_trade_symbols():
    domain_array = [
        'symbol_partition',
        'base_currency',
        'quote_currency',
        'price_precision',
        'amount_precision',
        'c_t',
        'u_t'
    ]

    for symbol in get_symbols()['data']:
        database.query_dic({
            'replace': 'trade_symbols',
            'domain_array': domain_array,
            'value_array': [
                symbol['symbol-partition'],
                symbol['base-currency'],
                symbol['quote-currency'],
                symbol['price-precision'],
                symbol['amount-precision'],
                int(time.time()),
                int(time.time())
            ]
        })

# 保存火币支持的交易对
def save_kline():
    domain_array = [
        'symbol',
        'period',
        'ts',
        'open',
        'close',
        'low',
        'high',
        'amount',
        'vol',
        'count',
        'c_t',
        'u_t'
    ]

    period = '1min'
    symbols = database.query('''
          select base_currency from trade_symbols where symbol_partition='main'
        ''')
    for symbol in symbols:
        isymbol = symbol[0] + 'usdt'
        klines = get_kline(isymbol, period, 2000)
        for kl in klines['data']:
            database.query_dic({
                'replace': 'k_line_data',
                'domain_array': domain_array,
                'value_array': [
                    symbol,
                    period,
                    kl['id'],
                    kl['open'],
                    kl['close'],
                    kl['low'],
                    kl['high'],
                    kl['amount'],
                    kl['vol'],
                    kl['count'],
                    int(time.time()),
                    int(time.time())
                ]
            })


if __name__ == '__main__':
    # save_trade_symbols()
    save_kline()
    # print(get_depth('eosusdt', 'step0'))