# coding=utf-8
import StatisticsBase
import functools
import utils


class AvatarGuildBandit(StatisticsBase.AvatarBase):
    def __init__(self):
        super(AvatarGuildBandit, self).__init__()
        self.try_enter_num = 0
        self.enter_success_num = 0
        self.mission_success_num = 0

    @staticmethod
    def key(row_dict):
        return row_dict['gbId'].strip()

    def process_one(self, row):
        log_type = row['logType'].strip()
        if log_type == '1':
            self.try_enter_num += 1
        elif log_type == '2':
            self.enter_success_num += 1
        elif log_type == '4':
            self.mission_success_num += 1


class DayGuildBandit(StatisticsBase.DayBase):
    pass


class GuildBandit(StatisticsBase.StatisticsBase):
    DAY_CLASS = DayGuildBandit
    AVATAR_CLASS = AvatarGuildBandit
    COL_HEADER = [
        '日',
        '角色数',
        '玩家数',
        '参与度',
        '尝试进入次数',
        '进入次数',
        '完成次数'
    ]

    def process_one(self, row_dict):
        detail_belong_name = row_dict['detail_belongName']
        if utils.is_name_inter(detail_belong_name):
            return

        super(GuildBandit, self).process_one(row_dict)

    def get_datas(self):
        return [
            self.get_headers(),
            self.get_infos('avatar_nums'),
            self.get_infos('get_account_num'),
            self.get_infos('account_rate'),
            self.get_infos('reduce_num', lambda x: x.try_enter_num),
            self.get_infos('reduce_num', lambda x: x.enter_success_num),
            self.get_infos('reduce_num', lambda x: x.mission_success_num),
        ]


def deal_guild_bandit(da_dic):
    gb = GuildBandit('e:\\shlog\\log_60.csv.new.csv')
    gb.process_data()\
        .set_da_dic(da_dic)\
        .dump('e:\\shlog\\60_out.csv')
    return gb


if __name__ == '__main__':
    deal_guild_bandit()
