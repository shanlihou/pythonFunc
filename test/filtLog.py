import os
import re

class State(object):
    normal = 1
    avatar = 2


if __name__ == '__main__':
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