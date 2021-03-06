import os
import re

class State(object):
    normal = 1
    avatar = 2

def main():
    gbId = ''
    #pat = re.compile(r'Avatar\((\d+)\)\]_guildInit\: 5630366051649716225')
    pat = re.compile(r'Avatar\((\d+)\)\]:_guildInit: 5630366051649716225')
    idstr = ''
    targetstr = '$$$$$$'
    fw = open(r'e:\shLog\tmp.log', 'w')
    with open(r'E:\shLog\logger_baseapp.log.2021-03-30', encoding='utf-8') as fr:
        while 1:
            try:
                line = fr.readline()
                if not line:
                    break

                find = pat.search(line)
                if find:
                    idstr = find.group(1)
                    targetstr = f'[Avatar({idstr})]:_calcAct:'

                if targetstr in line:
                    tup = line.split(' ')
                    now = int(tup[-2])
                    last = int(tup[-1].strip())
                    if now < last:
                        print(line, now - last)
            except UnicodeDecodeError as e:
                pass


def out_test_0618():
    ori_file = r'E:\shLog\tmp\ori.log'
    ori_base = r'F:\shdownload\log\9.150.94.241_data_home_user00_log_20210716_logger_baseapp.log-20210716'
    tmp_file = r'E:\shLog\tmp\db.8444835990201591397'
    filter_gbid = r'E:\shLog\tmp\ori.log.8444835983061208270'
    filter_avatar_id = r'E:\shLog\tmp\ori.log.96619'
    filter_modify_failed = r'E:\shLog\tmp\base.onUpdateGuildDiffsProxy'
    #fw = open(filter_gbid, 'w')
    fw = open(filter_modify_failed, 'w')


    with open(ori_base) as fr:
        for line in fr:
            if 'onUpdateGuildDiffsProxy' in line:
                fw.write(line)


if __name__ == '__main__':
    out_test_0618()
