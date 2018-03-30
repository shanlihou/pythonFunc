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
        tell = fRead.tell()
        block_size = ord(fRead.read(1))
        self.formatPrint(tell, tell + 1, block_size, 'block size')
        tell += 1
        
        tmp = fRead.read(block_size)
        self.formatPrint(tell, tell + 1, self.get2(ord(tmp[0])), 'res3:method3:i1:t1')
        tell += 1
        
        self.formatPrint(tell, tell + 2, ord(tmp[1]) + ord(tmp[2]) * 256, 'delay time') 
        tell += 2
        
        self.formatPrint(tell, tell + 1, ord(tmp[3]), 'transparent')
        tell += 1
        
        tmp = fRead.read(1)
        self.formatPrint(tell, tell + 1, ord(tmp), 'transparent')
        print '_' * 60
        return fRead.read(1)
    def getBytes2Num(self, fRead):
        return ord(fRead.read(1)) + ord(fRead.read(1)) * 256
        
    def parseImage(self, fRead):
        tell = fRead.tell()
        self.formatPrint(tell, tell + 2, self.getBytes2Num(fRead), 'x offset')
        tell += 2
        
        self.formatPrint(tell, tell + 2, self.getBytes2Num(fRead), 'y offset')
        tell += 2
        
        self.formatPrint(tell, tell + 2, self.getBytes2Num(fRead), 'width')
        tell += 2
        
        self.formatPrint(tell, tell + 2, self.getBytes2Num(fRead), 'height')
        tell += 2
        
        tmp = fRead.read(1)  
        self.formatPrint(tell, tell + 1, self.get2(ord(tmp)), 'm1:i1:s1:r2:pix3')
        tell += 1
          
        
        pixel = ord(tmp) & 0x7
        pixel_size = int(math.pow(2, pixel + 1))
        m = ord(tmp) & 0x80
        if m == 0x80:
            tmp = fRead.read(3 * pixel_size)
             
        self.bit = 0
        BitsPerPixel = ord(fRead.read(1))
        self.formatPrint(tell, tell + 1, BitsPerPixel, 'bits per pixel')
        tell + 1
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
        print fRead.tell()
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
                print 'cur:', cur
                print dictCode[cur]
                print RunningCode
                print fRead.tell()
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
            print '_' * 60
            tell = fRead.tell()
            if flag == '!':
                self.formatPrint(tell - 1, tell, '%02x' % ord(flag), 'flag')
                tell += 1
                
                flag = fRead.read(1)
                self.formatPrint(tell - 1, tell, '%02x' % ord(flag), 'flag')
                if ord(flag) == 0xff:
                    flag = self.parseFF(fRead)
                if ord(flag) == 0xf9:
                    flag = self.parseF9(fRead)
            elif flag == ',':
                self.formatPrint(tell - 1, tell, '%02x' % ord(flag), 'image')
                flag = self.parseImage(fRead)
            elif flag == '\0':
                flag = fRead.read(1)
            elif flag == ';':
                print 'enter end'
                break
            else:
                break
    def formatPrint(self, s, e, content, comment=''):
        if not isinstance(content, str):
            content = str(content)
        print '%8d-%8d|%20s|%20s|' % (s, e, content, comment)
    def parseGif(self, fileName):
        fileRead = open(fileName, 'rb')
        tmp = fileRead.read(6)
        print 'parse header-------------------------------------------'
        print '_' * 60   
        self.formatPrint(0, 6, tmp, 'ver')
        
        tmp = fileRead.read(7)
        self.formatPrint(6, 8, ord(tmp[0]) + ord(tmp[1]) * 256, 'width')
        self.formatPrint(8, 10, ord(tmp[2]) + ord(tmp[3]) * 256, 'height')
        
        comment = ['m1:cr3:s1:pixel3', 'bgColor', 'W:H']
        for i in xrange(3):
            self.formatPrint(i + 10, i + 11, self.get2(ord(tmp[i + 4])), comment[i])
        pixel = ord(tmp[4]) & 0x7
        pixel_size = int(math.pow(2, pixel + 1))
        m = ord(tmp[4]) & 0x80
        #print 'pixel', pixel_size
        if m == 0x80:
            tell = fileRead.tell()
            tmp = fileRead.read(3 * pixel_size)
            
            index_ = tmp.find(',')
            while index_ != -1:
                print 'index:', index_
                index_tmp = tmp[index_+1:].find(',')
                if index_tmp == -1:
                    break
                index_ += 1 + index_tmp
            self.formatPrint(tell, tell + 3 * pixel_size, 'rgb * %d' % pixel_size, 'pixel_table')
        print '_' * 60
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
    gif = gifHelper()
    gif.parseGif('box.gif')