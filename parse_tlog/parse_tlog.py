# coding = utf-8
import time
import os
import LogOne
import Filter
import utils
import functools
import const


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

    def add_one(self, log_one: LogOne.LogOne):
        day = log_one.get_day()
        self.days_dict.setdefault(day, {})
        self.days_dict[day].setdefault(log_one.unique_key(), log_one)

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

            stay_set = new_set
            for calc_day in range(day + 1, max_day + 1):
                day_dict = self.days_dict[calc_day]
                stay_set = set(i for i in day_dict if i in stay_set)
                rd.add_stay(calc_day, len(stay_set))

            rds.append(rd)

        return rds

    def out_as_csv(self, filename):
        rds = self.output()
        with open(filename, 'w') as fw:
            row = 0
            while 1:
                strs = [rd.get_row(row) for rd in rds]
                if not any(strs):
                    break

                fw.write(','.join(strs) + '\n')

                row += 1

        with open('{}.full.csv'.format(filename), 'w') as fw:
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

    def debug(self):
        for k, v in self.days_dict.items():
            print(k, len(v))


def parse_tlog(filename, out_name):
    dm = DaysManager()
    with open(filename) as fr:
        for line in fr:
            log_one = LogOne.LogOne.get_log_obj_from_line(line)
            dm.add_one(log_one)

    dm.out_as_csv(out_name)
#     dm.debug()


def main():
    #     filter_tlog(r'E:\shLog\xzj.log', 'SecLogin')
    #     ret = get_time_stamp('2020-11-13 19:26:20')
    #     print(ret)
    #     parse_tlog(r'E:\shLog\tlog\xzj.log.SecLogin.log')
    fname = Filter.Filter.filter_tlog(const.ORI_FILE_NAME, 'SecLogin')

    filt = Filter.Filter(fname, LogOne.LogOne)

    # --------------------------------------
    tmp_log_name = filt.filter_inner()
    out_name = utils.get_out_name('out', 'inner.csv')
    parse_tlog(tmp_log_name, out_name)

    # --------------------------------------
    tmp_log_name = filt.filter_out_first()
    out_name = utils.get_out_name('out', 'out_first.csv')
    parse_tlog(tmp_log_name, out_name)

    # --------------------------------------
    tmp_log_name = filt.filter_out_second()
    out_name = utils.get_out_name('out', 'out_second.csv')
    parse_tlog(tmp_log_name, out_name)


if __name__ == '__main__':
    main()
