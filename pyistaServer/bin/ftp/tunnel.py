from ftplib import FTP
import os
import argparse


class Tunnel(object):
    def __init__(self, ip, port=None):
        self.ip = ip
        self.port = port
        ftp = FTP()
        ftp.connect(self.ip)
        ftp.login('123')
        self.ftp = ftp
        self.file_list = []

    def fileInfoCB(self, fileInfo):
        info_list = fileInfo.split()
        filename = info_list[-1]

        if filename == 'sh_download':
            return

        self.file_list.append({
            'filename': filename,
            'is_dir': info_list[0].startswith('d')
        })

    def join_remote_names(self, *args):
        return '\\'.join(args)

    def down_path(self, remote_path, hasroot):
        if hasroot:
            remote_root = os.path.dirname(remote_path)
            remote_path = os.path.basename(remote_path)
        else:
            remote_root = 'python\\pythonFunc'

        local_root = 'sh_download'
        try:
            os.mkdir(local_root)
        except Exception as e:
            pass

        self.ftp.cwd(remote_root)
        os.chdir(local_root)

        def rec_down(cur):

            try:
                os.mkdir(cur)
            except Exception as e:
                pass

            self.ftp.cwd(cur)
            os.chdir(cur)

            self.file_list = []
            self.ftp.dir(self.fileInfoCB)

            for fileinfo in self.file_list:
                print(fileinfo)
                if fileinfo['is_dir']:
                    rec_down(fileinfo['filename'])
                else:
                    with open(fileinfo['filename'], 'wb') as fw:
                        downname = 'RETR {}'.format(fileinfo['filename'])
                        self.ftp.retrbinary(downname, fw.write)

            self.ftp.cwd('..')
            os.chdir('..')

        rec_down(remote_path)
        os.chdir('..')
        self.ftp.cwd('..\\..')

    def list(self):
        self.file_list = []
        self.ftp.dir(self.fileInfoCB)
        return '\n'.join([x['filename'] for x in self.file_list])

    def ch_dir(self, dir):
        self.ftp.cwd(dir)

    def up_file(self, filePath):
        bn = os.path.basename(filePath)
        self.ftp.storbinary('STOR ' + bn, open(filePath, 'rb'))

    def test(self):
        self.down_path('bmob')
        self.upFile('../baidu.py')


g_tunnel = Tunnel('192.168.16.123')


def main(args):
    ap = argparse.ArgumentParser()
    ap.add_argument('ip', default='192.168.16.123', nargs='?')
    group = ap.add_mutually_exclusive_group()
    group.add_argument('--up', '-u', default=None)
    group.add_argument('--download', '-d', default=None)
    group.add_argument('--root', '-r', default=None)
    group.add_argument('--changedir', '-c', default=None)
    group.add_argument('--list', '-l', action='store_true')
    # ap.add_argument('remote_dir')
    ns = ap.parse_args(args)
    t = g_tunnel
    ret = None
    if ns.up is not None:
        ret = t.up_file(ns.remote_dir)
    elif ns.download is not None:
        ret = t.down_path(ns.remote_dir, ns.root)
    elif ns.list:
        ret = t.list()
    return 'ok' if ret is None else ret


if __name__ == '__main__':
    arg_str = '-l'
    main(arg_str.split())
