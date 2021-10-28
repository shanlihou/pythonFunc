import gzip
import os
import shutil
from collections import deque
class A(object):
    def __init__(self, b, c):
        self.b = b
        self.c = c

    @property
    def abc(self):
        return 123


DIR = r'.'
def main():
    for i in os.listdir(DIR):
        if not (i.startswith('game_') and i.endswith('.sh')):
            continue
        filename = os.path.join(DIR, i)
        new_file = filename + '.new'
        fw = open(new_file, 'w')
        with open(filename) as fr:
            for line in fr:
                if 'export KBE_BIN_PATH="/mnt/hgfs/trunk_server/kbe/bin/server/"' in line:
                    line = line.replace('trunk_server', 'shitu_server')

                fw.write(line)
        fw.close()
        shutil.move(new_file, filename)
        os.system("sed 's/^M//' {} > {}".format(filename, new_file))
        shutil.move(new_file, filename)


if __name__ == '__main__':
    # a = b'\x1f\x8b\x08\x00\xdd,P`\x02\xffc` \x03\x00\x00\x0ew\xaf\x195\x00\x00\x00'
    # a = gzip.decompress(a)
    # print(a)
    # q = deque()
    # a = A(1, 2)
    # q.append(a)
    # q.append(A(3, 4))
    # q.append(A(5, 6))
    # q.remove(A(5, 6))
    # print(q)
    main()