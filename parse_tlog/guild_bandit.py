import Filter
import LogOne
import const
import os
import utils


class ActDays(object):

    def __init__(self, filename):
        self.filename = filename
        self.days = {}

    def parse(self):
        print(f'self.filename:{self.filename}')
        with utils.utf8_open(self.filename, encoding='utf-8') as fr:
            for line in fr:
                lo = LogOne.RoundFlow.get_log_obj_from_line(line)
                self.days.setdefault(lo.get_day(), {})
                day_dict = self.days[lo.get_day()]
                day_dict.setdefault(lo.gbid, [])
                day_dict[lo.gbid].append(lo)

    def out_as_csv(self, csv_name):
        dirname = utils.get_dir('out')
        full_csv_name = os.path.join(dirname, csv_name)
        days_list = list(self.days.keys())
        days_list.sort()
        with utils.utf8_open(full_csv_name, 'w') as fw:
            days_str = ','.join(map(str, days_list))
            fw.write(days_str + '\n')

            avatar_count = ','.join(map(lambda day: str(len(self.days[day])), days_list))
            fw.write(avatar_count + '\n')

            def sum_times(day_dict):
                return sum(map(len, day_dict.values()))

            times = ','.join(map(lambda day: str(sum_times(self.days[day])), days_list))
            fw.write(times + '\n')


def parse_file(filename, outname):
    ad = ActDays(filename)
    ad.parse()
    ad.out_as_csv(outname)


def parse_by_act(filt, act_id):
    fname = filt.filter_by_act(act_id)
    f = Filter.Filter(fname, LogOne.RoundFlow)
    fname = f.filter_inner()
    parse_file(fname, '{}.{}.csv'.format(act_id, 'inner'))

    fname = f.filter_out()
    parse_file(fname, '{}.{}.csv'.format(act_id, 'outter'))


if __name__ == '__main__':
    # whole_log = r'E:\shLog\tlog\xzj.log.LOG_GUILD_BANDIT.log'
    print(1)
    fname = utils.filter_from_origin('RoundFlow')
    print(2)
    f = Filter.Filter(fname, LogOne.RoundFlow)
    print(3)
    # parse_by_act(f, 9)
    print(4)
    fname = f.filter_by_act(20)
    print(5)
    with utils.utf8_open(fname, encoding='utf-8') as fr:
        for line in fr:
            lo = LogOne.RoundFlow.get_log_obj_from_line(line)
            if int(lo.round_time) > 1800:
                print(lo.result)


    # parse_by_act(f, 32000004)
    # f = Filter.Filter(whole_log, filter_inner_name, filter_out_name)
    # f.filter_tlog(r'E:\shLog\tlog\xzj.log', 'LOG_VITALITY')
    # f.filter_guild_bandit()

