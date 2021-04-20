# coding = utf-8
import time
import os
import LogOne
import Filter
import utils
import functools
import const
import csv_output
import pickle
import log_one_utils


class Avatar(object):
    def __init__(self, open_id, day, create_from):
        self.open_id = open_id
        self.queue = []
        self.days = set()
        self.days.add(day)
        self.create_from = create_from
        self.battle_point = 0
        self.channel = None
        self.level = 0

    def __str__(self):
        return f'create_from:{self.create_from}, open_id:{self.open_id} days:{self.days}'

    def add_log(self, lo):
        self.level = max(self.level, int(lo.level))
        self.battle_point = max(self.battle_point, int(lo.battle_point))
        _last = self.queue[-1]
        cur = (lo.FILTER_STR == 'PlayerLogin', lo.get_day())
        if cur[0] != _last[0] and _last[0]:
            for day in range(_last[1], cur[1] + 1):
                self.days.add(day)

    def add_battle_point(self, battle_point):
        self.battle_point = max(self.battle_point, int(battle_point))

    def add_channel(self, channel):
        self.channel = channel

    def add_level(self, level):
        self.level = max(self.level, int(level))

    def add_day(self, day):
        self.days.add(day)

    def add_school(self, school):
        self.school = school

    def is_stay_by(self, n): # 是否n流 1是次留(连续登陆两天),2是3流(连续登陆3天)
        min_day = min(self.days)
        for i in range(n):
            target_day = min_day + i + 1
            if target_day not in self.days:
                return False

        return True



class ResultDay(object):

    def __init__(self, day):
        self.day = day
        self.stay_dict = {}

    def add_new(self, new):
        self.new = new

    def add_stay(self, day, stay):
        self.stay_dict[day] = stay

    def get_row(self, row_idx):
        if row_idx == 0:
            return str(self.day)
        elif row_idx == 1:
            return str(self.new)
        else:
            ret = self.stay_dict.get(row_idx - 1 + self.day, 0)
            return str(ret) if ret else ''

    def get_stay_by_day_index(self, day_idx):
        return self.new, self.stay_dict.get(self.day + day_idx, 0)


class DaysManager(object):

    def __init__(self):
        self.days_dict = {}
        self.uk_dict = {}  # type: dict[int, LogOne.LogOne]

    def get_day_uk_dict(self):
        ret_dict = {}
        for uk, lo in self.uk_dict.items():
            for day in lo.day_set:
                ret_dict.setdefault(day, set())
                ret_dict[day].add(uk)

        return ret_dict

    def add_one(self, log_one: LogOne.LogOne):
        day = log_one.get_day()
        uk = log_one.unique_key()

        if uk in self.uk_dict:
            self.uk_dict[uk].add_day(day, log_one.IS_LOGIN, log_one.timestamp)
        elif isinstance(log_one, LogOne.LogOne):
            self.uk_dict[uk] = log_one
        else:
            print(f'invalid log_one:{log_one}')
            return

        self.days_dict.setdefault(day, {})
        self.days_dict[day].setdefault(uk, log_one)

    def get_stay_num(self, day1, day2):
        dict1 = self.days_dict[day1]
        dict2 = self.days_dict[day2]
        sum = 0
        for unique_key in dict2:
            if unique_key in dict1:
                sum += 1

        return sum

    def output(self):
        days = list(self.days_dict.keys())
        days.sort()
        max_day = days[-1]
        old_avatar_set = set()
        rds = []
        for day in days:
            day_dict = self.days_dict[day]
            new_count = 0
            new_set = set()
            rd = ResultDay(day)
            for unique_key in day_dict:
                if unique_key not in old_avatar_set:
                    new_count += 1
                    old_avatar_set.add(unique_key)
                    new_set.add(unique_key)

            rd.add_new(len(new_set))

            for i in range(const.FIRST_DAY + 1, const.FINAL_DAY + 1):
                calc_day = i
                stay_num = 0
                for uk in new_set:
                    lo = self.uk_dict[uk]
                    if lo.is_stay_by_dur(i):
                        stay_num += 1

                rd.add_stay(calc_day, stay_num)

            rds.append(rd)

        return rds

    def out_as_csv(self, filename):
        rds = self.output()
        with utils.utf8_open(filename, 'w') as fw:
            row = 0
            while 1:
                strs = [rd.get_row(row) for rd in rds]
                if not any(strs):
                    break

                fw.write(','.join(strs) + '\n')

                row += 1

        with utils.utf8_open('{}.full.csv'.format(filename), 'w') as fw:
            day_idx = 1
            line1 = []
            line2 = []
            while 1:
                tmp = [rd.get_stay_by_day_index(day_idx) for rd in rds]
                tmp = functools.reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]), tmp)
                if not tmp[1]:
                    break

                line1.append(tmp[0])
                line2.append(tmp[1])
                day_idx += 1

            fw.write(','.join(map(str, line1)) + '\n')
            fw.write(','.join(map(str, line2)) + '\n')

    def out_school_csv(self, filename):
        csv = csv_output.CSVOutPut()

        schools = set(utils.get_gbid_school_dict().values())
        school_dict = {}
        for uk, lo in self.uk_dict.items():
            school_dict.setdefault(lo.school, {})
            school_dict[lo.school][uk] = lo

        for index, school in enumerate(schools):
            csv.set(0, index, school)
            csv.set(1, index, len(school_dict[school]))

            stay_1 = 0
            for lo in school_dict[school].values():
                if lo.is_stay_by_dur(1):
                    stay_1 += 1

            stay_2 = 0
            for lo in school_dict[school].values():
                if lo.is_stay_by_dur(2):
                    stay_2 += 1

            csv.set(2, index, stay_1)
            csv.set(3, index, stay_2)

        for k, v in school_dict.items():
            print(k, len(v))
        csv.output(filename)

    def debug(self):
        for k, v in self.days_dict.items():
            print(k, len(v))


def get_dm(filename):
    dm = DaysManager()
    print(filename)
    with utils.utf8_open(filename, encoding='utf-8') as fr:
        for line in fr:
            log_one = LogOne.get_log_from_line(line)
            dm.add_one(log_one)
    print(f'len:{len(dm.uk_dict)}')
    return dm


def get_stay_list(dic, isFilterByFrist=False): # 从字典中获取各个留存数据
    """
    dic: type dict[int, Avatar]
    """
    day_num = utils.get_whole_days()
    ret_list = [0] * day_num
    for avatar_val in dic.values():
        if isFilterByFrist and const.FIRST_DAY not in avatar_val.days:
            continue

        ret_list[0] += 1
        for i in range(1, day_num):
            if avatar_val.is_stay_by(i):
                ret_list[i] += 1

    return ret_list


def get_avatar_dic(): # 获得一个dic,里面每个玩家包含有自己登陆的天数
    avatar_dic = {}
    out_name = utils.get_out_name('tmp', 'avatar_days_dict')

    if os.path.exists(out_name):
        avatar_dic = pickle.load(open(out_name, 'rb'))
    else:
        fname = log_one_utils.filter_by_log_one_all()
        with utils.utf8_open(fname) as fr:
            for line in fr:
                lo = LogOne.get_log_from_line(line)
                if not lo:
                    continue

                if not (const.FIRST_DAY <= lo.day <= const.FINAL_DAY):
                    continue

                uk = lo.unique_key() # 获取open_id
                if uk not in avatar_dic:
                    avatar_dic[uk] = Avatar(uk, lo.day, lo.FILTER_STR)

                avatar_val = avatar_dic[uk]
                avatar_val.add_day(lo.day)
                if lo.FILTER_STR == 'SecLogin':
                    avatar_val.add_school(lo.school)
                elif lo.FILTER_STR == 'PlayerLogin' or lo.FILTER_STR == 'PlayerLogout':
                    avatar_val.add_level(lo.level)
                    avatar_val.add_battle_point(lo.battle_point)
                    avatar_val.add_channel(lo.login_channel)


        pickle.dump(avatar_dic, open(out_name, 'wb'))
    return avatar_dic

def parse_tlog():
    avatar_dic = get_avatar_dic()
    school_dic = {}
    for uk, avatar_val in avatar_dic.items():
        if not hasattr(avatar_val, 'school'):
            print('error not has school:', avatar_val.open_id, avatar_val.create_from)
            continue
        school_dic.setdefault(avatar_val.school, {})
        school_dic[avatar_val.school][uk] = avatar_val

    csv = csv_output.CSVOutPut()
    schools = list(school_dic.keys())
    # 总的次留
    ret_list = get_stay_list(avatar_dic, True)
    for ii, stay in enumerate(ret_list):
        csv.set(ii + 1, 1, stay)

    # 根据职业的次留
    for index, school in enumerate(schools):
        csv.set(0, index + 2, school)
        stay_list = get_stay_list(school_dic[school], True)
        for _index, stay in enumerate(stay_list):
            csv.set(_index + 1, index + 2, stay)

    for i in range(utils.get_whole_days()):
        csv.set(i + 1, 0, f'{i + 1}留')

    out_name = utils.get_out_name('out', 'school.csv')
    csv.output(out_name)


def get_avatar_login_5_days():
    # 获得登陆五天的玩家的相关信息
    avatar_dic = get_avatar_dic()
    csv = csv_output.CSVOutPut()
    csv.set(0, 0, 'OPENID')
    csv.set(0, 1, '等级')
    csv.set(0, 2, '战力')
    csv.set(0, 3, '渠道号')
    csv.set(0, 4, '登陆天')
    idx = 1
    for avatar_val in avatar_dic.values():
        if len(avatar_val.days) < 5:
            continue

        csv.set(idx, 0, avatar_val.open_id)
        csv.set(idx, 1, avatar_val.level)
        csv.set(idx, 2, avatar_val.battle_point)
        csv.set(idx, 3, avatar_val.channel)
        csv.set(idx, 4, '|'.join(map(str, (avatar_val.days))))
        idx += 1

    out_name = utils.get_out_name('out', 'login_5_days.csv')
    csv.output(out_name)

    # uk = str(5860530770676540844)
    # if uk in dm.uk_dict:
    #     lo =dm.uk_dict[uk]
    #     print(lo.day_set)
    #     print(lo.school)
    #     print(lo.is_stay_by_dur(3))
#     dm.debug()

def get_openid_info_by_txt():
    # 根据openids.txt提供特定玩家信息
    avatar_dic = get_avatar_dic()
    csv = csv_output.CSVOutPut()
    csv.set(0, 0, 'openid')
    csv.set(0, 1, '次留')
    csv.set(0, 2, '三留')
    csv.set(0, 3, '七留')
    csv.set(0, 4, '首周登录天数')
    csv.set(0, 5, '战力')
    csv.set(0, 6, '等级')
    csv.set(0, 7, '哪一天登陆')
    idx = 0
    with utils.utf8_open(const.OPEN_IDS_TXT) as fr:
        for line in fr:
            idx += 1
            line = line.strip()
            if line in avatar_dic:
                a = avatar_dic[line]
                csv.set(idx, 0, line)
                csv.set(idx, 1, 1 if a.is_stay_by(1) else 0)
                csv.set(idx, 2, 1 if a.is_stay_by(2) else 0)
                csv.set(idx, 3, 1 if a.is_stay_by(6) else 0)
                csv.set(idx, 4, len(a.days))
                csv.set(idx, 5, a.battle_point)
                csv.set(idx, 6, a.level)
                csv.set(idx, 7, '|'.join(map(str, a.days)))

            else:
                print(line)
    out_name = utils.get_out_name('out', 'avatar_info_by_open_id_txt.csv')
    csv.output(out_name)


def main():
    # fname = Filter.Filter.filter_login_log()

    # filt = Filter.Filter(fname, None)

    # # --------------------------------------
    # tmp_log_name = filt.filter_inner()
    # out_name = utils.get_out_name('out', 'daily_inner.csv')
    # parse_tlog(tmp_log_name, out_name)

    # # --------------------------------------
    # tmp_log_name = filt.filter_out()
    # out_name = utils.get_out_name('out', 'daily_outer.csv')
    # parse_tlog(tmp_log_name, out_name)
    get_openid_info_by_txt()


if __name__ == '__main__':
    main()
