# coding:utf-8
# 玩家ID 玩家昵称  OPENID 首次登陆时间 最后登陆时间 最后等级 男女 第二天 第三天是否登陆

import Filter
import const
import LogOne
import heapq
import utils


class AvatarVal(object):
    def __init__(self, gbid, open_id):
        self.gbid = gbid
        self.open_id = open_id
        self.level = -1
        self.log_info = []
        self.days = set()

    def update(self, name, level, school):
        self.name = name
        self.school = school
        self.level = max(self.level, int(level))

    def add_info(self, timestamp, is_login, level):
        heapq.heappush(self.log_info, (timestamp, is_login))
        self.level = max(self.level, int(level))

    def deal_login(self):
        cur = False
        last = -1
        for timestamp, is_login in heapq.nsmallest(10000, self.log_info):
            if cur == is_login:
                print('error avatar log info:', self.gbid, self.open_id, timestamp, is_login)

            day = utils.get_day_by_timestamp(timestamp)
            self.days.add(day)
            if not is_login and last != -1:
                for i in range(last, day + 1):
                    self.days.add(i)

            last = day
            cur = is_login

    def get_avatar_info(self):
        first = min(self.days)
        last = max(self.days)
        day_27 = 27 in self.days
        day_28 = 28 in self.days
        sex = utils.get_sex_dict().get(self.gbid)
        if sex == '2':
            sex = '女'
        else:
            sex = '男'
        return f'{self.gbid}\',{self.name},{self.open_id}\',{self.level},{self.school},{sex},{first},{last},{day_27},{day_28}'


class ParseAll(object):
    def __init__(self, filename):
        self.gbid_dic = {}
        self.parse(filename)

    def parse(self, filename):
        with utils.utf8_open(filename, encoding='utf-8') as fr:
            for line in fr:
                lo = LogOne.get_log_from_line(line)
                if lo.gbid in self.gbid_dic:
                    self.gbid_dic[lo.gbid]
                else:
                    self.gbid_dic[lo.gbid] = AvatarVal(lo.gbid, lo.account)

                if lo.IS_LOGIN:
                    self.gbid_dic[lo.gbid].update(lo.name, lo.level, lo.school)

                self.gbid_dic[lo.gbid].add_info(lo.timestamp, lo.IS_LOGIN, lo.level)

    def output(self, filename):
        out_name = utils.get_out_name('out', filename)
        with utils.utf8_open(out_name, 'w', encoding='utf-8') as fw:
            for val in self.gbid_dic.values():
                val.deal_login()
                fw.write(val.get_avatar_info() + '\n')



if __name__ == '__main__':
    fname = Filter.Filter.filter_login_log()

    filt = Filter.Filter(fname, None)
    tmp_log_name = filt.filter_out()
    pa = ParseAll(tmp_log_name)
    pa.output('all_avatar_info.csv')