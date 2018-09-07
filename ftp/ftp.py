from ftplib import FTP
import ftplib
import os
import re
import sys


def ftpDownByName(fileName):
    ftp = FTP()
    ftp.connect("10.30.6.77", "29")
    ftp.login('ftpuser', 'abc@123456')
    pat = re.compile(r'^(.+)/([^/]+)$')
    find = pat.search(fileName)
    if find:
        # print(find.group(1))
        ##print(find.group(2) + '\n')
        ftp.cwd('pengminfang20170317')
        if not os.path.exists(find.group(1)):
            os.makedirs(find.group(1))
        os.chdir(find.group(1))
        ftp.cwd(find.group(1))
        downName = 'RETR ' + find.group(2)
        f = open(find.group(2), 'wb')
        ftp.retrbinary(downName, f.write)
        os.chdir('..')


def ftpDownByTxtName(fileName):
    fileRead = open(fileName, 'r')
    for line in fileRead:
        ftpDownByName(line.replace('\n', '').replace('\r', ''))


def ftpRec(ftp, path):
    # print path
    try:
        ret = ftp.cwd(path)
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        if 'successful' in ret:
            ftpList = ftp.nlst()
            for i in ftpList:
                ftpRec(ftp, i)
        else:
            return
        ftp.cwd('..')
        os.chdir('..')
    except ftplib.error_perm:
        downName = 'RETR ' + path
        f = open(path, 'wb')
        ftp.retrbinary(downName, f.write)
        return


def createSH(path, type):
    crossDict = {"Rhea": "arm-linux-gnueabihf-5.2.1-", "Themis": "arm-linux-gnueabihf-4.9.1-", "Eos": "arm-hisiv300-linux-", "Eos2": "arm-hisiv100nptl-linux-", "Eos3": "arm-hisiv300-linux-", "Alps": "csky-linux-", "Adreia": "arm-none-linux-gnueabi-4.6.1-",
                 "Demeter2": "arm-none-linux-gnueabi-", "Nova": "arm-hisiv500-linux-uclibcgnueabi-", "Nova2": "arm-hisiv501-linux-uclibcgnueabi-", "Cavlir": "arm-linux-gnueabihf-4.9.1-", "Demeter": "arm-none-linux-gnueabi-", "TI-16M": "arm_v5t_le-", "TI-8M": "arm_v5t_le-"}
    pat = re.compile(r'CROSS=(\s*\S+)')
    fileRead = open(path, 'r')
    pathSH = path + '/IPC/Tool/' + 'checkApp_new.sh'
    fileWrite = open(path + '.new', 'w')
    for line in fileRead:
        find = pat.search(line)
        if find:
            # print find.group()
            tub = pat.subn('CROSS=' + crossDict[type], line)
            # print tub
            fileWrite.write(tub[0])
        else:
            fileWrite.write(line)
    fileRead.close()
    fileWrite.close()
    os.rename(path + '.new', path)


def ftpUP(path):
    ftp = FTP()
    ftp.connect('10.1.2.102')
    ftp.login('admin01', 'dahua@2017')
    ftp.cwd(path)
    for i in os.listdir('.'):
        if os.path.isdir(i):
            continue
        ftp.storbinary('STOR ' + i, open(i, 'rb'))


def ftpDown(path, path2):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect("10.30.6.77", "29")
    ftp.login('ftpuser', 'abc@123456')
    if (path):
        ftp.cwd(path)
    ftpRec(ftp, path2)


file1 = open('1.txt', 'w')
file2 = open('2.txt', 'w')
fileNo = open('fileNotFind.txt', 'w')
count = 0


def ftpRecSearch(ftp, path, name, iNum, pPath):
    try:
        ret = ftp.cwd(path)
        global count
        # print pPath + '/' + path
        '''
		if not os.path.exists(path):
			os.makedirs(path)
		os.chdir(path)
		'''
        if 'successful' in ret:
            ftpList = ftp.nlst()
            for i in ftpList:
                if i == name:
                    mkPath = pPath + '/' + path
                    # print pPath + '/' + path + '/' + i
                    file1.writelines(name + '\n')
                    file2.writelines(pPath + '/' + path + '/' + name + '\n')
                    count += 1
                    if not os.path.exists(mkPath):
                        os.makedirs(mkPath)
                    os.chdir(mkPath)
                    downName = 'RETR ' + i
                    f = open(i, 'wb')
                    ftp.retrbinary(downName, f.write)
                    os.chdir('/root/ftp/download')
                if path == '.':
                    ftpRecSearch(ftp, i, name, iNum + 1, path)
                else:
                    ftpRecSearch(ftp, i, name, iNum + 1, pPath + '/' + path)
        else:
            return
        ftp.cwd('..')
        # os.chdir('..')
    except ftplib.error_perm:
        if pPath + '/' + path == './yinting/Eos':
            # print 'hello'
            # print name
            pass
        if path == name:
            pPath + '/' + name
        '''
		downName = 'RETR ' + path
		f = open(path, 'wb')
		ftp.retrbinary(downName, f.write)
		'''
        return


def ftpSearch(path, path2, name):
    ftp = FTP()
    ftp.connect("10.30.6.77", "29")
    ftp.login('ftpuser', 'abc@123456')
    ftp.cwd(path)
    ftpRecSearch(ftp, path2, name, 0, '')


def txtSearch(fileName):
    fileRead = open(fileName, 'r')
    # print 'hello'
    global count
    for line in fileRead:
        # print 'search:' + line
        count = 0
        ftpSearch('.', '.', line[:-2])
        # print 'count:' + str(count)
        if count == 0:
            fileNo.writelines(line)


def ftpInit(path):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect("10.30.6.77", "29")
    ftp.login('ftpuser', 'abc@123456')
    # print ftp.getwelcome()
    pathMK = path + '/IPC/Tool/src'
    if not os.path.exists(pathMK):
        os.makedirs(pathMK)
#	createSH(path)
    os.chdir(pathMK)
    ftp.cwd('Eos')
    ftpRec(ftp, path)


'''
	os.chdir('..')
	if not os.path.exists('dist'):
		os.makedirs('dist')
	os.system('chmod 777 checkApp_new.sh')
	os.system('sh ./checkApp_new.sh')
	os.chdir('dist')
	ftpUP(path)'''

'''
	ftp.cwd("Nova2")
	ftpList = ftp.nlst()
	ftpDir = ftp.dir()
	##print ftpDir
	##print type(ftpDir)
	for i in ftpList:
		ftpRec(ftp, i)
		##print i
		downName = 'RETR ' + i
		f = open(i, 'wb')'''
#		ftp.retrbinary(downName, f.write)


if len(sys.argv) == 4:
    # print '4'
    if (sys.argv[1] == 'down'):
        ftpDown(sys.argv[2], sys.argv[3])
    elif (sys.argv[1] == 'sh'):
        createSH(sys.argv[2], sys.argv[3])
elif len(sys.argv) == 5:
    # print '5'
    if (sys.argv[1] == 'search'):
        ftpSearch(sys.argv[2], sys.argv[3], sys.argv[4])
elif len(sys.argv) == 3:
    # print '3'
    if (sys.argv[1] == 'up'):
        ftpUP(sys.argv[2])
    elif (sys.argv[1] == 'txtSearch'):
        txtSearch(sys.argv[2])
    elif sys.argv[1] == 'downByFileList':
        ftpDownByTxtName(sys.argv[2])
