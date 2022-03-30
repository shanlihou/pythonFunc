import os
import re


LOG_PATH = r'f:\shdownload\log\dong_tian.txt'


def main():
    pat = re.compile(r"'(rpc.+)', \(([^\)]+)\)")
    strs = []
    with open(LOG_PATH) as fr:
        for line in fr:
            find = pat.search(line)
            if find:
                _func, args = find.groups()
                _str = '    rei.{}({})'.format(_func, args)
                strs.append(_str)

    strs.reverse()
    for i in strs:
        print(i)

if __name__ == '__main__':
    main()
