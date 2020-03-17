from xmlrpc.client import ServerProxy
import sys
import json


def exec_cmd(s, cmd_str):
    cmd_req = '{"cmd_str": "%s"}' % cmd_str
    result = s.cmd(cmd_req)
    ret_obj = json.loads(result)
    print(ret_obj['result'])


if __name__ == '__main__':
    s = ServerProxy("http://192.168.16.123:8080")
    while True:
        i = input()
        if not i.strip():
            continue

        if i == 'q':
            sys.exit()
        else:
            exec_cmd(s, i)
