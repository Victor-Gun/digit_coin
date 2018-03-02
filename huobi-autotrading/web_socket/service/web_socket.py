# encoding=utf8
from web_socket import settings
from web_socket.service import kline_handler
from web_socket.service import mongodb
import gzip
import json
import logging

import websocket

logger = logging.getLogger(__name__)


###
# 本文件通过websocket与火币网实现通信
###

def save_data(msg):
    # if settings.DATABASE_RECORD and mongodb:
    #     try:
    #         collection = mongodb.get_collection(msg['ch'].replace('.', '_'))
    #         collection.insert_one(msg)
    #     except Exception as exp:
    #         logger.error("无法保存到数据库：" + str(exp))
    msg


def send_message(ws, msg_dict):
    data = json.dumps(msg_dict).encode()
    logger.debug("发送消息:" + str(msg_dict))
    ws.send(data)


def on_message(ws, message):
    unzipped_data = gzip.decompress(message).decode()
    msg_dict = json.loads(unzipped_data)
    if 'ping' in msg_dict:
        data = {
            "pong": msg_dict['ping']
        }
        logger.debug("收到ping消息: " + str(msg_dict))
        send_message(ws, data)
    elif 'subbed' in msg_dict:
        logger.debug("收到订阅状态消息：" + str(msg_dict))
    else:
        save_data(msg_dict)
        logger.debug("收到消息: " + str(msg_dict))
        kline_handler.handle_raw_message(msg_dict)


def on_error(ws, error):
    error = gzip.decompress(error).decode()
    logger.error(str(error))


def on_close(ws):
    logger.info("已断开连接")


def on_open(ws):
    # 遍历settings中的货币对象
    for currency in settings.COINS.keys():
        # 订阅 KLine 数据 market.$symbol.kline.$period
        subscribe = "market.{0}{1}.kline.{2}".format(currency, settings.SYMBOL, settings.PERIOD).lower()
        # 请求 KLine 数据 market.$symbol.kline.$period
        # 订阅 Market Depth 数据 market.$symbol.depth.$type
        # 请求 Market Depth 数据 market.$symbol.depth.$type
        # 订阅 Trade Detail 数据 market.$symbol.trade.detail
        # 请求 Trade Detail 数据 market.$symbol.trade.detail
        # 请求 Market Detail 数据 market.$symbol.detail
        data = {
            "sub": subscribe,
            "id": currency
        }
        # 订阅K线图
        send_message(ws, data)


def start():
    ws = websocket.WebSocketApp(
        "wss://api.huobipro.com/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()
