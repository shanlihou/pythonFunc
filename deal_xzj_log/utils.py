import functools
import pickle
import time


g_name_gbid_dic = pickle.load(open('name_gbid_dic', 'rb'))
g_gbid_dic = pickle.load(open('gbid_dic', 'rb'))
g_filter_set = pickle.load(open('filter_set', 'rb'))


def is_gbid_inter(gbid):
    return gbid in g_filter_set


def is_name_inter(name):
    gbid = g_name_gbid_dic.get(name)
    if not gbid:
        return False

    return is_gbid_inter(gbid)


def get_account(gbid):
    return g_gbid_dic.get(gbid)


def add_col_header(col_headers, datas):
    return ['{},{}'.format(col_headers[i], data) for i, data in enumerate(datas)]


def get_time_stamp(time_str):
    return time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))