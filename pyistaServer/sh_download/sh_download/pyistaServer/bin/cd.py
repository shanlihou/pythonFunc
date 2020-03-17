import os
import argparse


class CD(object):
    @staticmethod
    def cwd(path):
        os.chdir(path)


def main(args):
    p = argparse.ArgumentParser()
    p.add_argument('paths', nargs='?')
    ns = p.parse_args(args)
    CD.cwd(ns.paths)
    return 'ok'


if __name__ == '__main__':
    main(['..'])