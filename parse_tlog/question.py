# coding:utf-8
# 【【服务端log】[Avatar(28339)]:ckz: friend not in my friends: 8444836000281342769】
# https://www.tapd.cn/57153713/bugtrace/bugs/view/1157153713001025519

import utils
import const
import LogOne
import Filter

gbid1 = '8444837063422203219'
gbid2 = '8444837064372912131'

def main1():
    fname = utils.filter_from_origin('SecSNSGetFlow')
    print(fname)
    with utils.utf8_open(fname) as fr:
        for line in fr:
            if gbid1 in line and gbid2 in line:
                print(line)

def main2():
    fname = utils.filter_from_origin('PlayerFriendsList')
    print(fname)
    with utils.utf8_open(fname) as fr:
        for line in fr:
            log_one = LogOne.get_log_from_line(line)
            if log_one.gbid == gbid2:
                print(log_one.time_str, log_one.friend_gbid, log_one.friend_name)


def login():
    fname = Filter.Filter.filter_login_log()
    print(fname)
    with utils.utf8_open(fname) as fr:
        for line in fr:
            log_one = LogOne.get_log_from_line(line)
            if log_one.gbid == gbid2:
                print(log_one.FILTER_STR, log_one.time_str)


if __name__ == '__main__':
    main1()
    main2()
    login()