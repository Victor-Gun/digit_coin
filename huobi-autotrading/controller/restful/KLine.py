#!/usr/bin/env python
# -*- coding: utf-8 -*-
from service.KLineService import KLineService


class KLine(object):
    """
    K线相关的请求
    """
    # 保存k线数据
    @staticmethod
    def save_kline(request_args):
        period = request_args['period']
        size = request_args['size']
        KLineService().save_kline(period, size)
