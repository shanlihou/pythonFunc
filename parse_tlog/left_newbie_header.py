# coding:utf-8
# 新手流失玩家的表头
import utils
import const
import LogOne
import csv_output


class NewBieLeft(object):

    def __init__(self, open_id, level, login_channel, battle_point):
        self.open_id = open_id
        self.level = int(level)
        self.battle_point = int(battle_point)
        self.login_channel = login_channel
        
    def update_level(self, level, battle_point):
        if int(level) > self.level:
            self.level = int(level)
            self.battle_point = int(battle_point)


def get_header():
    dic = {}
    fname = utils.filter_from_origin('PlayerLogout')
    with utils.utf8_open(fname) as fr:
        for line in fr:
            lo = LogOne.get_log_from_line(line)
            if not lo:
                continue
            
            uk = lo.unique_key()
            if uk in dic:
                dic[uk].update_level(lo.level, lo.battle_point)
            else:
                dic[uk] = NewBieLeft(uk, lo.level, lo.login_channel, lo.battle_point)

    csv = csv_output.CSVOutPut()
    csv.set(0, 0, 'GOPENID')
    csv.set(0, 1, '等级')
    csv.set(0, 2, '战力')
    csv.set(0, 3, '渠道号')
    idx = 1
    for lo in dic.values():
        if lo.level > const.MAX_LEFT_LEVEL:
            continue

        csv.set(idx, 0, f'{lo.open_id}\'')
        csv.set(idx, 1, lo.level)
        csv.set(idx, 2, lo.battle_point)
        csv.set(idx, 3, lo.login_channel)
        idx += 1
        
    fname = utils.get_out_name('out', 'left_newbie_header.csv')
    csv.output(fname)

    
if __name__ == '__main__':
    get_header()
