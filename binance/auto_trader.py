#coding: utf-8
from common import utils
from common import const
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *


class AutoTrader(object):
    def __init__(self, symbol) -> None:
        super().__init__()
        self.symbol = symbol
        user_info = utils.get_binance_user_info()
        self.request_client = RequestClient(api_key=user_info['api_key'], secret_key=user_info['secret_key'])

    def get_positions(self, dire):
        result = self.request_client.get_position_v2()
        rets = []
        for pos in result:
            if pos.symbol != self.symbol:
                continue

            if pos.positionSide != dire:
                continue

            rets.append(pos)

        return rets

    def get_orders(self):
        result = self.request_client.get_open_orders('ETHUSDT')
        PrintMix.print_data(result)

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



    def run(self):
        poses = self.get_positions(const.TradeSide.SHORT)
        for pos in poses:
            for k, v in pos.__dict__.items():
                print(k, v)
        self.get_orders()
        self.open_short('ETHUSDT', 3060, 0.04)
        self.open_short('ETHUSDT', 3110, 0.08)
        self.open_short('ETHUSDT', 3160, 0.16)
        #self.post_order()

def main():
    at = AutoTrader('ETHUSDT')
    at.run()

if __name__ == '__main__':
    main()