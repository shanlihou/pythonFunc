import os
class bakFile(object):
    def __init__(self, bakFileName):
        self.bakFile = bakFileName
    def bak(self):
        fileRead = open(self.bakFile, 'r')
        for line in fileRead:
            name = line.replace('\r', '').replace('\n', '')
            print name
            listSh = ('cp ', name, ' ', name, '.JP4')
            shStr = ''.join(listSh)
            print shStr
            os.system(shStr)
    def revert(self):
        fileRead = open(self.bakFile, 'r')
        for line in fileRead:
            name = line.replace('\r', '').replace('\n', '')
            print name
            listSh = ('cp ', name, '.bak', ' ', name)
            shStr = ''.join(listSh)
            print shStr
            os.system(shStr)
        

bak = bakFile('/home/32355/lm5/JP_Proj/bak.txt')
bak.revert()    