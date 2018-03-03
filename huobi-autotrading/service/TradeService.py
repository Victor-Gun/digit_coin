#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from apis.restful.BasicApi import BasicApi
from utils.MySQLUtil import MySQLUtil


class TradeService(object):
    def __init__(self):
        self.database = MySQLUtil()

    # 保存火币支持的交易对
    def save_trade_symbols(self):
        domain_array = [
            'symbol_partition',
            'base_currency',
            'quote_currency',
            'price_precision',
            'amount_precision',
            'c_t',
            'u_t'
        ]

        for symbol in BasicApi.get_symbols()['data']:
            self.database.query_dic({
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
