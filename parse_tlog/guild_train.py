import Filter
import utils
import LogOne
import csv_output
import os


class GuildTrain(object):
    def __init__(self, filename):
        self.filename = filename
        self.uk_dict = {}
        self.uk_day_dict = {}

    def parse(self):
        with open(self.filename) as fr:
            for line in fr:
                lo = LogOne.get_log_from_line(line)
                day = lo.get_day()
                uk = lo.unique_key()
                if lo.gbid not in utils.get_out_first_day_score_dict()[day]:
                    continue

                self.uk_dict[uk] = self.uk_dict.get(uk, 0) + lo.score
                self.uk_day_dict.setdefault(uk, {})
                self.uk_day_dict[uk][day] = self.uk_dict[uk]

    def out_as_csv(self, filename):
        out_dir = utils.get_dir('out')
        out_name = os.path.join(out_dir, filename)

        day_list = list(self.days.keys())
        csv = csv_output.CSVOutPut()
        for index, day in enumerate(day_list):
            day_dict = self.days[day]
            csv.set(0, index, day)

            sum_score = sum(day_dict.values())

            csv.set(1, index, sum_score / len(day_dict))
            csv.set(2, index, sum_score)
            csv.set(3, index, len(day_dict))

        csv.output(out_name)


if __name__ == '__main__':
    fname = Filter.Filter.filter_guild_train()
    f = Filter.Filter(fname, None)
    fname = f.filter_out_first()

    gt = GuildTrain(fname)
    gt.parse()
    gt.out_as_csv('guild_train_out_first.csv')