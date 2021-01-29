import Filter
import utils
import LogOne
import csv_output
import os
import const
import parse_tlog


class GuildTrain(object):
    def __init__(self, filename):
        self.filename = filename
        self.uk_dict = {}
        self.uk_day_dict = {}

    def get_score_by_day(self, uk, day):
        if uk not in self.uk_day_dict:
            return 0

        day_score_list = list(self.uk_day_dict[uk].items())
        day_score_list.sort(key=lambda x: x[0])
        cur_score = 0
        for _day, score in day_score_list:
            if _day > day:
                break

            cur_score = score

        return cur_score

    def parse(self):
        with open(self.filename) as fr:
            for line in fr:
                lo = LogOne.get_log_from_line(line)
                day = lo.get_day()
                uk = lo.unique_key()

                self.uk_day_dict.setdefault(day, {})
                self.uk_day_dict[day][uk] = max(self.uk_day_dict[day].get(uk, 0), int(lo.score))

    def out_as_csv(self, filename):
        out_dir = utils.get_dir('out')
        out_name = os.path.join(out_dir, filename)

        csv = csv_output.CSVOutPut()
        index = 0
        for day, day_dict in self.uk_day_dict.items():
            sum_score = sum(day_dict.values())
            csv.set(0, index, day)

            csv.set(1, index, sum_score / len(day_dict))
            csv.set(2, index, sum_score)
            csv.set(3, index, len(day_dict))
            index += 1

        csv.output(out_name)


if __name__ == '__main__':
    fname = utils.filter_tlog(const.ORI_FILE_NAME, 'LOG_GUILD_TRAIN')
    f = Filter.Filter(fname, None)
    fname = f.filter_out()

    gt = GuildTrain(fname)
    gt.parse()
    gt.out_as_csv('guild_train_out_first.csv')