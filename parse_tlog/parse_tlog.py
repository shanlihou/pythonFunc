# coding = utf-8
import time


UNIQUE_BY_ACCOUNT = True


def get_time_stamp(time_str):
    time_st = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    return time.mktime(time_st)


def get_day(time_str):
    time_st = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    return time_st.tm_mday


class Filter(object):
    @classmethod
    
    @classmethod
    def filter_outside(cls, filename):
        with open(filename, encoding='utf-8') as fr:
            


class LogOne(object):
    def __init__(self, log_type, server_id, time_str, app_id, plant_id,
                 area_id, zone_id, open_id, client_ver, sec_report_data,
                 sys_software, *args):
        self.gbid = args[6]
        self.name = args[7]
        self.time_str = time_str
        self.timestamp = get_time_stamp(time_str)
        self.account = open_id
        self.day = get_day(time_str)

    def get_day(self):
        return self.day

    def unique_key(self):
        if UNIQUE_BY_ACCOUNT:
            return self.account
        else:
            return self.gbid


class DaysManager(object):
    def __init__(self):
        self.days_dict = {}

    def add_one(self, log_one: LogOne):
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

    def output(self, day_index):
        days = list(self.days_dict.keys())
        if day_index >= len(days):
            return

        day = days[day_index]
        ret_list = []
        for idx in range(day_index + 1, len(days)):
            cur = days[idx]
            ret_list.append({
                'day': cur,
                'idx': idx,
                'count': self.get_stay_num(day, cur)
            })

        return ret_list

    def debug(self):
        for k, v in self.days_dict.items():
            print(k, len(v))


def filter_tlog(filename, filter_str):
    fw = open(filename + '.{}.log'.format(filter_str), 'w')
    with open(filename, encoding='utf-8') as fr:
        for line in fr:
            if line.startswith(filter_str):
                fw.write(line)


def parse_tlog(filename):
    dm = DaysManager()
    with open(filename) as fr:
        for line in fr:
            tup = line.strip().split('|')
            log_one = LogOne(*tup)
            dm.add_one(log_one)

    out = dm.output(1)
    print(out)
#     dm.debug()


def main():
    #     filter_tlog(r'E:\shLog\xzj.log', 'SecLogin')
    #     ret = get_time_stamp('2020-11-13 19:26:20')
    #     print(ret)
#     parse_tlog(r'E:\shLog\tlog\xzj.log.SecLogin.log')
    Filter.filter_outside(r'E:\shLog\tlog\xzj.log.SecLogin.log')

if __name__ == '__main__':
    main()
