import os
import re
import json
import shutil

def cache(dir_name):
    cur_dir = os.getcwd()
    os.chdir(dir_name)
    ret = os.popen('svn st')
    pat = re.compile('[^ ]+$')
    ret_list = []
    for line in ret:
        line = line.strip()
        if line.endswith('.py') or line.endswith('.def'):
            find = pat.search(line)
            if find:
                if find.group().startswith('data\\'):
                    continue
                ret_list.append(os.path.join(dir_name, find.group()))

    os.chdir(cur_dir)
    write_dic = {}
    for index, i in enumerate(ret_list):
        filename = '{}.txt'.format(index)
        write_dic[i] = filename
        shutil.copyfile(i, 'tmp\\{}'.format(filename))

    json.dump(write_dic, open('tmp\\cache_name.txt', 'w'))


if __name__ == '__main__':
    dir_name = r'E:\trunk_server\kbengine\assets\scripts'
    ret = cache(dir_name)
    print(ret)