from xmlrpc.client import ServerProxy
import sys
import json
import os
import re


class OprType(object):
    cmd = 1
    down = 2
    downJ = 3


def exec_cmd(s, cmd_str):
    cmd_req = '{"cmd_str": "%s"}' % cmd_str
    result = s.cmd(cmd_req)
    ret_obj = json.loads(result)
    print(ret_obj['result'])


if __name__ == '__main__':
    opr = OprType.downJ
    if opr == OprType.cmd:
        s = ServerProxy("http://192.168.16.82:8080")
        while True:
            print('please inpu:')
            i = input()
            if not i.strip():
                continue

            if i == 'q':
                sys.exit()
            else:
                exec_cmd(s, i)
    elif opr == OprType.down:
        s = ServerProxy("http://192.168.16.82:8080")
        root = r'E:\shgithub\others\Javbus_crawler'
        os.chdir(root)
        result = os.popen('git status')
        pat = re.compile('\w+\.py')
        files = []
        for line in result.readlines():
            if '.py' in line:
                find = pat.search(line)
                if find:
                    files.append(find.group())

        for filename in files:
            cmd_str = 'ftp -r others/Javbus_crawler/{}'.format(filename)
            print(cmd_str)
            exec_cmd(s, cmd_str)
    elif opr == OprType.downJ:
        s = ServerProxy("http://192.168.16.82:8080")
        exec_cmd(s, 'ftp -r others/Javbus_crawler')
