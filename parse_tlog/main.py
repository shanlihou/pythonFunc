# coding:utf-8
import parse_tlog
import Filter
import utils
import guild_bandit
import const
import LogOne
import guild_train
import hour_stay
import left_newbie_header
import guide_flow
import bandit_boss


if __name__ == '__main__':
    fname = Filter.Filter.filter_login_log(const.ORI_FILE_NAME)

    filt = Filter.Filter(fname, None)

    print('-------------------------------------- 内部玩家次留统计')
    tmp_log_name = filt.filter_inner()
    out_name = utils.get_out_name('out', 'daily_inner.csv')
    parse_tlog.parse_tlog(tmp_log_name, out_name)

    print('-------------------------------------- 外部玩家次留统计')
    tmp_log_name = filt.filter_out()
    out_name = utils.get_out_name('out', 'daily_outer.csv')
    parse_tlog.parse_tlog(tmp_log_name, out_name)

    print('-------------------------------------- 帮盗统计')
    fname = utils.filter_tlog(const.ORI_FILE_NAME, 'RoundFlow')
    f = Filter.Filter(fname, LogOne.RoundFlow)
    guild_bandit.parse_by_act(f, 9)

    print('-------------------------------------- 帮会修炼')
    fname = utils.filter_tlog(const.ORI_FILE_NAME, 'GuildTrainFlow')
    f = Filter.Filter(fname, None)
    fname = f.filter_out()

    gt = guild_train.GuildTrain(fname)
    gt.parse()
    gt.out_as_csv('guild_train_out_first.csv')

    print('-------------------------------------- 日留')
    fname = Filter.Filter.filter_login_log(const.ORI_FILE_NAME)
    f = Filter.Filter(fname, None)

    fname = f.filter_inner()
    hs = hour_stay.HourStay(fname)
    hs.parse()
    hs.out_as_csv('hour_inner.csv')

    fname = f.filter_out()
    hs = hour_stay.HourStay(fname)
    hs.parse()
    hs.out_as_csv('hour_out_second.csv')

    print('-------------------------------------- 流失玩家头')
    left_newbie_header.get_header()

    print('-------------------------------------- 新手节点')
    guide_flow.guide_flow()

    print('-------------------------------------- 帮盗boss')
    bandit_boss.bandit_boss()