#coding=utf-8
import os
import sys
import re
import shutil
from log import logger
g_curPath = 'j:\\889914'
def merge(list1, list2):
    list(map(lambda x: list1.append(x), filter(lambda x: x not in list1, list2)))
    return list1
def deleteEmpty(path):
    #print path
    pattern = re.compile(r'.+.(avi|mp4|mkv|wmv|vob|tdl|iso|xltd|m2ts)$', re.I)
    listFormat = []
    pathList = list(os.listdir(path))
    for i in pathList:
        fileName = path + '\\' + i
        if os.path.isdir(fileName):
            listFormat = merge(listFormat, deleteEmpty(fileName))
        else:
            strFind = pattern.search(i)
            if(strFind):
                #print '\t', i
                if strFind.group(1) not in listFormat:
                    listFormat.append(strFind.group(1))
    #print listFormat
    if len(listFormat) == 0:
        print('will delete:', path, pathList)
        logger.warn('will delete:{}'.format(path))
        if 'Lucie' not in path:
            os.system('rd /s /q "' + path + '"')
    return listFormat
def joinPath(path, name):
    return path + name if path.endswith('\\') else path + '\\' + name
                
def cp(path):
    pattern = re.compile(r'.+.(avi|mp4|mkv|wmv)$', re.I)
    cpList = []
    try:
        for i in os.listdir(path):
            pathName = joinPath(path, i)
            if os.path.isdir(pathName):
                if i == 'video' or i == 'sort' or i == 'System Volume Information':
                    continue
                cp(pathName)
            else:
                strFind = pattern.search(i)
                if(strFind):
                    
                    cpList.append(joinPath(path, i))
                    #print(path + '\\' + i)
                    #shutil.move(path + '\\' + i, 'video\\' + i)
    except (Exception) as e:
        print('err end:', e)

    lenToCp = len(cpList)
    if lenToCp > 0:
        if lenToCp < 3:
            print(cpList)
            #return
            for i in cpList:
                #help(os)
                try:
                    videoName = os.path.join(g_curPath, 'video')
                    finalName = os.path.join(videoName, os.path.basename(i))
                    shutil.move(i, finalName)
                except Exception as e:
                    print(e)
        else:
            print('len of %s is :%d' % (path, lenToCp))
if __name__ == '__main__':
    opt = 0
    if opt == 0:
        cp(g_curPath)
        print('-' * 60)
        deleteEmpty(g_curPath)
    elif opt == 1:
        if len(sys.argv) == 3:
            if sys.argv[1] == 'cp':
                cp(sys.argv[2])
            elif (sys.argv[1]) == 'del':
                deleteEmpty(sys.argv[2])
    elif opt == 2:
        pass