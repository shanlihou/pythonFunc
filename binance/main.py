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
    try:
        cm = config_manager.ConfigManager()
    except Exception as e:
        print(e)
        cm = None


    _mail = mail.get_default_user_mail()
    listener = []
    byte_coin_cmper = {}
    reset(cm, listener, byte_coin_cmper)

    while 1:
        try:
            if not cm.load_config_and_check():
                reset(cm, listener, byte_coin_cmper)
        except Exception as e:
            print(f'load error:{e}')

        try:
            for _lis in listener:
                klines = _lis.get()
                cmp = byte_coin_cmper[_lis.symbol]
                send_str = f'coin[{_lis.symbol}] {klines[-1]}, cmp is:{cmp}'
                max_vol = max(i.deal_rice for i in klines)
                for k in klines:
                    print(k, f', vol:{(k.deal_rice / max_vol):.2f}')
                print(_lis.symbol, '-' * 60)
                if cmp.compare(klines[-1].end_rice):
                    _mail.send_mail('472888366@qq.com', send_str, send_str)
        except Exception as e:
            print(f'meet error:{e}')

        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print(f'{time_str}------------------------------------------------------\n')
        time.sleep(30)


def update_config():
    cm = config_manager.ConfigManager()
    cm.set_default_config()


def test_order():
    user_info = utils.get_binance_user_info()
    request_client = RequestClient(api_key=user_info['api_key'], secret_key=user_info['secret_key'])
    result = request_client.get_position_v2()
    print(result.__class__)
    for i in result:
        if i.symbol != 'ETHUSDT':
            continue
        print('i class is:', i.__class__)
        for k, v in i.__dict__.items():
            print(k, v)
        print('-' * 20)
    #PrintMix.print_data(result)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'up':
            update_config()
        elif sys.argv[1] == 'test':
            test_order()
        else:
            main()