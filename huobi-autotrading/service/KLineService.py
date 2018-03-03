#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from apis.restful.BasicApi import BasicApi
from utils.MySQLUtil import MySQLUtil


class KLineService(object):
    def __init__(self):
        self.database = MySQLUtil()

    """
    K线相关的请求
    """
    # 保存k线数据
    def save_kline(self, period, size):
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

        symbols = self.database.query('''select concat(base_currency, quote_currency) from trade_symbols''')
        for symbol in symbols:
            klines = BasicApi.get_kline(symbol[0], period, size)
            if(klines == None):
                continue
            for kl in klines['data']:
                self.database.query_dic({
                    'replace': 'k_line_data',
                    'domain_array': domain_array,
                    'value_array': [
                        symbol[0],
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
