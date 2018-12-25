from functools import partial
from ftplib import FTP
import os


class Tunnel(object):
    def __init__(self, ip, port=None):
        self.ip = ip
        self.port = port
        ftp = FTP()
        ftp.connect(self.ip)
        ftp.login('123')
        self.ftp = ftp
        self.fileList = []
        self.cur = 'tmp'

    def fileInfoCB(self, fileList, fileInfo):
        infoList = fileInfo.split()
        # print(infoList)
        fileName = infoList[-1]
        isdir = True if infoList[0].startswith('d') else False
        if isdir:
            fileList.append((isdir, fileName))
            return

        if not fileName.endswith('.py') and not fileName.endswith('.pem'):
            return

        if fileName == 'tunnel.py':
            return

        fileList.append((isdir, fileName))
        return

    def downFile(self, local, remote):
        with open(local, 'wb') as fw:
            downName = 'RETR ' + remote
            self.ftp.retrbinary(downName, fw.write)

    def downPath(self, path):
        self.ftp.cwd(path)
        fileList = []
        old = self.cur
        self.cur = os.path.join(old, path)

        try:
            os.mkdir(self.cur)
        except Exception as e:
            pass

        self.ftp.dir(partial(self.fileInfoCB, fileList))
        for isdir, filename in fileList:
            if isdir:
                self.downPath(filename)
            else:
                localname = os.path.join(self.cur, filename)
                print(localname)
                self.downFile(localname, filename)

        self.ftp.cwd('..')
        self.cur = old

    def upFile(self, filePath):
        bn = os.path.basename(filePath)
        self.ftp.storbinary('STOR ' + bn, open(filePath, 'rb'))

    def test(self):
        self.ftp.cwd('python\\pythonFunc\\')
        self.downPath('propose')
        # self.upFile('../TabbedView.py')


if __name__ == '__main__':
    tunnel = Tunnel('192.168.16.67')
    tunnel.test()
