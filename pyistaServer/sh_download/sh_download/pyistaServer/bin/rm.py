import argparse
import os
import shutil


def main(args):
    ap = argparse.ArgumentParser()
    ap.add_argument('-r', '--recursive',
                    action="store_true",
                    default=False,
                    help='remove directory and its contents recursively')
    ap.add_argument('-i', '--interactive',
                    action="store_true",
                    default=False,
                    help='prompt before every removal')
    ap.add_argument('-f', '--force',
                    action='store_true',
                    default=False,
                    help='attempt to delete without confirmation or warning due to permission or file existence (override -i)')
    ap.add_argument('-v', '--verbose',
                    action="store_true",
                    default=False,
                    help='explain what is being done')
    ap.add_argument('paths', action="store", nargs='+',
                    help='files or directories to delete')

    ns = ap.parse_args(args)
    print(ns)
    for path in ns.paths:
        if os.path.isdir(path):
            if ns.recursive:
                shutil.rmtree(path)
            else:
                return 'failed'
        else:
            os.remove(path)

    return 'ok'


if __name__ == '__main__':
    os.chdir('../sh_download/pyistaServer')
    print(os.getcwd())
    arg_str = 'client.py'
    main(arg_str.split())
