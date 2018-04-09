import xml.dom.minidom
import os
import re
import sys
class compile(object):
    def __init__(self, path, src, name):
        self.path = path
        self.src = src
        self.name = name
        self.dom = xml.dom.minidom.parse(self.path + 'DependInfo.xml')
        self.root = self.dom.documentElement
    def getBySvn(self):
        sons = self.root.getElementsByTagName('Module')
        for i in sons:
            if i.getAttribute('url') == self.name:
                return i
    def getVer(self):
        mod = self.getBySvn()
        return mod.getAttribute('revision')
    def rmLib(self, libs):
        retStr = ''
        for i in libs:
            retStr += 'rm ' + i.getAttribute('generatedfolder') + '/' + i.getAttribute('name') + '\n'
        return retStr
    def cpLib(self, libs):
        retStr = ''
        for i in libs:
            retStr += ' ' * 8 + 'cp ' + i.getAttribute('generatedfolder') + '/' + i.getAttribute('name') + ' ' + self.path + i.getAttribute('targetfolder') + '\n'
        return retStr
    def getFirstLib(self, libs):
        return libs[0].getAttribute('generatedfolder') + '/' + libs[0].getAttribute('name')
    def getInfo(self):
        fileWrite = open('compile.sh', 'w')
        mod = self.getBySvn()
        makeStr = mod.getAttribute('makecmd')
        sons = mod.getElementsByTagName('Library')
        packStr = '#!/bin/sh\n'
        packStr += 'cd ' + self.src + '\n'
        packStr += 'date >> make.txt\n'
        packStr += self.rmLib(sons)
        packStr += makeStr + '\ncd -\n'
        packStr += 'if [ -f ' + self.getFirstLib(sons) + ' ]\n'
        packStr += 'then\n'
        packStr += self.cpLib(sons)
        packStr += 8 * ' ' + 'cd ' + self.path + '\n'
        packStr += ' ' * 8 + 'make pack\n' + ' ' * 8 + 'cd -\nfi\n'
        packStr += 'date >> make.txt\n'
        fileWrite.write(packStr)
        os.system('sh compile.sh')
        print packStr
def test():
    comp = compile('/home/32355/lm5_2/PROJ/', '/home/32355/pll/manager/Trunk/', 'Manager')
    comp.getInfo()
def getCurSvn():
    result = os.popen('svn info').read()
    pattern = re.compile(r'URL: (\S+)')
    find = pattern.search(result)
    if find:
        return find.group(1)
if __name__ == '__main__':
    if sys.argv[1] == '-v':
        curDir = os.getcwd()
        svn = getCurSvn()
        comp = compile(sys.argv[2], curDir, svn)
        ver = comp.getVer()
        print ver
    '''
    curDir = os.getcwd()
    print curDir
    result = os.popen('svn info').read()
    pattern = re.compile(r'URL: (\S+)')
    find = pattern.search(result)
    if find:
        print find.group(1)
    
    '''