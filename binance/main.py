#coding: utf-8
from common import utils
import requests
import time
import biance
import mail
import comparer
import sys
import config_manager
import json
import argparse

from binance_with_api import auto_trader
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *


def reset(cm, listener, byte_coin_cmper):
    listener.clear()
    byte_coin_cmper.clear()
    if cm is None:
        config = json.load(open('config\\binance_default.json'))
        config = config['notify_strategy']
    else:
        config = cm.config['notify_strategy']
    for k, v in config.items():
        listener.append(biance.BinanceKlines(k))
        cmp = comparer.get_comp_from_dic(v)
        byte_coin_cmper[k] = cmp


def main():
    # try:
    #     cm = config_manager.ConfigManager()
    # except Exception as e:
    #     print(e)
    #     cm = None
    cm = None

    _mail = mail.get_default_user_mail()
    listener = []
    byte_coin_cmper = {}
    reset(cm, listener, byte_coin_cmper)

    while 1:
        # try:
        #     if not cm.load_config_and_check():
        #         reset(cm, listener, byte_coin_cmper)
        # except Exception as e:
        #     print(f'load error:{e}')

        try:
            for _lis in listener:
                klines = _lis.get()
                cmp = byte_coin_cmper[_lis.symbol]
                send_str = f'{_lis.symbol}到了价位{klines[-1].end_rice}'
                max_vol = max(i.deal_rice for i in klines)
                for k in klines:
                    print(k, f', vol:{(k.deal_rice / max_vol):.2f}')
                print(_lis.symbol, '-' * 60)
                if cmp.compare(klines[-1].end_rice):
                    _mail.send_mail('472888366@qq.com', send_str, send_str)
        except Exception as e:
            print(f'meet error:{e}')

        time_t = time.localtime(time.time())
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_t)
        percent = ((time_t.tm_min % 30) / 30 * 100)
        print(f'{time_str}  {percent:.2f}%------------------------------------------------------\n')
        time.sleep(30)


def update_config():
    cm = config_manager.ConfigManager()
    cm.set_default_config()


def test_order():
    at = auto_trader.AutoTrader()
    at.get_klines()
    #PrintMix.print_data(result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--update', help="update bmob config", action="store_true")
    parser.add_argument('-t', '--test', help="test", action="store_true")
    parser.add_argument('-r', '--run', help="run tick", action="store_true")
    args = parser.parse_args()
    if args.update:
        update_config()
    elif args.test:
        test_order()
    elif args.run:
        main()
