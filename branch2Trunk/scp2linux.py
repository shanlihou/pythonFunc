import os
import re


class Scp(object):
    def get_file_list(self):
        ret = os.popen('svn st -q')
        pat = re.compile('[^ ]+$')
        ret_list = []
        for line in ret:
            line = line.strip()
            if line.endswith('.cpp') or line.endswith('.h'):
                find = pat.search(line)
                if find:
                    ret_list.append(find.group())

        return ret_list

    def scp(self, file_list):
        for file_path in file_list:
            unix_path = file_path.replace('\\', '/')
            dst = '/home/shanlihou/shsvn/kbe/src/{}'.format(unix_path)
            cmd_str = 'scp {} shanlihou@192.168.16.223:{}'.format(
                unix_path, dst)
            print(cmd_str)
            os.system(cmd_str)

    def test(self):
        print(1)
        os.chdir(r'D:\shKbeWin\kbe\src')
        fl = self.get_file_list()
        print(fl)
        fl = [i for i in fl if not i.startswith('server\\tools\\')]
        for i in fl:
            print(i)
        self.scp(fl)


def main():
    scp = Scp()
    scp.test()


if __name__ == '__main__':
    main()
