import ListPath
import os

class CpPic(object):
    pats = ['1pon', 'carib', 'fc2ppv', 'hey', 'orex', 'tokyohot', 'musume']
    def __init__(self, base):
        self.base = base
        
    def test(self):
        lp = ListPath.ListPath(self.base)
        allFile = lp.getAllFile()
        self.cpPic(allFile)
        
    def isInPat(self, name):
        for pat in self.pats:
            if pat in name:
                return True
        
        return False
        
    def cpPic(self, allFile):
        os.chdir(self.base)
        if not os.path.exists('un'):
            os.mkdir('un')
        for filename in allFile:
            findname = filename.lower()
            if self.isInPat(findname):
                bname = os.path.basename(filename)
                dstname = os.path.join('un', bname)
                cmdStr = 'copy %s %s' % (filename, dstname)
                print(cmdStr)
                os.system(cmdStr)
            

if __name__ == '__main__':
    cp = CpPic(r'G:\github\npm\electron-quick-start\data')
    cp.test()