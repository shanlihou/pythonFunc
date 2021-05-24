#coding: utf-8
from common import utils
import sys
from common import const
from common import sh_log
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from . import position
from . import order
from . import calc


console = sys.stdout
def self_print(print_str):
    console.write(print_str + '\n')


class AutoTrader(object):
    def __init__(self) -> None:
        super().__init__()
        user_info = utils.get_binance_user_info()
        self.request_client = RequestClient(api_key=user_info['api_key'], secret_key=user_info['secret_key'])

    def get_positions(self, symbol, dire):
        result = self.request_client.get_position_v2()
        rets = []
        for pos in result:
            if symbol and pos.symbol != symbol:
                continue

            if dire and pos.positionSide != dire:
                continue

            rets.append(position.Position(
                pos.symbol,
                pos.entryPrice,
                pos.markPrice,
                pos.unrealizedProfit,
                pos.positionSide,
                pos.positionAmt,
            ))

        return rets

    def cancel_order(self, symbol, order_id):
        return self.request_client.cancel_order(symbol=symbol, orderId=order_id)

    def get_orders(self, symbol):
        rets = []
        ret = self.request_client.get_open_orders(symbol)
        for _order in ret:
            rets.append(order.Order(
                _order.symbol,
                _order.orderId,
                _order.side,
                _order.positionSide,
                _order.price,
                _order.origQty,
                _order.type,
            ))
        return rets

    def open_short(self, symbol, price, quantity):
        result = self.request_client.post_order(
            symbol=symbol,
            side=OrderSide.SELL,
            ordertype=OrderType.LIMIT,
            price=price,
            quantity=quantity,
            timeInForce="GTC",
            closePosition=False,
            positionSide="SHORT")

    def print_positions(self):
        poses = self.get_positions('ETHUSDT', const.TradeSide.SHORT)
        for pos in poses:
            sh_log.sh_print(pos)

    def get_small_order_qty(self, mark_price):
        return 5 / mark_price

    def one_key_order(self, symbol, side, small_order_qty):
        pos_side = 'LONG' if side == 'SHORT' else 'SHORT'

        pos = self.get_positions(symbol, pos_side)
        pos = pos[0]
        sh_log.sh_print(pos)
        _small_order_qty = self.get_small_order_qty(pos.mark_price)
        sh_log.sh_print('small', _small_order_qty)
        if small_order_qty < _small_order_qty:
            sh_log.sh_print('[ERROR]: could not use small price:', _small_order_qty)
            return



    def run(self):
        # self.open_short('MATICUSDT', 1.87, 3)
        #self.open_short('MATICUSDT', '1.97', 9)
        # self.open_short('MATICUSDT', '2.07', 27)
        #self.open_short('ETHUSDT', '2460', '0.027')
        # ret = self.get_orders('ETHUSDT')
        # for _order in ret:
        #     sh_log.sh_print(_order)

        # self.print_positions()
        #self.cancel_order('ETHUSDT', '8389765498173618739')

        # self.open_short('ETHUSDT', 3060, 0.04)
        # self.open_short('ETHUSDT', 3110, 0.08)
        # self.open_short('ETHUSDT', 3160, 0.16)
        #self.post_order()
        self.one_key_order('DOGEUSDT', 'SHORT')