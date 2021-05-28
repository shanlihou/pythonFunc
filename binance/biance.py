import requests
import attr
import json
import common_struct
import time
import functools

import hmac
from hashlib import sha256
from common import const
from common import utils


http_proxy  = "http://127.0.0.1:7890"
https_proxy = "http://127.0.0.1:7890"
ftp_proxy   = "ftp://127.0.0.1:7890"

proxyDict = {
              "http"  : http_proxy,
              "https" : https_proxy,
              "ftp"   : ftp_proxy
            }

HOST = 'https://api.binance.com'
#HOST = 'https://fapi.binance.com'


def get_sig(appsecret, data):
    appsecret = appsecret.encode('utf-8')
    data = data.encode('utf-8')
    print(appsecret, data)
    return hmac.new(appsecret, data, digestmod=sha256).hexdigest()


class BinanceBase(object):
    API = ''
    def __attrs_post_init__(self):
        json_data = utils.get_user_info()
        self.api_key = json_data['api_key']
        self.secret_key = json_data['secret_key']

    @staticmethod
    def get_url(api):
        return f'{HOST}{api}'

    def get_header(self):
        return {
            'X-MBX-APIKEY': self.api_key
        }

    def get(self):
        url = self.get_url(self.API)
        ret = requests.get(url, proxies=proxyDict, params=self.params())
        return self.parse_response(ret.text)

    def post(self):
        url = self.get_url(self.API)
        ret = requests.post(url, proxies=proxyDict, params=self.params(), headers=self.get_header())
        print(ret.url)
        return self.parse_response(ret.text)

    @staticmethod
    def parse_response(data):
        return data

    def params(self):
        try:
            return attr.asdict(self)
        except:
            return {}

    @staticmethod
    def load_exchange_info():
        ret = json.load(open('test.json'))
        for i in ret:
            print(i)

        return
        for i in ret['symbols']:
            if 'USDT' not in i['symbol']:
                continue
            print(i['symbol'])


class BinancePing(BinanceBase):
    API = '/api/v1/ping'


class BinanceTime(BinanceBase):
    API = '/api/v1/time'


class BinanceExchangeInfo(BinanceBase):
    API = '/api/v1/exchangeInfo'


@attr.s
class BinanceDepth(BinanceBase):
    API = '/api/v1/depth'
    symbol = attr.ib(default='BTCUSDT')
    limit = attr.ib(default=20)


@attr.s
class BinanceTrades(BinanceBase):
    API = '/api/v1/trades'
    symbol = attr.ib(default='BTCUSDT')
    limit = attr.ib(default=20)


@attr.s
class BinanceKlines(BinanceBase):
    API = '/api/v1/klines'
    symbol = attr.ib(default='BTCUSDT')
    interval = attr.ib(default='30m')
    limit = attr.ib(default=4)

    @staticmethod
    def parse_response(data):
        json_data = json.loads(data)
        kList = []
        for i in json_data:
            klines = common_struct.KLines(*i)
            kList.append(klines)

        return kList


@attr.s
class BinanceAvgPrice(BinanceBase):
    API = '/api/v3/avgPrice'
    symbol = attr.ib(default='BTCUSDT')

    @staticmethod
    def parse_response(data):
        return json.loads(data)['price']


@attr.s
class BinanceTicker(BinanceBase):
    API = '/api/v1/ticker/24hr'
    symbol = attr.ib(default='BTCUSDT')


@attr.s
class BinanceTickerPrice(BinanceBase):
    API = '/api/v3/ticker/price'
    symbol = attr.ib(default='BTCUSDT')


@attr.s
class BinanceTickerBookTicker(BinanceBase):
    API = '/api/v3/ticker/bookTicker'
    symbol = attr.ib(default='BTCUSDT')


@attr.s
class BinanceOrder(BinanceBase):
    API = '/api/v3/order'
    symbol = attr.ib(default='MATICUSDT')

    def params(self):
        _params = {
            'symbol': self.symbol,
            'side': 'BUY',
            'type': 'LIMIT',
            'timeInForce': 'GTC',
            'quantity': '5',
            'price': '1',
            'recvWindow': '5000',
            'timestamp': str(int(time.time() * 1000))
        }
        data = '&'.join('{}={}'.format(k, v) for k, v in _params.items())
        sig = get_sig(self.secret_key, data)
        _params['signature'] = sig
        return _params


if __name__ == '__main__':
    btot = BinanceOrder()
    ret = btot.post()
    print(ret)