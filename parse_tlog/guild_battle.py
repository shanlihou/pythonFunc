import Filter
import LogOne
import const
import os
import utils


class GuildBattle(object):
    def __init__(self, filename):
        self.filename = filename
        self.days = {}

    def parse(self):
        with utils.utf8_open(self.filename) as fr:
            for line in fr:
                ls = LogOne.LogSys.get_log_obj_from_line(line)
                if not ls:
                    print(line)
                    continue

                self.days.setdefault(ls.get_day(), {})
                day_dict = self.days[ls.get_day()]
                day_dict.setdefault(ls.unique_key(), [])
                day_dict[ls.unique_key()].append(ls)

    def out_as_csv(self, csv_name):
        dirname = utils.get_dir('out')
        full_csv_name = os.path.join(dirname, csv_name)
        days_list = list(self.days.keys())
        days_list.sort()
        print(days_list)
        with utils.utf8_open(full_csv_name, 'w') as fw:
            days_str = ','.join(map(str, days_list))
            fw.write(days_str + '\n')

            avatar_count = ','.join(map(lambda day: str(len(self.days[day])), days_list))
            fw.write(avatar_count + '\n')

            def sum_times(day_dict):
                return sum(map(len, day_dict.values()))


            times = ','.join(map(lambda day: str(sum_times(self.days[day])), days_list))
            # fw.write(times + '\n')


if __name__ == '__main__':
    fname = Filter.Filter.filter_sys_log('LOG_GUILD_BATTLE_STATISTICS')
    print(fname)

    f = Filter.Filter(fname, LogOne.LogSys)

    fname = f.filter_inner()
    gb = GuildBattle(fname)
    gb.parse()
    gb.out_as_csv('guild_battle_inner.csv')

    fname = f.filter_out_first()
    gb = GuildBattle(fname)
    gb.parse()
    gb.out_as_csv('guild_battle_out_first.csv')

    fname = f.filter_out_second()
    gb = GuildBattle(fname)
    gb.parse()
    gb.out_as_csv('guild_battle_out_second.csv')