# coding:utf-8
import os
import shutil


ORI_ASSETS = r'E:\trunk_server\kbengine\assets'
SHITU_ASSETS = r'F:\shitu_server\assets'



def main():
    script_dir = os.path.join(ORI_ASSETS, "scripts")
    script_data_dir = os.path.join(script_dir, 'data')
    print(script_data_dir)
    cmd_str = f'svn st -q {script_dir}'
    print(cmd_str)
    with os.popen(cmd_str) as fr:
        for line in fr:
            rets = line.split(' ')
            rets = [i for i in rets if i]
            if rets[1].startswith(script_data_dir):
                continue

            ori_dir = rets[1].strip()
            if os.path.isdir(ori_dir):
                continue

            dst_dir = SHITU_ASSETS + ori_dir.split(ORI_ASSETS)[1]
            print(dst_dir)
            shutil.copy(ori_dir, dst_dir)


if __name__ == '__main__':
    main()