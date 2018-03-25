class lzw(object):
    def __init__(self, bit, data):
        self.bit = bit
        self.data = data
        self.wbit = 0
        self.retData = ''
        self.single = 0
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
    def putBit(self, bit, code):
        #print 'put code start-----------------------:', bit, code
        while bit:
            #print 'first:'
            #print self.get2(self.single)
            #print self.get2(code)
            #print bit, self.wbit
            if self.wbit == 0:
                if bit >= 8:
                    self.single = self.masks[8] & code
                    bit -= 8
                    code = code >> 8
                    self.retData += chr(self.single)
                else:
                    self.single = code
                    self.wbit = bit
                    bit = 0
            else:
                right = self.wbit
                wholeBit = right + bit
                if wholeBit >= 8:
                    mid = 8 - right
                    left = 0 
                    bit -= mid
                    self.wbit = 0
                else:
                    mid = wholeBit - right
                    left = 8 - wholeBit
                    bit = 0
                    self.wbit = wholeBit
                #print 'second:'
                #print self.get2(self.single)
                #print self.get2(code)
                #print mid, right
                self.single += (code & self.masks[mid]) << right
                code = code >> mid
                if self.wbit == 0:
                    ##print self.single
                    self.retData += chr(self.single)
        if self.wbit == 8:
            self.wbit = 0
    def encode(self):
        dictCode = {}
        clearCode = 1 << self.bit
        runBits = self.bit + 1
        endCode = clearCode + 1
        runCode = endCode + 1
        for i in range(clearCode):
            dictCode[chr(i)] = i
        pre = ''
        self.putBit(runBits, clearCode)
        for i in self.data:
            if pre == '':
                pre = i
            else:
                strWhole = pre + i
                if dictCode.has_key(strWhole):
                    pre = strWhole
                else:
                    #print runCode
                    dictCode[strWhole] = runCode
                    self.putBit(runBits, dictCode[pre])
                    pre = i
                    runCode += 1
            if runCode > 1 << runBits:
                runBits += 1
        self.putBit(runBits, dictCode[pre])                     
        runCode += 1
        if runCode > 1 << runBits:
            runBits += 1      
        self.putBit(runBits, endCode) 
        strPrint = ''
        #print len(self.retData)
        count = 0
        for i in self.retData:
            strPrint += '%x ' % ord(i)
            count += 1
            if count == 16:
                count = 0
                strPrint += '\n'
        #print strPrint
        #print '%x' % ord(pre)
        return self.retData