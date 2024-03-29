#!/usr/bin/env python
# --*-- coding: utf-8 --*--

from get_fileProperty import fileProperty
import socket
import threading
import os
import stat
import sys
import time
import traceback

allow_delete = False


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('google.com', 80))
        ip = s.getsockname()[0]
        s.close()
    except:
        ip = 'N/A'
    return ip


#HOST = socket.gethostbyname(socket.gethostname())
HOST = get_local_ip()
PORT = 9527  # command port
#CWD  = os.getenv('HOME')
CWD = "G:\shgame"


def log(func, cmd):
    logmsg = time.strftime("%Y-%m-%d %H-%M-%S [-] " + func)
    print("func:%s, %s" % (logmsg, cmd))


class FtpServerProtocol(threading.Thread):
    def __init__(self, commSock, address):
        threading.Thread.__init__(self)
        self.authenticated = False
        self.pasv_mode = False
        self.rest = False
        self.cwd = CWD
        self.commSock = commSock   # communication socket as command channel
        self.address = address

    def run(self):
        """
        receive commands from client and execute commands
        """
        self.sendWelcome()
        while True:
            try:
                cmd = self.commSock.recv(1024).rstrip()
                log('Received data', cmd)
                if not cmd:
                    break
            except socket.error as err:
                traceback.print_stack()
                log('Receive', err)

            try:
                cmd, arg = cmd[:4].strip().upper(), cmd[4:].strip() or None
                func = getattr(self, cmd)
                func(arg)
            except AttributeError as err:
                self.commSock.send('500 Syntax error, command unrecognized. '
                                   'This may include errors such as command line too long.\r\n')
                traceback.print_stack()
                log('Receive', err)

    #-------------------------------------#
    ## Create Ftp data transport channel ##
    #-------------------------------------#
    def startDataSock(self):
        log('startDataSock', 'Opening a data channel')
        try:
            self.dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.pasv_mode:
                self.dataSock, self.address = self.serverSock.accept()

            else:
                self.dataSock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                self.dataSock.connect((self.dataSockAddr, self.dataSockPort))
            self.dataSock = ConnectAdaptor(self.dataSock)
        except socket.error as err:
            log('startDataSock', err)

    def stopDataSock(self):
        log('stopDataSock', 'Closing a data channel')
        try:
            self.dataSock.close()
            if self.pasv_mode:
                self.serverSock.close()
        except socket.error as err:
            log('stopDataSock', err)

    #------------------------------#
    ## Ftp services and functions ##
    #------------------------------#
    def USER(self, user):
        log("USER", user)
        if not user:
            self.commSock.send(
                '501 Syntax error in parameters or arguments.\r\n')

        else:
            self.commSock.send('331 User name okay, need password.\r\n')
            self.username = user

    def PASS(self, passwd):
        log("PASS", passwd)
        if not passwd:
            self.commSock.send(
                '501 Syntax error in parameters or arguments.\r\n')

        elif not self.username:
            self.commSock.send('503 Bad sequence of commands.\r\n')

        else:
            self.commSock.send('230 User logged in, proceed.\r\n')
            self.passwd = passwd
            self.authenticated = True

    def TYPE(self, type):
        log('TYPE', type)
        self.mode = type
        if self.mode == 'I':
            self.commSock.send('200 Binary mode.\r\n')
        elif self.mode == 'A':
            self.commSock.send('200 Ascii mode.\r\n')

    def PASV(self, cmd):
        log("PASV", cmd)
        self.pasv_mode = True
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSock.bind((HOST, 0))
        self.serverSock.listen(5)
        addr, port = self.serverSock.getsockname()
        # self.commSock.send('277 Entering Passve mode (%s,%d,%d).\r\n' %
        #  (addr.replace('.', ','), (port / 256), (port % 256)))
        #self.commSock.send('227 Entering Passive Mode (%s,%u,%u).\r\n' % (','.join(addr.split('.')), port>>8&0xFF, port&0xFF))
        #self.commSock.send('227 Entering Passive Mode (%s,%u,%u).\r\n' % (','.join(addr.split('.')), port>>8&0xFF, port&0xFF))
        self.commSock.send('227 Entering Passive Mode (%s,%u,%u).\r\n' %
                           (','.join(addr.split('.')), port >> 8 & 0xFF, port & 0xFF))

    '''
    def PORT(self, pair):
        log('PORT', pair)
        pair = pair.split(',')
        ip, p1, p2 = ('.'.join(pair[:4]), pair[5], pair[6])
        self.dataSockAddr = ip
        self.dataSockPort = (256 * p1) + p2
        self.commSock.send('200 Ok.\r\n')
    '''

    def PORT(self, cmd):
        log("PORT: ", cmd)
        if self.pasv_mode:
            self.servsock.close()
            self.pasv_mode = False
        l = cmd[5:].split(',')
        self.dataSockAddr = '.'.join(l[:4])
        self.dataSockPort = (int(l[4]) << 8) + int(l[5])
        self.commSock.send('200 Get port.\r\n')

    def LIST(self, dirpath):
        if not self.authenticated:
            self.commSock.send('530 User not logged in.\r\n')
            return

        if not dirpath:
            pathname = os.path.abspath(os.path.join(self.cwd, '.'))
        elif dirpath.startswith(os.path.sep):
            pathname = os.path.abspath(dirpath)
        else:
            pathname = os.path.abspath(os.path.join(self.cwd, dirpath))

        log('LIST', pathname)
        if not self.authenticated:
            self.commSock.send('530 User not logged in.\r\n')

        elif not os.path.exists(pathname):
            self.commSock.send('550 LIST failed Path name not exists.\r\n')

        else:
            self.commSock.send('150 Here is listing.\r\n')
            self.startDataSock()
            if not os.path.isdir(pathname):
                fileMessage = fileProperty(pathname)
                self.dataSock.sock(fileMessage + '\r\n')

            else:
                for file in os.listdir(pathname):
                    try:
                        fileMessage = fileProperty(os.path.join(pathname, file))
                        # print 'fileMessage:', fileMessage
                        self.dataSock.send(fileMessage + '\r\n')
                    except Exception as e:
                        print(e)
            self.stopDataSock()
            self.commSock.send('226 List done.\r\n')

    def NLIST(self, dirpath):
        self.LIST(dirpath)

    def CWD(self, dirpath):
        if 'win' in sys.platform:
            if dirpath.startswith('/'):
                pathname = dirpath[1:]

        else:
            pathname = dirpath.endswith(
                os.path.sep) and dirpath or os.path.join(self.cwd, dirpath)
        log('CWD', '[{}], [{}], [{}]'.format(dirpath, os.path.sep, pathname))
        if not os.path.exists(pathname) or not os.path.isdir(pathname):
            self.commSock.send('550 CWD failed Directory not exists.\r\n')
            return
        self.cwd = pathname
        self.commSock.send('250 CWD Command successful.\r\n')

    def PWD(self, cmd):
        log('PWD', cmd)
        self.commSock.send('257 "%s".\r\n' % self.cwd)

    def CDUP(self, cmd):
        self.cwd = os.path.abspath(os.path.join(self.cwd, '..'))
        log('CDUP', self.cwd)
        self.commSock.send('200 Ok.\r\n')

    def DELE(self, filename):
        pathname = filename.endswith(
            os.path.sep) and filename or os.path.join(self.cwd, filename)
        log('DELE', pathname)
        if not self.authenticated:
            self.commSock.send('530 User not logged in.\r\n')

        elif not os.path.exists(pathname):
            self.send('550 DELE failed File %s not exists.\r\n' % pathname)

        elif not allow_delete:
            self.send('450 DELE failed delete not allow.\r\n')

        else:
            os.remove(pathname)
            self.commSock.send('250 File deleted.\r\n')

    def MKD(self, dirname):
        pathname = dirname.endswith(
            os.path.sep) and dirname or os.path.join(self.cwd, dirname)
        log('MKD', pathname)
        if not self.authenticated:
            self.commSock.send('530 User not logged in.\r\n')

        else:
            try:
                os.mkdir(pathname)
                self.commSock.send('257 Directory created.\r\n')
            except OSError:
                self.commSock.send(
                    '550 MKD failed Directory "%s" already exists.\r\n' % pathname)

    def RMD(self, dirname):
        import shutil
        pathname = dirname.endswith(
            os.path.sep) and dirname or os.path.join(self.cwd, dirname)
        log('RMD', pathname)
        if not self.authenticated:
            self.commSock.send('530 User not logged in.\r\n')

        elif not allow_delete:
            self.commSock.send('450 Directory deleted.\r\n')

        elif not os.path.exists(pathname):
            self.commSock.send(
                '550 RMDIR failed Directory "%s" not exists.\r\n' % pathname)

        else:
            shutil.rmtree(pathname)
            self.commSock.send('250 Directory deleted.\r\n')

    def RNFR(self, filename):
        pathname = filename.endswith(
            os.path.sep) and filename or os.path.join(self.cwd, filename)
        log('RNFR', pathname)
        if not os.path.exists(pathname):
            self.commSock.send(
                '550 RNFR failed File or Directory %s not exists.\r\n' % pathname)
        else:
            self.rnfr = pathname

    def RNTO(self, filename):
        pathname = filename.endswith(
            os.path.sep) and filename or os.path.join(self.cwd, filename)
        log('RNTO', pathname)
        if not os.path.exists(os.path.sep):
            self.commSock.send(
                '550 RNTO failed File or Direcotry  %s not exists.\r\n' % pathname)
        else:
            try:
                os.rename(self.rnfr, pathname)
            except OSError as err:
                log('RNTO', err)

    def REST(self, pos):
        self.pos = int(pos)
        log('REST', self.pos)
        self.rest = True
        self.commSock.send('250 File position reseted.\r\n')

    def RETR(self, filename):
        pathname = os.path.join(self.cwd, filename)
        log('RETR', pathname)
        if not os.path.exists(pathname):
            return
        try:
            if self.mode == 'I':
                file = open(pathname, 'rb')
            else:
                file = open(pathname, 'r')
        except OSError as err:
            log('RETR', err)

        self.commSock.send('150 Opening data connection.\r\n')
        if self.rest:
            file.seek(self.pos)
            self.rest = False

        self.startDataSock()
        while True:
            data = file.read(1024)
            if not data:
                break
            self.dataSock.send(data)
        file.close()
        self.stopDataSock()
        self.commSock.send('226 Transfer complete.\r\n')

    def STOR(self, filename):
        if not self.authenticated:
            self.commSock.send('530 STOR failed User not logged in.\r\n')
            return

        pathname = os.path.join(self.cwd, filename)
        log('STOR', pathname)
        try:
            if self.mode == 'I':
                file = open(pathname, 'wb')
            else:
                file = open(pathname, 'w')
        except OSError as err:
            log('STOR', err)

        self.commSock.send('150 Opening data connection.\r\n')
        self.startDataSock()
        while True:
            data = self.dataSock.recv(1024)
            if not data:
                break
            file.write(data)
        file.close()
        self.stopDataSock()
        self.commSock.send('226 Transfer completed.\r\n')

    def APPE(self, filename):
        if not self.authenticated:
            self.commSock.send('530 APPE failed User not logged in.\r\n')
            return

        pathname = filename.endswith(
            os.path.sep) and filename or os.path.join(self.cwd, filename)
        log('APPE', pathname)
        self.commSock.send('150 Opening data connection.\r\n')
        self.startDataSock()
        if not os.path.exists(pathname):
            if self.mode == 'I':
                file = open(pathname, 'wb')
            else:
                file = open(pathname, 'w')
            while True:
                data = self.dataSock.recv(1024)
                if not data:
                    break
                file.write(data)

        else:
            n = 1
            while not os.path.exists(pathname):
                filename, extname = os.path.splitext(pathname)
                pathname = filename + '(%s)' % n + extname
                n += 1

            if self.mode == 'I':
                file = open(pathname, 'wb')
            else:
                file = open(pathname, 'w')
            while True:
                data = self.dataSock.recv(1024)
                if not data:
                    break
                file.write(data)
        file.close()
        self.stopDataSock()
        self.commSock.send('226 Transfer completed.\r\n')

    def SYST(self, arg):
        log('SYS', arg)
        self.commSock.send('215 %s type.\r\n' % sys.platform)

    def SIZE(self, arg):
        pathname = os.path.join(self.cwd, arg)
        size = os.stat(pathname)[6]
        print('size:', size)
        self.commSock.send('213 %d\r\n' % size)

    def HELP(self, arg):
        log('HELP', arg)
        help = """
            214
            USER [name], Its argument is used to specify the user's string. It is used for user authentication.
            PASS [password], Its argument is used to specify the user password string.
            PASV The directive requires server-DTP in a data port.
            PORT [h1, h2, h3, h4, p1, p2] The command parameter is used for the data connection data port
            LIST [dirpath or filename] This command allows the server to send the list to the passive DTP. If
                 the pathname specifies a path or The other set of files, the server sends a list of files in
                 the specified directory. Current information if you specify a file path name, the server will
                 send the file.
            CWD Type a directory path to change working directory.
            PWD Get current working directory.
            CDUP Changes the working directory on the remote host to the parent of the current directory.
            DELE Deletes the specified remote file.
            MKD Creates the directory specified in the RemoteDirectory parameter on the remote host.
            RNFR [old name] This directive specifies the old pathname of the file to be renamed. This command
                 must be followed by a "heavy Named "command to specify the new file pathname.
            RNTO [new name] This directive indicates the above "Rename" command mentioned in the new path name
                 of the file. These two Directive together to complete renaming files.
            REST [position] Marks the beginning (REST) ​​The argument on behalf of the server you want to re-start
                 the file transfer. This command and Do not send files, but skip the file specified data checkpoint.
            RETR This command allows server-FTP send a copy of a file with the specified path name to the data
                 connection The other end.
            STOR This command allows server-DTP to receive data transmitted via a data connection, and data is
                 stored as A file server site.
            APPE This command allows server-DTP to receive data transmitted via a data connection, and data is stored
                 as A file server site.
            SYS  This command is used to find the server's operating system type.
            HELP Displays help information.
            QUIT This command terminates a user, if not being executed file transfer, the server will shut down
                 Control connection\r\n.
            """
        self.commSock.send(help)

    def QUIT(self, arg):
        log('QUIT', arg)
        self.commSock.send('221 Goodbye.\r\n')

    def sendWelcome(self):
        """
        when connection created with client will send a welcome message to the client
        """
        self.commSock.send('220 Welcome.\r\n')


class ConnectAdaptor(object):
    def __init__(self, commSock):
        print(sys.platform)
        self.isWin = 'win' in sys.platform or 'ios' in sys.platform
        self.commSock = commSock

    def send(self, msg):
        if self.isWin and not isinstance(msg, bytes):
            msg = msg.encode('utf-8')
        self.commSock.send(msg)

    def recv(self, *args):
        ret = self.commSock.recv(*args)
        if self.isWin:
            ret = ret.decode('utf-8')
        return ret

    def close(self):
        self.commSock.close()


def serverListener():
    global listen_sock
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind((HOST, PORT))
    listen_sock.listen(5)

    log('Server started', 'Listen on: %s, %s' % listen_sock.getsockname())
    while True:
        connection, address = listen_sock.accept()
        f = FtpServerProtocol(ConnectAdaptor(connection), address)
        f.start()
        log('Accept', 'Created a new connection %s, %s' % address)


if __name__ == "__main__":
    #log('Start ftp server', 'Enter q or Q to stop ftpServer...')
    print('start:')
    listener = threading.Thread(target=serverListener)
    listener.start()
    if input().lower() == "q":
        listen_sock.close()
        log('Server stop', 'Server closed')
        sys.exit()
