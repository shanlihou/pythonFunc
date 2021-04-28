#coding: utf-8
import requests
import time
import biance
import mail
import comparer
import config_manager

BYTE_COIN_LISTEN = {
    'BTCUSDT': comparer.ComparerDown(54000, 500),
    'ETHUSDT': comparer.ComparerDown(2600, 100),
    'BNBUSDT': comparer.ComparerDown(550, 10),
    'DOGEUSDT': comparer.ComparerDown(0.275, 0.01),
    'LTCUSDT': comparer.ComparerDown(250, 5),
    'XRPUSDT': comparer.ComparerDown(1.3, 0.05),
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
                cmp = BYTE_COIN_LISTEN[_lis.symbol]
                send_str = f'coin[{_lis.symbol}] cur is:{cur}, cmp is:{cmp}'
                print(send_str)
                if cmp.compare(cur):
                    _mail.send_mail('472888366@qq.com', send_str, send_str)
        except Exception as e:
            print(f'meet error:{e}')
        print('------------------------------------------------------\n')
        time.sleep(60)


def testConfig():
    b = config_manager.ConfigManager()
    b.test()
    ret = comparer.get_comp_from_dic(b.config['notify_strategy'][0])
    print(ret)

if __name__ == '__main__':
    testConfig()
