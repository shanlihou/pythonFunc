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

    def down_path(self, remote_path):
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

    def up_file(self, filePath):
        bn = os.path.basename(filePath)
        self.ftp.storbinary('STOR ' + bn, open(filePath, 'rb'))

    def test(self):
        self.down_path('bmob')
        self.upFile('../baidu.py')


def main(args):
    ap = argparse.ArgumentParser()
    ap.add_argument('ip', default='192.168.16.123', nargs='?')
    ap.add_argument('--up', '-u', action='store_true')
    ap.add_argument('remote_dir')
    ns = ap.parse_args(args)
    t = Tunnel(ns.ip)
    if ns.up:
        t.up_file(ns.remote_dir)
    else:
        t.down_path(ns.remote_dir)
    return 'ok'


if __name__ == '__main__':
    arg_str = 'abdd'
    main(arg_str.split())
