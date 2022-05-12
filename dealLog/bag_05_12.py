from asyncore import read
import re
import datetime
import time
import collections


SAVE_LOG_PATH = r'E:\shLog\parse_avatar\to.txt'
COMP_LOG_PATH = r'E:\shLog\parse_avatar\completed.txt'


def read_info(fr, idx):
    pat = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+) (\d+)')
    ret_list = []
    for line in fr:
        find = pat.search(line)
        if find:
            ret = time.mktime(time.strptime(find.group(1), '%Y-%m-%d %H:%M:%S'))
            ret = ret * 1000 + int(find.group(2))
            ret_list.append((ret, idx, line))

    return ret_list

def main():
    _fr_to = open(SAVE_LOG_PATH)
    _fr_co = open(COMP_LOG_PATH)
    _lines = read_info(_fr_to, 1)
    _lines.extend(read_info(_fr_co, 0))
    _lines = sorted(_lines, key= lambda x: (x[0], x[1]))

    fw = open(r'E:\shLog\parse_avatar\final.txt', 'w')
    #print(_lines)

    _dq = collections.deque()
    for _time, idx, line in _lines:

        if idx == 1:
            if _dq:
                _last = _dq[0]
                if _last[1] == 0:
                    print(_last[2])
                fw.write(_last[2])
            fw.write(line)

        _dq.appendleft((_time, idx, line))
        if len(_dq) > 3:
            _dq.pop()

    fw.close()

if __name__ == '__main__':
    main()

