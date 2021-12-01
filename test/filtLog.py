import os
import re

class State(object):
    normal = 1
    avatar = 2

def main():
    fw = open(r'e:\shLog\tmp.log', 'w')
    with open(r'E:\shLog\logger_baseapp.log', encoding='utf-8') as fr:
        for line in fr:
            if 'Guild(754)' in line:
                fw.write(line)
            elif 'Avatar(604)' in line:
                if 'checkAchievementTrigger' in line:
                    continue
                elif 'pickUpItems' in line:
                    continue
                elif 'tlog' in line:
                    continue
                elif 'applyEndDigTreasure' in line:
                    continue

                fw.write(line)


def out_test_0618():
    ori_file = r'E:\shLog\tmp\ori.log'
    ori_base = r'F:\shdownload\log\logger_baseapp.log.1-20210908-180010'
    tmp_file = r'E:\shLog\tmp\db.8444835990201591397'
    filter_gbid = r'E:\shLog\tmp\ori.log.8444835983061208270'
    filter_avatar_id = r'E:\shLog\tmp\ori.log.96619'
    final = r'F:\shdownload\log\1578921.log'
    #fw = open(filter_gbid, 'w')
    fw = open(final, 'w')


    with open(ori_base) as fr:
        for line in fr:
            if '1578921' in line:
                fw.write(line)


if __name__ == '__main__':
    main()
