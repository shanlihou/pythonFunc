from common import utils
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

user_info = utils.get_user_info()
http_proxy  = "http://127.0.0.1:7890"
https_proxy = "http://127.0.0.1:7890"
ftp_proxy   = "ftp://127.0.0.1:7890"

proxyDict = {
              "http"  : http_proxy,
              "https" : https_proxy,
              "ftp"   : ftp_proxy
            }
client = Client(user_info['api_key'], user_info['secret_key'], {'proxies': proxyDict})
withdraws = client.get_withdraw_history()
print(withdraws)
# get market depth

# socket manager using threads
twm = ThreadedWebsocketManager()
twm.start()

# depth cache manager using threads
dcm = ThreadedDepthCacheManager()
dcm.start()

def handle_socket_message(msg):
    print(f"message type: {msg['e']}")
    print(msg)

def handle_dcm_message(depth_cache):
    print(f"symbol {depth_cache.symbol}")
    print("top 5 bids")
    print(depth_cache.get_bids()[:5])
    print("top 5 asks")
    print(depth_cache.get_asks()[:5])
    print("last update time {}".format(depth_cache.update_time))

twm.start_kline_socket(callback=handle_socket_message, symbol='BNBBTC')

dcm.start_depth_cache(callback=handle_dcm_message, symbol='ETHBTC')

