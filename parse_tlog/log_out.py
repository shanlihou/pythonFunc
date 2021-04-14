import Filter
import const
import LogOne
import os
import utils
import csv_output


class LogOut(object):
    def __init__(self, filename):
        self.filename = filename
        self.days = {}

    def parse(self):
        with utils.utf8_open(self.filename) as fr:
            for line in fr:
                lo = LogOne.LogOut.get_log_obj_from_line(line)
                self.days.setdefault(lo.get_day(), {})
                day_dict = self.days[lo.get_day()]
                uk = lo.unique_key()
                if uk in day_dict:
                    if lo.level > day_dict[uk].level:
                        day_dict[uk] = lo
                else:
                    day_dict[uk] = lo

    def out_as_csv(self, filename):
        csv = csv_output.CSVOutPut()
        out_name = os.path.join(utils.get_dir('out'), filename)
        day_list = list(self.days.keys())
        day_list.sort()

        for index, day in enumerate(day_list):
            csv.set(0, index * 2, str(day))
            csv.set(0, index * 2 + 1, str(day))
            day_dict = self.days[day]
            levelDict = {}
            for unique_key, lo in day_dict.items():
                levelDict.setdefault(lo.level, [])
                levelDict[lo.level].append(lo)

            levelList = list(levelDict.keys())
            levelList.sort()

            for _index, level in enumerate(levelList):
                num = len(levelDict[level])
                csv.set(_index + 1, index * 2, str(level))
                csv.set(_index + 1, index * 2 + 1, str(num))

        csv.output(out_name)


if __name__ == '__main__':
    fname = utils.filter_from_origin('SecLogout')
    f = Filter.Filter(fname, LogOne.LogOut)

    fname = f.filter_inner()
    lo = LogOut(fname)
    lo.parse()
    lo.out_as_csv('log_out_inner.csv')

    fname = f.filter_out()
    lo = LogOut(fname)
    lo.parse()
    lo.out_as_csv('log_out_out_first.csv')
