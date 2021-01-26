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
                if uk not in utils.get_out_first_day_score_dict()[day]:
                    continue

                self.uk_dict[uk] = self.uk_dict.get(uk, 0) + lo.score
                self.uk_day_dict.setdefault(uk, {})
                self.uk_day_dict[uk][day] = self.uk_dict[uk]

    def out_as_csv(self, filename):
        out_dir = utils.get_dir('out')
        out_name = os.path.join(out_dir, filename)

        csv = csv_output.CSVOutPut()

        fname = Filter.Filter.filter_login_log(const.ORI_FILE_NAME)
        dm = parse_tlog.get_dm(fname)
        day_uk_dict = dm.get_day_uk_dict()
        day_list = list(day_uk_dict.keys())
        day_list.sort()
        day_score_dict = utils.get_out_first_day_score_dict()
        for index, day in enumerate(day_list):
            csv.set(0, index, day)

            uk_set = day_uk_dict[day]
            sum_score = 0
            avatar_num = 0

            for uk in uk_set:
                if uk not in day_score_dict[day]:
                    continue

                score = self.get_score_by_day(uk, day)
                sum_score += score
                avatar_num += 1

            csv.set(1, index, sum_score / avatar_num)
            csv.set(2, index, sum_score)
            csv.set(3, index, avatar_num)


        csv.output(out_name)


if __name__ == '__main__':
    fname = utils.filter_tlog(const.ORI_FILE_NAME, 'LOG_GUILD_TRAIN')
    f = Filter.Filter(fname, None)
    fname = f.filter_out()

    gt = GuildTrain(fname)
    gt.parse()
    gt.out_as_csv('guild_train_out_first.csv')