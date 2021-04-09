import utils
import const
import LogOne
import log_one_utils
import csv_output


def bandit_boss():
    fname = log_one_utils.filter_resource_flow_by_src(65)
    days = {}
    with utils.utf8_open(fname) as fr:
        for line in fr:
            lo = LogOne.get_log_from_line(line)
            if lo.count != 200:
                continue

            days.setdefault(lo.day, set())
            days[lo.day].add(lo.unique_key())

    csv = csv_output.CSVOutPut()
    csv.set(0, 0, '日期')
    csv.set(1, 0, '人数')
    day_list = list(days.keys())
    day_list.sort()
    for idx, day in enumerate(day_list):
        csv.set(0, idx + 1, day)
        csv.set(1, idx + 1, len(days[day]))

    fw_name = utils.get_out_name('out', 'bandit_boss.csv')
    csv.output(fw_name)


if __name__ == '__main__':
    bandit_boss()
