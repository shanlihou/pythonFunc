#coding: utf-8
import requests
import time
import biance
import mail
import comparer
import config_manager


def reset(cm, listener, byte_coin_cmper):
    listener.clear()
    byte_coin_cmper.clear()
    for k, v in cm.config['notify_strategy'].items():
        listener.append(biance.BinanceKlines(k))
        cmp = comparer.get_comp_from_dic(v)
        byte_coin_cmper[k] = cmp


def main():
    cm = config_manager.ConfigManager()
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
                send_str = f'coin[{_lis.symbol}] {klines}, cmp is:{cmp}'
                print(send_str)
                if cmp.compare(klines.end_rice):
                    _mail.send_mail('472888366@qq.com', send_str, send_str)
        except Exception as e:
            print(f'meet error:{e}')
        print(f'{time.localtime(time.time())}------------------------------------------------------\n')
        time.sleep(60)


def update_config():
    cm = config_manager.ConfigManager()
    cm.set_default_config()


def test_order():
    pass



if __name__ == '__main__':
    main()