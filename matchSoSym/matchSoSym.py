import os
import sys
class matchSoSym:
    def __init__(self, path, target):
        self.path = path
        self.target = target
    def getAllSo(self):
        #allSo = os.path.join(self.path, '*.so')
        cmdStr = 'ls ' + os.path.join(self.path, '*.so')
        print cmdStr
        cmd = os.popen(cmdStr)
        #print cmd.read()
        soFiles = cmd.read().split()
        return soFiles
    def getSym(self, name):
        cmdStr = 'arm-hisiv300-linux-nm  -C %s' % name
        cmd = os.popen(cmdStr).readlines()
        syms = map(lambda x: x.split()[-1],cmd)
        return syms
    def match(self):
        tgtSet = set(self.getSym(self.target))
        soFiles = self.getAllSo()
        mainSym = []
        for i in soFiles:
            if i == self.target:
                continue
            syms = self.getSym(i)
            matchSym = filter(lambda x: x in tgtSet, syms)
            if not matchSym:
                continue
            print i, ':'
            print matchSym
            mainSym.extend(matchSym)
        mainSet = list(set(mainSym))
        print 'main:'
        #print set(mainSym)
        strPrint = ''
        for i in xrange(len(mainSet)):
            strPrint += '%50s' % mainSet[i]
            if i % 4 == 3:
                strPrint += '\n'
        print strPrint
            
        
if __name__ == '__main__':
    match = matchSoSym(sys.argv[1], sys.argv[2])
    match.match()