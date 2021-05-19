import requests
import attr
import json
import common_struct
import time
from common import const


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


class BinanceBase(object):
    API = ''
    def __attrs_post_init__(self):
        json_data = json.load(open(const.USER_INFO))
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
class BinanceTickerOrderTest(BinanceBase):
    API = '/api/v3/order/test'
    symbol = attr.ib(default='BTCUSDT')


@attr.s
class BinanceTickerOpenOrders(BinanceBase):
    API = '/fapi/v1/openOrders'


if __name__ == '__main__':
    while 1:
        b = BinanceKlines('ETHUSDT')
        ret = b.get()
        for i in ret:
            print(i)
        time.sleep(10)
