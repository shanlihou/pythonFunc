import os
class symbolsLink(object):
    def __init__(self, cross):
        self.cross = cross
    def readNM(self, fileName):
        cmd = self.cross + 'nm -D ' + fileName + '>./nm.txt'
        os.system(cmd)
        fileRead = open('nm.txt', 'r')
        lineList = fileRead.readlines()
        retList = map(lambda x:x.replace('\n', '').replace('\r', '').split(' ')[-1], lineList)
        #print retList
        return retList
    def findAnd(self, list1, list2):
        retList = filter(lambda x:x in list2, list1)
        print 'final:\n\n\n'
        for i in retList:
            print i
        return retList
sb = symbolsLink('arm-hisiv500-linux-uclibcgnueabi-')
list1 = sb.readNM('Libs/sys_hi3519/libhoneywellCrypto.so')
list2 = sb.readNM('Libs/sys_hi3519/libpdi.so.bak')
sb.findAnd(list1, list2)