import os
import platform
import sys
sysstr = platform.system()


def findInner(fileName, keyword):
    fileRead = open(fileName, 'rb')
    count = 0
    for line in fileRead:
        count += 1
        if keyword in str(line):
            print(fileName + ':' + str(count))
            if len(line) < 200:
                print(line)


def listDir(path, keyword, level, choice='-c'):
    pathList = os.listdir(path)
    for i in pathList:
        if sysstr == 'Windows':
            sonName = path + '\\' + i
        else:
            sonName = path + '/' + i
        if (os.path.isdir(sonName)):
            if i == '.svn' or i == '.vs':
                continue
            listDir(sonName, keyword, level + 1, choice)
        elif(sonName.endswith('.cpp') or sonName.endswith('.h') or sonName.endswith('.c') or sonName.endswith('.js')):
            findInner(sonName, keyword)
        elif sonName.endswith('.rar') or sonName.endswith('.o') or sonName.endswith('.a') or sonName.endswith('sonia'):
            continue
        else:
            if choice == '-a':
                findInner(sonName, keyword)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        listDir(sys.argv[1], sys.argv[2], 0)
    elif len(sys.argv) == 4:
        listDir(sys.argv[1], sys.argv[2], 0, '-a')
    else:
        listDir(r'E:\svn\Dev\Client',
                '61000089', 0, '-a')
        #listDir(r'E:\svn\Dev\Server\kbeWin\kbengine',
        print('end')
