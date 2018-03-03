#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.utils import *

class BasicApi(object):
    # 获取KLine
    @staticmethod
    def get_kline(symbol, period, size=150):
        """

        :param symbol: 交易对, btcusdt, bchbtc, rcneth ...
        :param period: K线类型, 可选值：{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
        :param size: 获取数量, 可选值： [1,2000]
        :return:
        """
        params = {'symbol': symbol,
                  'period': period,
                  'size': size}

        url = MARKET_URL + '/market/history/kline'
        return http_get_request(url, params)

    # 获取marketdepth
    @staticmethod
    def get_depth(symbol, md_type):
        """
        :param symbol
        :param md_type: type 可选值：{ percent10, step0, step1, step2, step3, step4, step5 }
        :return:
        """
        params = {'symbol': symbol,
                  'type': md_type}

        url = MARKET_URL + '/market/depth'
        return http_get_request(url, params)

    # 获取tradedetail
    @staticmethod
    def get_trade(symbol):
        """
        :param symbol
        :return:
        """
        params = {'symbol': symbol}

        url = MARKET_URL + '/market/trade'
        return http_get_request(url, params)

    # 获取批量交易信息tradedetail
    @staticmethod
    def get_batch_trade(symbol, size):
        """
        :param symbol
        :param size
        :return:
        """
        params = {'symbol': symbol, 'size': size}

        url = MARKET_URL + '/market/history/trade'
        return http_get_request(url, params)

    # 获取merge ticker
    @staticmethod
    def get_ticker(symbol):
        """
        :param symbol:
        :return:
        """
        params = {'symbol': symbol}

        url = MARKET_URL + '/market/detail/merged'
        return http_get_request(url, params)

    # 获取 Market Detail 24小时成交量数据
    @staticmethod
    def get_detail(symbol):
        """
        :param symbol
        :return:
        """
        params = {'symbol': symbol}

        url = MARKET_URL + '/market/detail'
        return http_get_request(url, params)

    # 获取火币支持的交易对
    @staticmethod
    def get_symbols(long_polling=None):
        """

        """
        params = {}
        if long_polling:
            params['long-polling'] = long_polling
        path = '/v1/common/symbols'
        return api_key_get(params, path)

    # 获取火币支持的交易对
    @staticmethod
    def get_currencys(long_polling=None):
        """

        """
        params = {}
        if long_polling:
            params['long-polling'] = long_polling
        path = '/v1/common/currencys'
        return api_key_get(params, path)

    '''
    Trade/Account API
    '''

    @staticmethod
    def get_accounts():
        """
        :return:
        """
        path = "/v1/account/accounts"
        params = {}
        return api_key_get(params, path)

    # 获取当前账户资产
    @staticmethod
    def get_balance(acct_id=None):
        """
        :param acct_id
        :return:
        """

        if not acct_id:
            accounts = BasicApi.get_accounts()
            acct_id = accounts['data'][0]['id']

        url = "/v1/account/accounts/{0}/balance".format(acct_id)
        params = {"account-id": acct_id}
        return api_key_get(params, url)

    # 下单

    # 创建并执行订单
    @staticmethod
    def send_order(amount, source, symbol, _type, price=0):
        """
        :param amount:
        :param source: 如果使用借贷资产交易，请在下单接口,请求参数source中填写'margin-api'
        :param symbol:
        :param _type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param price:
        :return:
        """
        try:
            accounts = BasicApi.get_accounts()
            acct_id = accounts['data'][0]['id']
        except BaseException as e:
            print('get acct_id error.%s' % e)
            acct_id = ACCOUNT_ID

        params = {"account-id": acct_id,
                  "amount": amount,
                  "symbol": symbol,
                  "type": _type,
                  "source": source}
        if price:
            params["price"] = price

        url = '/v1/order/orders/place'
        return api_key_post(params, url)

    # 撤销订单
    @staticmethod
    def cancel_order(order_id):
        """

        :param order_id:
        :return:
        """
        params = {}
        url = "/v1/order/orders/{0}/submitcancel".format(order_id)
        return api_key_post(params, url)

    # 查询某个订单
    @staticmethod
    def order_info(order_id):
        """

        :param order_id:
        :return:
        """
        params = {}
        url = "/v1/order/orders/{0}".format(order_id)
        return api_key_get(params, url)

    # 查询某个订单的成交明细
    @staticmethod
    def order_matchresults(order_id):
        """

        :param order_id:
        :return:
        """
        params = {}
        url = "/v1/order/orders/{0}/matchresults".format(order_id)
        return api_key_get(params, url)

    # 查询当前委托、历史委托
    @staticmethod
    def orders_list(symbol, states, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
        """

        :param symbol:
        :param states: 可选值
            {
                pre-submitted 准备提交,
                submitted 已提交,
                partial-filled 部分成交,
                partial-canceled 部分成交撤销,
                filled 完全成交,
                canceled 已撤销
            }
        :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param start_date:
        :param end_date:
        :param _from:
        :param direct: 可选值{prev 向前，next 向后}
        :param size:
        :return:
        """
        params = {'symbol': symbol,
                  'states': states}

        if types:
            params[types] = types
        if start_date:
            params['start-date'] = start_date
        if end_date:
            params['end-date'] = end_date
        if _from:
            params['from'] = _from
        if direct:
            params['direct'] = direct
        if size:
            params['size'] = size
        url = '/v1/order/orders'
        return api_key_get(params, url)

    # 查询当前成交、历史成交
    @staticmethod
    def orders_matchresults(symbol, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
        """

        :param symbol:
        :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param start_date:
        :param end_date:
        :param _from:
        :param direct: 可选值{prev 向前，next 向后}
        :param size:
        :return:
        """
        params = {'symbol': symbol}

        if types:
            params[types] = types
        if start_date:
            params['start-date'] = start_date
        if end_date:
            params['end-date'] = end_date
        if _from:
            params['from'] = _from
        if direct:
            params['direct'] = direct
        if size:
            params['size'] = size
        url = '/v1/order/matchresults'
        return api_key_get(params, url)

    # 申请提现虚拟币
    @staticmethod
    def withdraw(address_id, amount, currency, fee=0, addr_tag=""):
        """

        :param address_id:
        :param amount:
        :param currency:btc, ltc, bcc, eth, etc ...(火币Pro支持的币种)
        :param fee:
        :param addr_tag: addr-tag
        :return: {
                  "status": "ok",
                  "data": 700
                }
        """
        params = {'address': address_id,
                  'amount': amount,
                  "currency": currency,
                  "fee": fee,
                  "addr-tag": addr_tag}
        url = '/v1/dw/withdraw/api/create'

        return api_key_post(params, url)

    # 申请取消提现虚拟币
    @staticmethod
    def cancel_withdraw(address_id):
        """

        :param address_id:
        :return: {
                  "status": "ok",
                  "data": 700
                }
        """
        params = {}
        url = '/v1/dw/withdraw-virtual/{0}/cancel'.format(address_id)

        return api_key_post(params, url)

    '''
    借贷API
    '''

    # 创建并执行借贷订单


    @staticmethod
    def send_margin_order(amount, symbol, _type, source='margin-api', price=0):
        """
        :param amount:
        :param source: 'margin-api'
        :param symbol:
        :param _type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param price:
        :return:
        """
        try:
            accounts = BasicApi.get_accounts()
            acct_id = accounts['data'][0]['id']
        except BaseException as e:
            print('get acct_id error.%s' % e)
            acct_id = ACCOUNT_ID

        params = {"account-id": acct_id,
                  "amount": amount,
                  "symbol": symbol,
                  "type": _type,
                  "source": source}
        if price:
            params["price"] = price

        url = '/v1/order/orders/place'
        return api_key_post(params, url)

    # 现货账户划入至借贷账户


    @staticmethod
    def exchange_to_margin(symbol, currency, amount):
        """
        :param amount:
        :param currency:
        :param symbol:
        :return:
        """
        params = {"symbol": symbol,
                  "currency": currency,
                  "amount": amount}

        url = "/v1/dw/transfer-in/margin"
        return api_key_post(params, url)

    # 借贷账户划出至现货账户


    @staticmethod
    def margin_to_exchange(symbol, currency, amount):
        """
        :param amount:
        :param currency:
        :param symbol:
        :return:
        """
        params = {"symbol": symbol,
                  "currency": currency,
                  "amount": amount}

        url = "/v1/dw/transfer-out/margin"
        return api_key_post(params, url)

    # 申请借贷
    @staticmethod
    def get_margin(symbol, currency, amount):
        """
        :param amount:
        :param currency:
        :param symbol:
        :return:
        """
        params = {"symbol": symbol,
                  "currency": currency,
                  "amount": amount}
        url = "/v1/margin/orders"
        return api_key_post(params, url)

    # 归还借贷
    @staticmethod
    def repay_margin(order_id, amount):
        """
        :param order_id:
        :param amount:
        :return:
        """
        params = {"order-id": order_id,
                  "amount": amount}
        url = "/v1/margin/orders/{0}/repay".format(order_id)
        return api_key_post(params, url)

    # 借贷订单
    @staticmethod
    def loan_orders(symbol, currency, start_date="", end_date="", start="", direct="", size=""):
        """
        :param symbol:
        :param currency:
        :param direct: prev 向前，next 向后
        :param start_date:
        :param end_date:
        :param start:
        :param size:
        :return:
        """
        params = {"symbol": symbol,
                  "currency": currency}
        if start_date:
            params["start-date"] = start_date
        if end_date:
            params["end-date"] = end_date
        if start:
            params["from"] = start
        if direct and direct in ["prev", "next"]:
            params["direct"] = direct
        if size:
            params["size"] = size
        url = "/v1/margin/loan-orders"
        return api_key_get(params, url)

    # 借贷账户详情,支持查询单个币种
    @staticmethod
    def margin_balance(symbol):
        """
        :param symbol:
        :return:
        """
        params = {}
        url = "/v1/margin/accounts/balance"
        if symbol:
            params['symbol'] = symbol

        return api_key_get(params, url)
