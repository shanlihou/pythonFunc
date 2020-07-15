# coding=utf-8
import csv
import pickle
import os
import time
import StatisticsBase


def get_gbid_dic(csv_name):
    gbid_dic = {}

    with open(csv_name, 'r') as fr:
        reader = csv.DictReader(fr)
        for row in reader:
            gbid = int(row['gbId'].replace('\t', ''))
            account = row['account']
            gbid_dic[gbid] = account

    print(gbid_dic)
    print(len(gbid_dic))
    pickle.dump(gbid_dic, open('gbid_dic', 'wb'))


def get_filter_accounts(accounts_name):
    account_set = set()
    with open(accounts_name) as fr:
        for line in fr:
            account = line.split('\t')[0]
            account_set.add(account)

    pickle.dump(account_set, open('account_set', 'wb'))


class LoginOnce(object):
    def __init__(self, row_data):
        self.gbid = int(row_data['gbId'])
        self.time_st = time.localtime(int(row_data['timestamp']))
        self.account = row_data['account'].strip()

    def get_day(self):
        return self.time_st.tm_mday

    def __str__(self):
        return ', '.join(['{}:{}'.format(k, v) for k, v in self.__dict__.items()])


class OneDay(object):
    def __init__(self, day):
        self.day = day
        self.accounts = {}
        self.new_accounts = set()
        self.next_stay = {}

    def add_once(self, log_one: LoginOnce):
        self.accounts[log_one.account] = log_one

    def add_newer(self, account):
        self.new_accounts.add(account)

    def accounts_num(self):
        return str(len(self.accounts))

    def newer(self):
        return str(len(self.new_accounts))

    def get_next_stay(self, next_num):
        return str(self.next_stay.get(next_num, 0))

    def get_next_2_stay(self):
        return str(self.next_stay.get(2, 0))

    def process_next_day_stay(self, sta, delay):
        next_day = self.day + delay
        od = sta.get_od(next_day)
        if not od:
            return

        num = 0
        for account in od.accounts:
            if account in self.new_accounts:
                num += 1

        od.next_stay[delay] = num


class Statistics(StatisticsBase.StatisticsBase):
    def __init__(self, filename):
        super(Statistics, self).__init__(filename)
        self.has_login_accounts = set()

    def init_data(self):
        for row in self.reader:
            if row['isOnline'].strip() != 'True':
                continue

            lo = LoginOnce(row)
            self.add_login_once(lo)

        return self

    def add_login_once(self, log_one: LoginOnce):
        day = log_one.get_day()
        self.days.setdefault(day, OneDay(day))
        od = self.days[day]
        od.add_once(log_one)
        if log_one.account not in self.has_login_accounts:
            self.has_login_accounts.add(log_one.account)
            od.add_newer(log_one.account)

    def get_od(self, day):
        return self.days.get(day)

    def process(self):
        for day, od in self.days.items():
            next_day = day + 1
            if next_day in self.days:
                for i in range(6):
                    od.process_next_day_stay(self, i)

        return self

    def get_headers(self):
        return ','.join(map(lambda x: 'day{}'.format(x), self.days.keys()))

    def get_infos(self, func, *args):
        return ','.join(map(lambda x: getattr(x, func)(*args), self.days.values()))

    def dump(self, outname):
        datas = [
            self.get_headers(),
            self.get_infos('accounts_num'),
            self.get_infos('newer'),
            self.get_infos('get_next_stay', 1),
            self.get_infos('get_next_stay', 2),
            self.get_infos('get_next_stay', 3),
            self.get_infos('get_next_stay', 4),
            self.get_infos('get_next_stay', 5),
            self.get_infos('get_next_stay', 6),
        ]

        with open(outname, 'w') as fw:
            fw.write('\n'.join(datas))

        return self


class AccountFilter(object):
    def __init__(self):
        self.filter_set = pickle.load(open('filter_set', 'rb'))

    def get_csv_name(self, log_id):
        return 'E:\\shLog\\log_{}.csv'.format(log_id)

    def export(self, log_id):
        csv_name = self.get_csv_name(log_id)
        ret_name = csv_name + '.new.csv'
        with open(csv_name, 'r', encoding='utf-8') as fr:
            reader = csv.DictReader(fr)

            fw = open(ret_name, 'w')
            writer = csv.DictWriter(fw, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in reader:
                gbid = int(row['gbId'])
                if gbid in self.filter_set:
                    continue

                writer.writerow(dict(row))

        return ret_name

    def delete_space_line(self, filename):
        new_name = filename + '.new'
        with open(filename) as fr:
            fw = open(new_name, 'w')
            for line in fr:
                if not line.strip():
                    continue

                fw.write(line)
            fw.close()

        os.system('move /y {} {}'.format(new_name, filename))

    def filter_once(self, log_id):
        ret_name = self.export(log_id)
        self.delete_space_line(ret_name)

    def calc_stay(self, filename, outname):
        Statistics(filename)\
            .init_data()\
            .process()\
            .dump(outname)

    def test(self):
        # filter_once(70)
        self.calc_stay(r'e:\shLog\log_70.csv.new.csv', 'e:\\shLog\\out.csv')
        self.calc_stay(r'e:\shLog\log_70.csv', 'e:\\shLog\\out1.csv')


def main():
    # get_gbid_dic(r'E:\shLog\log_70.csv')
    AccountFilter().test()


if __name__ == '__main__':
    main()
