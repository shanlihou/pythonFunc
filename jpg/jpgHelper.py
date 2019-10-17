# coding=utf8

from math import *
from display import display
from memoize import memoize


@memoize
def C(x):
    if x == 0:
        return 1.0 / sqrt(2.0)
    else:
        return 1.0


class MCU(object):
    def __init__(self, numColor):
        self.numColor = numColor
        self.mcus = [None] * numColor

    def getHmultiVs(self, index):
        return self.mcus[index]

    def __repr__(self):
        one = len(self.mcus)
        two = len(self.mcus[0])
        three = len(self.mcus[0][0])
        return 'YCrCb:{}, HmultiV:{}, 3:{}'.format(one, two, three)


class jpgHelper(object):
    def __init__(self, fileName):
        # pre argu
        self.idct_precision = 8
        # --------------------------
        self.fileRead = open(fileName, 'rb')
        self.huffmanTbl = {}
        self.huffmanTbl['dc'] = [None] * 2
        self.huffmanTbl['ac'] = [None] * 2
        self.EOI = False
        self.data = []
        self.colorInfo = None
        self.numColor = 0
        self.quantTable = [None] * 4
        self.zigMap = [[0,  1,  5,  6, 14, 15, 27, 28],
                       [2,  4,  7, 13, 16, 26, 29, 42],
                       [3,  8, 12, 17, 25, 30, 41, 43],
                       [9, 11, 18, 24, 31, 40, 44, 53],
                       [10, 19, 23, 32, 39, 45, 52, 54],
                       [20, 22, 33, 38, 46, 51, 55, 60],
                       [21, 34, 37, 47, 50, 56, 59, 61],
                       [35, 36, 48, 49, 57, 58, 62, 63]]

        self.idctTable = [[(C(u) * cos(((2.0 * x + 1.0) * u * pi) / 16.0))
                           for x in range(self.idct_precision)] for u in range(self.idct_precision)]

    def get2(self, num):
        bit = 128
        strRet = ''
        while bit:
            tmp = num % bit
            strRet += str(num / bit)
            num = tmp
            bit /= 2
        return strRet

    def readBit(self):
        FF = False
        tmp = self.fileRead.read(1)[0]
        while not self.EOI:
            num = tmp
            if FF:
                if num == 0:
                    num = 0xff
                    FF = False
                    tmp = self.fileRead.read(1)[0]
                elif num == 0xD9:
                    self.EOI = True
                    break
                elif num >= 0xD0 and num < 0xD8:
                    tmp = self.fileRead.read(1)[0]
                    FF = False
                    print('find flag:%x' % num)
                    continue
                else:
                    tmp = self.fileRead.read(1)[0]
                    continue
                '''
                elif num == 0xff:
                    tmp = self.fileRead.read(1)[0]
                    continue
                '''
            else:
                tmp = self.fileRead.read(1)[0]
                if num == 0xff:
                    FF = True
                    continue

            for i in range(7, -1, -1):
                yield (num >> i) & 0x01
        while True:
            yield None

    def readStream(self, bits):
        ret = 0
        for i in range(bits):
            bit = next(self.inputStream, None)
            if bit is not None:
                ret = (ret << 1) + bit
            else:
                return None
        return ret

    def parseHuffmanTbl(self, seq):
        first = seq[0]
        H1 = (0xf0 & first) >> 4
        L1 = 0x0f & first
        tmpTbl = {}
        code = 0
        index = 17
        count = 0
        for i in range(1, 17):
            num = seq[i]
            count += num
            # print i, num, index, count
            for j in range(num):
                # print 'index:', i, j, num, index, len(seq)
                tmpTbl[(i, code)] = seq[index]
                index += 1
                code += 1
            code <<= 1
        print(L1)
        if H1 == 0:
            self.huffmanTbl['dc'][L1] = tmpTbl
        else:
            self.huffmanTbl['ac'][L1] = tmpTbl

    def decodeHuffman(self):
        bit = 0
        key = 0
        while 1:
            bit += 1
            key = (key << 1) + self.readStream(1)
            # if
            break

    def decodeKey(self, keyLen, key):
        if key & (1 << (keyLen - 1)):
            return key
        else:
            return key - ((1 << keyLen) - 1)

    def readDataUnit(self, colorId):
        # print colorId
        # print self.huffmanNo
        data = []
        dc = False
        huffTable = self.huffmanTbl['dc'][self.huffmanNo[colorId]['dc']]
        huffAcTable = self.huffmanTbl['ac'][self.huffmanNo[colorId]['ac']]
        keyLen = 0
        while len(data) < 64 and not self.EOI:
            num = 0
            bit = 0
            while not self.EOI:
                bit += 1
                nextBit = self.readStream(1)
                if nextBit is None:
                    print('end')
                    return [0 for i in range(64)]
                num = (num << 1) + nextBit
                if (bit, num) in huffTable:
                    keyLen = huffTable[(bit, num)]
                    break
            if keyLen == 0xf0:
                data.extend([0] * 16)
                continue
            if not dc:
                key = self.readStream(keyLen)
                # print 'keyLen:', keyLen, 'key:', key
                if keyLen != 0:
                    key = self.decodeKey(keyLen, key)
                else:
                    print('error keyLen:%x' % keyLen)
                data.append(key)
                # print 'huffTable:', huffTable
                # print 'bit:', bit, 'num:', num, 'keyLen:', keyLen, 'data:',
                # data
                dc = True
                huffTable = huffAcTable
            else:
                if keyLen == 0:
                    lenData = len(data)
                    data.extend([0] * (64 - lenData))
                    break
                zeroNum = (keyLen >> 4) & 0x0f
                keyLen &= 0x0f
                data.extend([0] * zeroNum)
                key = self.readStream(keyLen)
                # print 'key len:', keyLen, 'zero:', zeroNum
                if keyLen != 0:
                    key = self.decodeKey(keyLen, key)
                else:
                    print('error ac keyLen:%x %x' % (keyLen, zeroNum))
                data.append(key)
                if len(data) == 12 and data[11] == -80:
                    print('-' * 80, data[11])
        # print data
        if len(data) > 64:
            # TODO:why here is out of 64
            data = data[0:64]
            print(len(data), data)
        return data

    def readMCU(self):
        mcu = MCU(self.numColor)
        for i in range(self.numColor):
            hori = self.colorInfo[i + 1]['horizontal']
            vert = self.colorInfo[i + 1]['vertical']
            mcu.mcus[i] = []
            for j in range(hori * vert):
                print(i, j)
                mcu.mcus[i].append(self.readDataUnit(i + 1))
        return mcu

    def for_each_data_unit(self, type):
        for mcu in self.data:
            for YCrCb in mcu.mcus:
                if type == 'deZig':
                    self.deZig(YCrCb)
                elif type == 'idct':
                    self.idct(YCrCb)

    def calcDC(self):
        prev = 0
        for mcu in self.data:
            print(mcu)
            for YCrCb in mcu.mcus:
                for HmultiV in YCrCb:
                    if HmultiV:
                        HmultiV[0] += prev
                        prev = HmultiV[0]

    def dequantify(self):
        for mcu in self.data:
            for YCrCb in range(mcu.numColor):
                id = self.colorInfo[YCrCb + 1]['Quant']
                qTable = self.quantTable[id]
                for HmultiV in mcu.getHmultiVs(YCrCb):
                    for index in range(len(HmultiV)):
                        # print index, len(HmultiV), len(qTable)
                        HmultiV[index] *= qTable[index]

    def deZig(self, YCrCb):
        for index in range(len(YCrCb)):
            if not YCrCb[index]:
                continue
            tmp = [list(range(8)) for i in range(8)]
            for i in range(8):
                for j in range(8):
                    tmp[i][j] = YCrCb[index][self.zigMap[i][j]]
            YCrCb[index] = tmp

    def idct(self, YCrCb):
        for index in range(len(YCrCb)):
            tmp = [list(range(8)) for i in range(8)]
            if len(YCrCb[index]) == 0:
                continue
            for x in range(8):
                for y in range(8):
                    sum = 0

                    # Iterate over every coefficient
                    # in the DU
                    for u in range(self.idct_precision):
                        for v in range(self.idct_precision):
                            sum += YCrCb[index][v][u] * \
                                self.idctTable[u][x] * self.idctTable[v][y]

                    tmp[y][x] = sum // 4
            YCrCb[index] = tmp

    def test(self):
        display().displayData(self.data, 3)
        '''
        print 'data len:', len(self.data)
        offset = 0
        step = 3
        for mcu in self.data:
            print '\t', len(mcu)
            for YCrCb in mcu:
                print '\t' * 2, len(YCrCb)
                for k in YCrCb:
                    print '\t' * 3, len(k)
                    if len(k) == 0:
                        continue
                    self.displayUnit(offset, 0, k, step)
                    offset += 8 * step + 1
        '''

    def reverse(self, data, deep):
        if type(data) != list:
            return
        print('\t' * deep, len(data))
        for i in data:
            self.reverse(i, deep + 1)

    def printSum(self):
        self.reverse(self.data, 0)

    def displayUnit(self, offsetX, offsetY, unit, step=1):
        for x in range(8):
            for y in range(8):
                red = unit[x][y] + 128
                if red < 0:
                    red = 0
                elif red > 255:
                    red = 255
                # print red
                display().drawPoint(offsetX + x * step, offsetY + y * step, (red, 0, 0), step)

    def parseSOF(self):
        # sofo start of frame
        print('parseSOF---------------------------------------')
        tmp = self.fileRead.read(2)
        size = tmp[0] * 256 + tmp[1]
        print('size:', size)
        tmp = self.fileRead.read(6)
        print(tmp[0])
        print('image high:', tmp[1] * 256 + tmp[2])
        print('image width:', tmp[3] * 256 + tmp[4])
        colorNum = tmp[5]
        self.colorInfo = [{} for i in range(colorNum + 1)]

        for i in range(colorNum):
            id = self.fileRead.read(1)[0]
            tmp = self.fileRead.read(1)[0]
            print('id:', id)
            self.colorInfo[id]['horizontal'] = (tmp >> 4) & 0x0f
            self.colorInfo[id]['vertical'] = tmp & 0x0f
            self.colorInfo[id]['Quant'] = self.fileRead.read(1)[0]
            print('hori:', self.colorInfo[id]['horizontal'],
                  'vert:', self.colorInfo[id]['vertical'])
            print('quant id:', self.colorInfo[id]['Quant'])

    def parseDHT(self):  # dht
        # dht huffman table
        print('parse DHT---------------------------------------')
        tmp = self.fileRead.read(2)
        size = tmp[0] * 256 + tmp[1]
        print('size:', size)
        tmp = self.fileRead.read(size - 2)
        print(self.get2(tmp[0]))
        count = 0
        for i in range(1, 17):
            count += tmp[i]
            # print i, count
        print('count:', count)
        self.parseHuffmanTbl(tmp)
        print(self.huffmanTbl)

    def parseDQT(self):
        # dqt Define Quantization Table
        print('parse DQT---------------------------------------')
        tmp = self.fileRead.read(2)
        size = tmp[0] * 256 + tmp[1]
        print('size:', size)
        tmp = self.fileRead.read(size - 2)
        print(tmp[0])
        id = tmp[0] & 0x0f
        tmpTable = []
        for i in range(64):
            tmpTable.append(tmp[i + 1])
        self.quantTable[id] = tmpTable

    def parseSOS(self):
        print('parseSOS---------------------------------------SOS')
        tmp = self.fileRead.read(2)
        size = tmp[0] * 256 + tmp[1]
        print('size:', size)
        #tmp = self.fileRead.read(size - 2)
        numColor = self.fileRead.read(1)[0]
        self.huffmanNo = [{} for i in range(numColor + 1)]
        print('huffNo:', self.huffmanNo)
        for i in range(numColor):
            id = self.fileRead.read(1)[0]
            tmp = self.fileRead.read(1)[0]
            dc = (tmp >> 4) & 0x0f
            ac = tmp & 0x0f
            print('id:', id, 'dc:', dc, 'ac:', ac)
            self.huffmanNo[id]['dc'] = dc
            self.huffmanNo[id]['ac'] = ac
        for i in range(3):
            print(self.get2(self.fileRead.read(1)[0]))
        self.inputStream = self.readBit()
        self.numColor = numColor  # color sum num

        while not self.EOI:
            print('not eoi')
            self.data.append(self.readMCU())
        self.calcDC()
        display().displayData(self.data, 7, 1)

        self.dequantify()
        display().displayData(self.data, 5, 1)

        self.for_each_data_unit('deZig')
        display().displayData(self.data, 1)

        self.for_each_data_unit('idct')

    def parseAPPn(self):
        print('parseAPPN---------------------------------------APPn')
        tmp = self.fileRead.read(2)
        size = tmp[0] * 256 + tmp[1]
        print('size:', size)
        tmp = self.fileRead.read(size - 2)

    def parseFlag(self):
        while 1:
            flag = self.fileRead.read(1)
            if not flag:
                break

            flag = flag[0]
            print('%x' % flag)
            if flag == 0xff:
                flag = self.fileRead.read(1)[0]
                print('%x' % flag)
                if flag == 0xdb:
                    self.parseDQT()
                elif flag == 0xc0:
                    self.parseSOF()
                elif flag == 0xc4:
                    self.parseDHT()
                elif flag == 0xda:
                    self.parseSOS()
                elif flag == 0xe1:
                    self.parseAPPn()
                else:
                    print('here 1')
                    break
            else:
                print('here 2')
                break

    def parser(self):
        tmp = self.fileRead.read(4)
        for i in tmp:
            print('%x' % i)
        tmp = self.fileRead.read(2)
        size = tmp[0] * 256 + tmp[1]
        print('size:', size)
        tmp = self.fileRead.read(size - 2)
        print(tmp[:5])
        print('ver:', str(tmp[5]) + '.' + str(tmp[6]))
        print(tmp[7])
        print('x:', tmp[8] * 256 + tmp[9])
        print('y:', tmp[10] * 256 + tmp[11])
        for i in tmp[12:]:
            print('%x' % i)
        self.parseFlag()
