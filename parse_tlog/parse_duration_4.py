# coding:utf-8
# 统计11月份连续登陆4天玩家的qq号
import Filter
import const
import utils
import LogOne


def main():
    fname = Filter.Filter.filter_login_log(const.ORI_FILE_NAME)

    filt = Filter.Filter(fname, None)
    tmp_log_name = filt.filter_out()

    player_dic = {}
    player_name_dic = {}
    out_name = utils.get_out_name('out', '1_20.txt')
    fw = utils.utf8_open(out_name, 'w')
    mark_set = set()
    with utils.utf8_open(fname, encoding='utf-8') as fr:
        for line in fr:
            log_one = LogOne.get_log_from_line(line)
            player_dic.setdefault(log_one.account, set())
            player_dic[log_one.account].add(log_one.day)

            player_name_dic.setdefault(log_one.account, set())
            try:
                player_name_dic[log_one.account].add(log_one.name)
            except:
                pass
            if len(player_dic[log_one.account]) >= 4:
                mark_set.add(log_one.account)

    count = 0
    for i in mark_set:
        names = player_name_dic[i]
        _2 = '|'.join(names)
        fw.write(','.join((i, _2)) + '\n')
        count += 1
    print(count)

if __name__ == '__main__':
    main()