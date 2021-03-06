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

    def _get_cur_file_list(self):
        self.file_list = []
        self.ftp.dir(self.fileInfoCB)
        return self.file_list

    def _get_cur_file_info(self, filename):
        for fileinfo in self._get_cur_file_list():
            if fileinfo['filename'] == filename:
                return fileinfo

        return None

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

        file_info = self._get_cur_file_info(remote_path)
        if not file_info['is_dir']:
            self._down_file(file_info['filename'])
        else:
            def rec_down(cur):

                try:
                    os.mkdir(cur)
                except Exception as e:
                    pass

                self.ftp.cwd(cur)
                os.chdir(cur)

                for fileinfo in self._get_cur_file_list():
                    print(fileinfo)
                    if fileinfo['is_dir']:
                        rec_down(fileinfo['filename'])
                    else:
                        self._down_file(fileinfo['filename'])

                self.ftp.cwd('..')
                os.chdir('..')

            rec_down(remote_path)

        os.chdir('..')
        self.ftp.cwd('..\\..')

    def _down_file(self, filename):
        with open(filename, 'wb') as fw:
            downname = 'RETR {}'.format(filename)
            self.ftp.retrbinary(downname, fw.write)

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
    print(ns)
    return
    t = Tunnel('192.168.16.123')
    ret = None
    if ns.root is not None:
        ret = t.down_path(ns.root, True)
    elif ns.up is not None:
        ret = t.up_file(ns.up)
    elif ns.download is not None:
        ret = t.down_path(ns.remote_dir, ns.root)
    elif ns.list:
        ret = t.list()
    return 'ok' if ret is None else ret


if __name__ == '__main__':
    arg_str = '-u a.tar'
    main(arg_str.split())
