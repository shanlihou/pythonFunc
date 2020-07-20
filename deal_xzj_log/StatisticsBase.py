import csv
import time
import utils
import pickle
import functools
from matplotlib.testing.jpl_units import day


class AvatarBase(object):
    def __init__(self):
        self.row_list = []

    @staticmethod
    def key(row_dict):
        return ''

    def for_print_row_list(self):
        return [{
            'gbId': row['gbId'].strip(),
            'logType': row['logType'].strip(),
            'timestamp': row['timestamp'].strip()
        }for row in self.row_list]

    def add_row(self, row_dict):
        self.row_list.append(row_dict)
        self.process_one(row_dict)

    def process_one(self, row):
        pass


class DayBase(object):
    def __init__(self, owner):
        self.info_dict = {}
        self.account_set = set()
        self.owner = owner
        self.login_account_num = 0

    def avatar_nums(self):
        return str(len(self.info_dict))

    def account_rate(self):
        if self.login_account_num:
            return str(len(self.account_set) / self.login_account_num)
        else:
            return 0

    def reduce_num(self, func):
        return str(functools.reduce(lambda x, y: (x if isinstance(x, int) else func(x)) + func(y), self.info_dict.values()))

    def add_row(self, row_dict, avatar_class):
        key = avatar_class.key(row_dict)

        if key not in self.info_dict:
            gbid = int(key)
            account = self.owner.get_account(gbid)
            if account is not None:
                self.account_set.add(account)

            self.info_dict[key] = avatar_class()

        ai = self.info_dict[key]
        ai.add_row(row_dict)

    def get_account_num(self):
        return str(len(self.account_set))


class StatisticsBase(object):
    DAY_CLASS = DayBase
    AVATAR_CLASS = AvatarBase
    COL_HEADER = []

    def __init__(self, filename):
        self.days = {}
        self.day_account_dic = {}
        self.gbid_dic = pickle.load(open('gbid_dic', 'rb'))
        fr = open(filename, 'r')
        self.reader = csv.DictReader(fr)

    def filter(self, row_dict):
        return True

    def set_da_dic(self, da_dic):
        self.day_account_dic = da_dic
        for day, val in self.days.items():
            account_num = da_dic.get(day, 0)
            val.login_account_num = account_num

        return self

    def get_datas(self):
        return []

    def dump(self, outname):
        datas = self.get_datas()
        datas = utils.add_col_header(self.COL_HEADER, datas)
        with open(outname, 'w') as fw:
            fw.write('\n'.join(datas))

        return self

    def get_account(self, gbid):
        return self.gbid_dic.get(gbid)

    def process_data(self):
        for row in self.reader:
            if not self.filter(row):
                continue

            self.process_one(row)

        return self

    @staticmethod
    def get_day(row_dict):
        timestamp = float(row_dict['timestamp'])
        time_st = time.localtime(timestamp // 1000)
        return time_st.tm_mday

    def process_one(self, row_dict):
        day = self.get_day(row_dict)
        self.days.setdefault(day, self.DAY_CLASS(self))
        day_obj = self.days[day]
        day_obj.add_row(row_dict, self.AVATAR_CLASS)

    def get_headers(self):
        return ','.join(map(lambda x: 'day{}'.format(x), self.days.keys()))

    def get_infos(self, func, *args):
        return ','.join(map(lambda x: getattr(x, func)(*args), self.days.values()))
