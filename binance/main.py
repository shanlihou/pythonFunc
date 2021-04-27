#coding: utf-8
import requests
import time
import biance
import mail

BYTE_COIN_LISTEN = {
    'BTCUSDT': lambda x: x < 50000,
    'ETHUSDT': lambda x: x < 2400,
    'BNBUSDT': lambda x: x < 500,
    'DOGEUSDT': lambda x: x < 0.2,
    'LTCUSDT': lambda x: x < 200,
    'XRPUSDT': lambda x: x < 1.2,
}


def main():
    _mail = mail.get_default_user_mail()
    listener = []
    for key in BYTE_COIN_LISTEN:
        listener.append(biance.BinanceAvgPrice(key))

    while 1:
        try:
            for _lis in listener:
                cur = float(_lis.get())
                print(f'coin[{_lis.symbol}] cur is:{cur}')
                func = BYTE_COIN_LISTEN[_lis.symbol]
                if func(cur):
                    _mail.send_mail('472888366@qq.com', f'coin[{_lis.symbol}] could bye, cur:{cur}', 'see subject')
        except Exception as e:
            print(f'meet error:{e}')
        print('------------------------------------------------------\n')
        time.sleep(60)


if __name__ == '__main__':
    main()
