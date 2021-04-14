import const
import utils
import Filter
import parse_tlog
import log_one_utils
import LogOne
import csv_output


class Avatar(object):
    def __init__(self, open_id, level, battle_point, lo):
        self.open_id = open_id
        self.level = int(level)
        self.battle_point = int(battle_point)
        self.queue = []
        self.queue.append((lo.FILTER_STR == 'PlayerLogin', lo.get_day()))
        self.days = set()
        self.days.add(lo.day)
        self.login_channel = lo.login_channel

    def add_log(self, lo):
        self.level = max(self.level, int(lo.level))
        self.battle_point = max(self.battle_point, int(lo.battle_point))
        _last = self.queue[-1]
        cur = (lo.FILTER_STR == 'PlayerLogin', lo.get_day())
        if cur[0] != _last[0] and _last[0]:
            for day in range(_last[1], cur[1] + 1):
                self.days.add(day)


def parse_today_not_login():
    fname = log_one_utils.get_login_out_log_new()
    avatar_dic = {}
    with utils.utf8_open(fname) as fr:
        for line in fr:
            lo = LogOne.get_log_from_line(line)
            if not (const.FIRST_DAY <= lo.day <= const.FINAL_DAY):
                continue
            uk = lo.unique_key()
            if uk in avatar_dic:
                avatar_dic[uk].add_log(lo)
            else:
                avatar_dic[uk] = Avatar(uk, lo.level, lo.battle_point, lo)

    print(len(avatar_dic))
    csv = csv_output.CSVOutPut()
    csv.set(0, 0, 'GOPENID')
    csv.set(0, 1, '等级')
    csv.set(0, 2, '战力')
    csv.set(0, 3, '渠道号')
    idx = 1
    for av in avatar_dic.values():
        if 22 <= av.level <= 35 and (const.FINAL_DAY not in av.days):
            csv.set(idx, 0, f'{av.open_id}')
            csv.set(idx, 1, av.level)
            csv.set(idx, 2, av.battle_point)
            csv.set(idx, 3, av.login_channel)
            idx += 1
        
    fname = utils.get_out_name('out', 'today_not_login.csv')
    csv.output(fname)



if __name__ == '__main__':
    parse_today_not_login()