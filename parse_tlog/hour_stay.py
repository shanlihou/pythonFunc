import Filter
import const
import LogOne
import csv_output
import utils
import os


class HourStay(object):
    def __init__(self, filename):
        self.filename = filename
        self.gbid_dic = {}
        self.days = {}

    def parse(self):
        with utils.utf8_open(self.filename, encoding='utf-8') as fr:
            for line in fr:
                lo = LogOne.get_log_from_line(line)
                uk = lo.unique_key()
                if uk not in self.gbid_dic:
                    if not lo.IS_LOGIN:
                        print('error first not login')
                        continue

                    self.gbid_dic[uk] = lo
                    self.days.setdefault(lo.get_day(), {})
                    self.days[lo.get_day()][uk] = lo
                else:
                    if lo.IS_LOGIN:
                        continue

                    self.gbid_dic[uk].add_log_out_time(lo.timestamp)

    def out_as_csv(self, filename):
        print(len(self.gbid_dic))
        newdir = utils.get_dir('out')
        out_name = os.path.join(newdir, filename)

        days_list = list(self.days.keys())
        days_list.sort()
        csv = csv_output.CSVOutPut()
        for i, day in enumerate(days_list):
            day_dict = self.days[day]
            dur_dict = {}
            csv.set(0, i * 2, day)
            csv.set(0, i * 2 + 1, day)
            for uk, lo in day_dict.items():
                dur_dict[lo.get_duration()] = dur_dict.get(lo.get_duration(), 0) + 1

            dur_list = list(dur_dict.keys())
            dur_list.sort()
            for j in range(121):
                csv.set(j + 1, i * 2, j)
                csv.set(j + 1, i * 2 + 1, dur_dict.get(j, 0))

            # for j, dur in enumerate(dur_list):
            #     count = dur_dict[dur]
            #     csv.set(j + 1, i * 2, dur)
            #     csv.set(j + 1, i * 2 + 1, count)

        csv.output(out_name)


if __name__ == '__main__':
    fname = Filter.Filter.filter_login_log(const.ORI_FILE_NAME)
    print(fname)

    f = Filter.Filter(fname, None)

    fname = f.filter_inner()
    hs = HourStay(fname)
    hs.parse()
    hs.out_as_csv('hour_inner.csv')

    fname = f.filter_out()
    hs = HourStay(fname)
    hs.parse()
    hs.out_as_csv('hour_out_second.csv')