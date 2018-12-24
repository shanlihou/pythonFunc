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

    def fileInfoCB(self, fileInfo):
        infoList = fileInfo.split()
        print(infoList)
        fileName = infoList[-1]
        if not fileName.endswith('.py') and not fileName.endswith('.pem'):
            return

        if fileName == 'tunnel.py':
            return

        print('will down :', fileName)
        self.fileList.append(fileName)
        return
        with open(fileName, 'wb') as fw:
            # downName = 'RETR ' + os.path.join(self.downPath, fileName)
            downName = 'RETR ' + fileName
            self.ftp.retrbinary(downName, fw)

    def downPath(self, path):
        self.downPath = 'python\\pythonFunc\\' + path
        self.ftp.cwd(self.downPath)
        self.ftp.dir(self.fileInfoCB)
        filePath = '..\\' + path
        try:
            os.mkdir(filePath)
        except Exception as e:
            print(e)

        for fileName in self.fileList:
            with open(filePath + '\\' + fileName, 'wb') as fw:
                downName = 'RETR ' + fileName
                self.ftp.retrbinary(downName, fw.write)

    def upFile(self, filePath):
        bn = os.path.basename(filePath)
        self.ftp.storbinary('STOR ' + bn, open(filePath, 'rb'))

    def test(self):
        self.downPath('propose')
        # self.upFile('../TabbedView.py')


if __name__ == '__main__':
    tunnel = Tunnel('192.168.16.67')
    tunnel.test()
