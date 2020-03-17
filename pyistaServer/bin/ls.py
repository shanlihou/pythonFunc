import argparse
import os


class LS(object):
    @staticmethod
    def list_idr_info(path):
        paths = (path, ) if path else ()
        datas = []
        for filename in os.listdir(*paths):
            info_list = []
            info_list.append('d' if os.path.isdir(filename) else '-')
            info_list.append(filename)
            info_str = '{} {}'.format(*info_list)
            datas.append(info_str)

        return '\n'.join(datas)


def main(arg_str):
    p = argparse.ArgumentParser()
    p.add_argument('files', nargs='?')
    ns = p.parse_args(arg_str)
    return LS.list_idr_info(ns.files)


if __name__ == '__main__':
    ls = LS()
    print(ls.list_idr_info(''))
