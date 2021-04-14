# coding = utf-8
import time
import os
import LogOne
import Filter
import utils
import functools
import const
import csv_output


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
        self.days_dict.setdefault(day, {})
        self.days_dict[day].setdefault(log_one.unique_key(), log_one)

        if uk in self.uk_dict:
            self.uk_dict[uk].add_day(day, log_one.IS_LOGIN, log_one.timestamp)
        elif isinstance(log_one, LogOne.LogOne):
            self.uk_dict[uk] = log_one
        else:
            print(f'invalid log_one:{log_one}')

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

            for i in range(1, 8):
                calc_day = day + i
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


def parse_tlog(filename, out_name):
    dm = get_dm(filename)

    dm.out_as_csv(out_name)
    dm.out_school_csv(out_name + '.school.csv')

    # uk = str(5860530770676540844)
    # if uk in dm.uk_dict:
    #     lo =dm.uk_dict[uk]
    #     print(lo.day_set)
    #     print(lo.school)
    #     print(lo.is_stay_by_dur(3))
#     dm.debug()


def main():
    fname = Filter.Filter.filter_login_log()

    filt = Filter.Filter(fname, None)

    # --------------------------------------
    tmp_log_name = filt.filter_inner()
    out_name = utils.get_out_name('out', 'daily_inner.csv')
    parse_tlog(tmp_log_name, out_name)

    # --------------------------------------
    tmp_log_name = filt.filter_out()
    out_name = utils.get_out_name('out', 'daily_outer.csv')
    parse_tlog(tmp_log_name, out_name)


if __name__ == '__main__':
    main()
