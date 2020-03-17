import argparse
import os
import shutil


def main(args):
    p = argparse.ArgumentParser()
    p.add_argument('src', nargs='+')
    p.add_argument('dst')
    ns = p.parse_args(args)

    def copy_common(src, dst):
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy(src, dst)

    for src in ns.src:
        src_base = os.path.basename(src)
        if os.path.isdir(ns.dst):
            dst_name = os.path.join(ns.dst, src_base)
        else:
            dst_name = ns.dst
        copy_common(src, dst_name)

    return 'ok'


if __name__ == '__main__':
    os.chdir('../sh_download/pyistaServer')
    print(os.getcwd())
    cmd_str = 'FetchFtp download/'
    main(cmd_str.split())
