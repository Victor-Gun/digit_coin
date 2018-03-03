#!/usr/bin/env python
# -*- coding: utf-8 -*-
from service.TradeService import TradeService


class Trade(object):
    """
    K线相关的请求
    """
    # 保存k线数据
    @staticmethod
    def save_trade_symbols(request_args):
        TradeService().save_trade_symbols()
