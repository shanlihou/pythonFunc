#coding=utf-8
import os
import sys
import re
import shutil
def merge(list1, list2):
    map(lambda x: list1.append(x), filter(lambda x: x not in list1, list2))
    return list1
def deleteEmpty(path):
    #print path
    pattern = re.compile(r'.+.(avi|mp4|mkv|wmv|vob|tdl|iso|xltd)$', re.I)
    listFormat = []
    for i in os.listdir(path):
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
        print('will delete:', path)
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
        print(e)
    lenToCp = len(cpList)
    if lenToCp > 0:
        if lenToCp < 5:
            print(cpList)
            #return
            for i in cpList:
                #help(os)
                shutil.move(i, 'e:\\889914\\video\\' + os.path.basename(i))
        else:
            print('len of %s is :%d' % (path, lenToCp))
if __name__ == '__main__':
    opt = 0
    if opt == 0:
        cp('e:\\')
        print('-' * 60)
        deleteEmpty('E:\\889914')
    elif opt == 1:
        if len(sys.argv) == 3:
            if sys.argv[1] == 'cp':
                cp(sys.argv[2])
            elif (sys.argv[1]) == 'del':
                deleteEmpty(sys.argv[2])
    elif opt == 2:
        pass