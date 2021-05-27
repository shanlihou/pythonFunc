from common import const
import functools
import json


@functools.lru_cache(maxsize=1)
def get_binance_user_info():
    with open(const.USER_INFO) as fr:
        return json.load(fr)


@functools.lru_cache(1)
def get_user_info():
    return json.load(open(const.USER_INFO))