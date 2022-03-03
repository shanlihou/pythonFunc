import re
import shutil

logPath = r'F:\shdownload\log\Avatar(4252471).txt'


def main():
    fwname = '{}.{}'.format(logPath, 'new')
    fw = open(fwname, 'w')
    pat = re.compile(r'')

    s_str = '"log": "'
    e_str = '", "ip":'
    with open(logPath) as fr:
        for line in fr:
            start = line.index(s_str)
            end = line.index(e_str)
            start += len(s_str)
            data = line[start: end] + '\n'
            fw.write(data)

    fw.close()
    shutil.move(fwname, logPath)


if __name__ == '__main__':
    main()