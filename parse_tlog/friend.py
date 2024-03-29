import utils
import const
import LogOne

gbid1 = '8444837063064289279'
gbid2 = '8444837063643662473'

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



if __name__ == '__main__':
    main2()