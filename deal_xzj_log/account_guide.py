# coding=utf8
import StatisticsBase
import functools


class AvatarGuide(StatisticsBase.AvatarBase):
    def __init__(self):
        super(AvatarGuide, self).__init__()
        self.try_enter_num = 0
        self.enter_success_num = 0
        self.mission_success_num = 0

    @staticmethod
    def key(row_dict):
        return row_dict['gbId'].strip()

    def process_one(self, row):
        log_type = row['logType'].strip()
        if log_type == '2':
            self.try_enter_num += 1
        elif log_type == '4':
            self.mission_success_num += 1


class DayGuide(StatisticsBase.DayBase):
    pass


class GuideInfo(StatisticsBase.StatisticsBase):
    DAY_CLASS = DayGuide
    AVATAR_CLASS = AvatarGuide
    COL_HEADER = [
        '日',
        '角色数',
        '玩家数',
        '参与度',
        '进入次数',
        '完成次数'
    ]

    def get_datas(self):
        return [
            self.get_headers(),
            self.get_infos('avatar_nums'),
            self.get_infos('get_account_num'),
            self.get_infos('account_rate'),
            self.get_infos('reduce_num', lambda x: x.try_enter_num),
            self.get_infos('reduce_num', lambda x: x.mission_success_num),
        ]


def deal_guide(da_dic):
    gi = GuideInfo('e:\\shlog\\log_59.csv.new.csv')
    gi.process_data()\
        .set_da_dic(da_dic)\
        .dump('e:\\shlog\\59_out.csv')

    return gi


if __name__ == '__main__':
    deal_guide()
