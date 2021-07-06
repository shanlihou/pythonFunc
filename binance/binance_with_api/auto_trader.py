#coding: utf-8
from common import utils
import sys
from common import const
from common import sh_log
import time
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from . import position
from . import order
from . import calc
import mail


console = sys.stdout
def self_print(print_str):
    console.write(print_str + '\n')


class OrderCallBack(object):
    def __init__(self, od, func) -> None:
        super().__init__()
        self._order = od
        self.func = func

    def do_func(self, mark_price):
        self.func(mark_price, self._order)


class AutoTrader(object):
    def __init__(self) -> None:
        super().__init__()
        self.last_amt = None
        user_info = utils.get_binance_user_info()
        self.request_client = RequestClient(api_key=user_info['api_key'], secret_key=user_info['secret_key'])
        self.order_dic = {}

    def get_klines(self):
        now = int(time.time())
        ret = self.request_client.get_candlestick_data('ETHUSDT', '30m', (now - 120) * 1000, now * 1000, 4)

    def get_positions(self, symbol, dire=None):
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
            rets.append(order.Order.from_order(_order))
        return rets

    def open_short(self, symbol, price, quantity):
        return self.post_order(
            symbol=symbol,
            side=OrderSide.SELL,
            ordertype=OrderType.LIMIT,
            price=price,
            quantity=quantity,
            timeInForce="GTC",
            closePosition=False,
            positionSide="SHORT")

    def post_order(self, *args, **kwargs):
        ret = self.request_client.post_order(*args, **kwargs)
        od = order.Order.from_order(ret)
        ocb = OrderCallBack(od, self.on_callback)
        self.order_dic[od.order_id] = ocb

    def on_callback(self, mark_price, one_order):
        sh_log.sh_print('on callback', mark_price, one_order)

    def do_callback(self, symbol, mark_price):
        orders = self.get_orders(symbol)
        id_set = set()
        for _order in orders:
            id_set.add(_order.order_id)

        #sh_log.sh_print(id_set)
        for order_id, ocb in list(self.order_dic.items()):
            if order_id not in id_set:
                ocb.do_func(mark_price)
                self.order_dic.pop(order_id)



    def open_long(self, symbol, price, quantity):
        return self.post_order(
            symbol=symbol,
            side=OrderSide.BUY,
            ordertype=OrderType.LIMIT,
            price=price,
            quantity=quantity,
            timeInForce="GTC",
            closePosition=False,
            positionSide="LONG")

    def take_short(self, symbol, price, quantity=None):
        if quantity is None:
            closePosition = True
            quantity = 0
        else:
            closePosition = False

        return self.post_order(
            symbol=symbol,
            side=OrderSide.BUY,
            ordertype=OrderType.TAKE_PROFIT_MARKET,
            stopPrice=price,
            quantity=quantity,
            timeInForce="GTC",
            closePosition=closePosition,
            positionSide="SHORT")

    def take_long(self, symbol, price, quantity=None):
        if quantity is None:
            closePosition = True
            quantity = 0
        else:
            closePosition = False

        return self.post_order(
            symbol=symbol,
            side=OrderSide.SELL,
            ordertype=OrderType.TAKE_PROFIT_MARKET,
            stopPrice=price,
            quantity=quantity,
            timeInForce="GTC",
            closePosition=closePosition,
            positionSide="LONG")

    def cancel_all_orders(self, symbol):
        return self.request_client.cancel_all_orders(symbol=symbol)

    def print_info(self, symbol):
        poses = self.get_positions(symbol)
        for pos in poses:
            sh_log.sh_print(pos)

        ret = self.get_orders(symbol)
        ret = sorted(ret, key=lambda x: (x.pos_side, x.side, x.stop_price, x.price))
        for _order in ret:
            sh_log.sh_print(_order)

    def get_small_order_qty(self, mark_price):
        return 5 / mark_price

    def one_key_order(self, symbol, side, small_order_qty, level):
        pos_side = 'LONG' if side == 'SHORT' else 'SHORT'

        pos = self.get_positions(symbol, pos_side)
        pos = pos[0]
        sh_log.sh_print(pos)
        _small_order_qty = self.get_small_order_qty(pos.mark_price)
        sh_log.sh_print('small', _small_order_qty)
        if small_order_qty < _small_order_qty:
            sh_log.sh_print('[ERROR]: could not use small price:', _small_order_qty)
            return

        ret = calc.cacl_by_avg_rice(pos.mark_price, level, pos.enter_price, small_order_qty)
        sh_log.sh_print(ret)

    def print_balance(self):
        rets = self.request_client.get_balance_v2()
        for k, v in rets[1].__dict__.items():
            sh_log.sh_print(k, v)

    def get_all_orders(self, symbol):
        orders = self.request_client.get_all_orders(symbol)
        rets = []
        for ret in orders:
            rets.append(order.Order.from_order(ret))

        return rets

    def init_order_dic(self):
        orders = self.get_orders('MATICUSDT')
        for _order in orders:
            ocb = OrderCallBack(_order, self.on_callback)
            self.order_dic[_order.order_id] = ocb

    def test(self):
        # self.open_short('MATICUSDT', 1.87, 3)
        #self.open_short('MATICUSDT', '1.97', 9)
        # self.open_short('MATICUSDT', '2.07', 27)
        #self.open_short('ETHUSDT', '2460', '0.027')
        #self.stop_profit('ETHUSDT', '2200', '0.07')
        #self.open_long('MATICUSDT', '1.55', 6)
        #self.open_long('MATICUSDT', '1.05', 9)
        #self.open_long('MATICUSDT', '0.95', 9)
        #self.open_long('MATICUSDT', '2.23', 66)
        #self.take_long('MATICUSDT', '2.29')
        #self.cancel_order('ETHUSDT', '10808389011')

        #ret = self.open_short('MATICUSDT', '100', 1)
        #ret = order.Order.from_order(ret)
        #sh_log.sh_print(ret)
        #self.cancel_all_orders('ETHUSDT')
        # # self.open_long('MATICUSDT', '2.22', 22)
        # # self.open_long('MATICUSDT', '2.25', 22)
        # #self.open_long('MATICUSDT', '2.305', 66)
        # #self.take_long('MATICUSDT', '2.32')
        # #self.take_long('MATICUSDT', '2.305')
        # #self.take_short('MATICUSDT', 2685, '0.03')
        # self.take_short('MATICUSDT', '1.8', 15)
        # self.take_short('MATICUSDT', '1.75', 15)
        # self.take_short('MATICUSDT', '1.7', 15)
        # self.take_short('MATICUSDT', '1.65', 15)
        # self.take_short('MATICUSDT', '1.6', 15)
        # self.take_short('MATICUSDT', '1.55', 15)

        #self.take_short('MATICUSDT', '1.83', 100)
        # start = 2674
        # for i in range(10):
        #     start += 8
        #     sh_log.sh_print('cur:', start)
        #     self.open_short('ETHUSDT', start, '0.003')

        #self.open_long('MATICUSDT', '1.78', 20)
        #self.open_short('ETHUSDT', '2710', '0.02')
        #self.open_short('MATICUSDT', '1.956', '10')
        #self.open_short('ETHUSDT', 2860, '0.06')
        # ret = self.get_all_orders('MATICUSDT')
        # for _ret in ret:
        #     sh_log.sh_print(_ret)
        # sh_log.sh_print('\n')
        #self.take_short('MATICUSDT', 2800, '0.06')
        #self.open_short('DOGEUSDT', '0.36', '50')
        self.print_info('MATICUSDT')
        sh_log.sh_print('\n')

        self.print_info('ETHUSDT')
        sh_log.sh_print('\n')

        self.print_info('DOGEUSDT')
        sh_log.sh_print('\n')

        self.print_info('UNIUSDT')
        sh_log.sh_print('\n')
        self.print_balance()
        #self.open_long('MATICUSDT', '0.95', 9)
        #self.cancel_order('ETHUSDT', '8389765498337130907')

        # self.open_short('ETHUSDT', 3060, 0.04)
        # self.open_short('ETHUSDT', 3110, 0.08)
        # self.open_short('ETHUSDT', 3160, 0.16)
        #self.post_order()
        #@self.one_key_order('ETHUSDT', 'LONG', 16, 3)

    def _eth_auto_buy(self):
        sh_log.sh_print('-' * 20 + '\n')
        poses = self.get_positions('ETHUSDT', const.TradeSide.SHORT)
        if len(poses) < 1:
            return

        pos = poses[0]
        sh_log.sh_print(pos, type(pos.amt))

        orders = self.get_orders('ETHUSDT')
        target_order = None
        for _order in orders:
            sh_log.sh_print(_order)
            if 0.005 < _order.qty < 0.015:
                target_order = _order

        if pos.amt < -0.075:
            if target_order is None:
                self.take_short('ETHUSDT', (pos.enter_price // 1) - 5, 0.01)
        else:
            if target_order is None:
                self.open_short('ETHUSDT', (pos.enter_price // 1) + 5, 0.01)

    def run_once(self):
        poses = self.get_positions('MATICUSDT', const.TradeSide.SHORT)
        pos = poses[0]
        sh_log.sh_print(pos)
        self.do_callback(pos.mark_price)
        if self.last_amt is None:
            self.last_amt = pos.amt

        if pos.amt != self.last_amt:
            if pos.amt < self.last_amt:
                mail.get_default_user_mail().send_mail('472888366@qq.com', '卖出成功', '成功卖出')
            else:
                mail.get_default_user_mail().send_mail('472888366@qq.com', '下单成功', '成功下单')

        self.last_amt = pos.amt


    def _run(self):
        # self.test()
        self.init_order_dic()
        while 1:
            try:
                self.run_once()
            except Exception as e:
                sh_log.sh_print(e)

            time.sleep(10)

    def run(self):
        self._run()
