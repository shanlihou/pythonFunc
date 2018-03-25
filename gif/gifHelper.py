#coding=utf8
import threading
Lock = threading.Lock()
import math
from lzw import lzw
class gifHelper(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(gifHelper, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance
    def __init__(self):
        self.count = 0
        self.bit = 0
        self.curByte = 0
        self.masks = [0x0000, 0x0001, 0x0003, 0x0007, 0x000f, 0x001f, 0x003f, 0x007f, 0x00ff, 0x01ff, 0x03ff, 0x07ff, 0x0fff]
    def get2(self, num):
        bit = 128
        strRet = ''
        while bit:
            tmp = num % bit
            strRet += str(num / bit)
            num = tmp
            bit /= 2
        return strRet
    def fFetch(self, fRead, num):
        use = 0
        ret = 0
        while use < num:
            if self.bit == 0:
                self.curByte = ord(fRead.read(1))
            right = self.bit
            mid = 8 - right
            left = 0
            if mid + use > num:
                mid = num - use
                left = 8 - right - mid
            #print left, mid, right, self.get2(self.curByte), use, ret
            ret = (((self.curByte & self.masks[right + mid] & (~self.masks[right])) >> right) << use) + ret
            self.bit = right + mid
            if self.bit == 8:
                self.bit = 0
            use += mid
        #print 'ret:', ret
        return ret

    def parseFF(self, fRead):
        print 'parseFF-----------------------------------------------------------'
        block_size = ord(fRead.read(1))
        print block_size
        tmp = fRead.read(block_size)
        print tmp
        strRet = ''
        while 1:
            tmp = fRead.read(1)
            if ord(tmp) != 0:
                strRet += tmp
                continue
            else:
                tmp = fRead.read(1)
                if ord(tmp) == 0:
                    strRet += tmp
                    continue
                
                for i in strRet:
                    print self.get2(ord(i))
                return tmp
    def parseF9(self, fRead):
        print 'parseF9-----------------------------------------------------------'
        block_size = ord(fRead.read(1))
        print block_size
        tmp = fRead.read(block_size)
        print self.get2(ord(tmp[0]))
        print ord(tmp[1]) + ord(tmp[2]) * 256
        print ord(tmp[3])
        tmp = fRead.read(1)
        print ord(tmp)
        return fRead.read(1)
    def parseImage(self, fRead):
        print 'parseImage-----------------------------------------------------------'
        tmp = fRead.read(9)    
        print ord(tmp[0]) + ord(tmp[1]) * 256
        print ord(tmp[2]) + ord(tmp[3]) * 256
        print ord(tmp[4]) + ord(tmp[5]) * 256
        print ord(tmp[6]) + ord(tmp[7]) * 256
        print self.get2(ord(tmp[8]))
        
        pixel = ord(tmp[8]) & 0x7
        pixel_size = int(math.pow(2, pixel + 1))
        m = ord(tmp[8]) & 0x80
        print 'pixel', pixel_size
        if m == 0x80:
            tmp = fRead.read(3 * pixel_size)
             
        self.bit = 0
        BitsPerPixel = ord(fRead.read(1))
        ClearCode = int(math.pow(2, BitsPerPixel))
        EOFCode = ClearCode + 1
        RunningCode = EOFCode + 1
        RunningBits = BitsPerPixel + 1
        Code1 = int(math.pow(2, RunningBits))
        StackPtr = 0
        LastCode = 4098;
        CrntShiftState = 0
        rntShiftDWord = 0
        print BitsPerPixel, ClearCode
        dictCode = [0] * 4096
        for i in range(ClearCode):
            dictCode[i] = chr(i)
        size = ord(fRead.read(1))
        tell1 = fRead.tell()
        print 'size:', size
        #output = dictCode[cur]
        output = ''
        cur = self.fFetch(fRead, RunningBits)
        while cur != EOFCode:
            if cur == ClearCode:
                pre = 0
                RunningCode = EOFCode + 1
                RunningBits = BitsPerPixel + 1
                cur = self.fFetch(fRead, RunningBits)
                continue
            if RunningCode == EOFCode + 1:
                pass
            elif cur == RunningCode - 1:
                dictCode[RunningCode - 1] = pre + pre[0]
            else:
                #print dictCode
                #print dictCode[cur]
                #print pre, cur, RunningCode, RunningBits
                dictCode[RunningCode - 1] = pre + dictCode[cur][0]
            pre = dictCode[cur]
            #print pre, cur, RunningCode, RunningBits
            output += pre
            RunningCode += 1
            cur = self.fFetch(fRead, RunningBits)
            if RunningCode == (1 << RunningBits):
                RunningBits += 1
        print 'out len:', len(output)
        tell2 = fRead.tell()
        print 'tell:', tell1, tell2, tell2 - tell1

        strPrint = ''
        for i in output:
            if ord(i) == 0xfb:
                strPrint += '%d, ' % 0
            else:
                strPrint += '%d, ' % 1
        print strPrint
        #test start
        #enc = lzw(5, output)
        #enc.encode()
        #test end
        return fRead.read(1)
    def parseFlag(self, fRead):
        flag = fRead.read(1)
        while 1:
            print flag
            print len(flag)
            print '%x' % ord(flag)
            if flag == '!':
                flag = fRead.read(1)
                if ord(flag) == 0xff:
                    flag = self.parseFF(fRead)
                if ord(flag) == 0xf9:
                    flag = self.parseF9(fRead)
            elif flag == ',':
                flag = self.parseImage(fRead)
            elif flag == '\0':
                flag = fRead.read(1)
            elif flag == ';':
                print 'enter end'
                break
            else:
                break
                
    def parseGif(self, fileName):
        fileRead = open(fileName, 'rb')
        tmp = fileRead.read(6)
        print 'parse gif-------------------------------------------'
        print tmp   
        self.count += 6
        print 'count:', '%x' % self.count
        tmp = fileRead.read(7)
        print ord(tmp[0]) + ord(tmp[1]) * 256
        print ord(tmp[2]) + ord(tmp[3]) * 256
        for i in tmp[4:]:
            print self.get2(ord(i))
        pixel = ord(tmp[4]) & 0x7
        pixel_size = int(math.pow(2, pixel + 1))
        m = ord(tmp[4]) & 0x80
        print 'pixel', pixel_size
        self.count += 7
        print 'count:', '%x' % self.count
        if m == 0x80:
            tmp = fileRead.read(3 * pixel_size)
            index_ = tmp.find(',')
            while index_ != -1:
                print 'index:', index_
                index_tmp = tmp[index_+1:].find(',')
                if index_tmp == -1:
                    break
                index_ += 1 + index_tmp
            self.count += 3 * pixel_size
            print 'count:', '%x' % self.count
            print fileRead.tell()
        self.parseFlag(fileRead)
    
    def insertFrame(self, data, delayTime):
        #write f9
        self.fileWrite.write('!')
        self.fileWrite.write(chr(0xf9))
        self.fileWrite.write(chr(4))
        self.fileWrite.write(chr(5))
        strWrite = ''
        strWrite += chr(delayTime % 256)
        strWrite += chr(delayTime / 256)
        strWrite += chr(7)
        strWrite += chr(0)
        self.fileWrite.write(strWrite)
        
        
        #write img
        self.fileWrite.write(',')
        strWrite = ''
        strWrite += chr(self.XOffset % 256)
        strWrite += chr(self.XOffset / 256)
        strWrite += chr(self.YOffset % 256)
        strWrite += chr(self.YOffset / 256)
        strWrite += chr(self.width % 256)
        strWrite += chr(self.width / 256)
        strWrite += chr(self.height % 256)
        strWrite += chr(self.height / 256)
        strWrite += chr(0)
        self.fileWrite.write(strWrite)
        
        #write
        self.fileWrite.write(chr(4))
        enc = lzw(4, data)
        strEncode = enc.encode()
        wholeLen = len(strEncode)
        wLen = 0
        while wLen < wholeLen:
            if wholeLen - wLen > 255:
                self.fileWrite.write(chr(255))
                self.fileWrite.write(strEncode[wLen: wLen + 255])
                wLen += 255
            else:
                self.fileWrite.write(chr(wholeLen - wLen))
                self.fileWrite.write(strEncode[wLen:])
                wLen = wholeLen
        self.fileWrite.write(chr(0))
            
    def createGIF(self, fileName, imgList, width, height, XOffset, YOffset):
        self.fileWrite = open(fileName, 'wb')
        self.width = width
        self.height = height
        self.XOffset = XOffset
        self.YOffset = YOffset
        self.fileWrite.write('GIF89a')
        strWrite = ''
        strWrite += chr(width % 256)
        strWrite += chr(width / 256)
        strWrite += chr(height % 256)
        strWrite += chr(height / 256)
        strWrite += chr(0xa2)
        strWrite += chr(0)
        strWrite += chr(0)
        self.fileWrite.write(strWrite)
        #write 0
        self.fileWrite.write(chr(0xf7))
        self.fileWrite.write(chr(0xe9))
        self.fileWrite.write(chr(0xba))
        #write 1:red
        self.fileWrite.write(chr(0xea))
        self.fileWrite.write(chr(0x21))
        self.fileWrite.write(chr(0x19))
        #write 2:red
        self.fileWrite.write(chr(0xff))
        self.fileWrite.write(chr(0xae))
        self.fileWrite.write(chr(0x10))
        #write 3:brown
        self.fileWrite.write(chr(0x06))
        self.fileWrite.write(chr(0x86))
        self.fileWrite.write(chr(0x4d))
        #write 4:green
        self.fileWrite.write(chr(0x25))
        self.fileWrite.write(chr(0x86))
        self.fileWrite.write(chr(0xe4))
        #write 5:blue
        self.fileWrite.write(chr(0))
        self.fileWrite.write(chr(128))
        self.fileWrite.write(chr(255))
        #write 6:pink
        self.fileWrite.write(chr(255))
        self.fileWrite.write(chr(128))
        self.fileWrite.write(chr(255))
        #write 7:purple
        self.fileWrite.write(chr(64))
        self.fileWrite.write(chr(0))
        self.fileWrite.write(chr(128))
        
        for i in imgList:
            self.insertFrame(i, 50)
        self.fileWrite.write(';')
        self.fileWrite.close()
if __name__ == '__main__':
    pass