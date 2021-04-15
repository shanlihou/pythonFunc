# coding:utf-8
# 灵虚
import utils
import LogOne


def parse_lingxu():
    fname = utils.filter_from_origin(LogOne.LingxuAttackFlow.FILTER_STR)
    with utils.utf8_open(fname) as fr:
        for line in fr:
            lo = LogOne.get_log_from_line(line)
            if lo.gbid == '8444553113334133613':
                print(line)


if __name__ == '__main__':
    parse_lingxu()