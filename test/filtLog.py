import os
import re

class State(object):
    normal = 1
    avatar = 2

def main():
    fw = open(r'e:\shLog\tmp.log', 'w')
    with open(r'E:\shLog\logger_baseapp.log', encoding='utf-8') as fr:
        for line in fr:
            if '_sendMasAppInfoToClient' in line:
                fw.write(line)

            if '] entities enable' in line:
                if '12-03' not in line:
                    continue

                if 'Avatar' not in line:
                    continue
                fw.write(line)


if __name__ == '__main__':
    main()
