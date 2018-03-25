import math
import random
class throwGame(object):
    def __init__(self, size):
        self.mMap = [([0] * 256) for i in range(256)]
        self.smile = [0 ,0 ,0 ,0 ,0 ,1 ,1 ,1 ,1 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,1 ,0 ,0 ,0 ,1 ,1 ,1 ,0 ,0 ,0 ,1 ,1 ,1 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,1 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,1 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,1 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
        self.bak = [0] * 258
        x = random.randint(128, 255 - size)
        y = random.randint(1, 254 - size)
        print 'x,y:', x, y
        self.size = size
        self.createBox(x, y)
        self.color = 2
    def createBox(self, x, y):
        for i in range(self.size):
            for j in range(self.size):
                if self.smile[(self.size - 1 - j) * self.size + i] == 1:
                    self.mMap[x + i][y + j] = 1
    def createImg(self):
        strRet = ''
        for i in range(256):
            for j in range(256):
                strRet += chr(self.mMap[j][255 - i])
        return [strRet]
        
    def calc(self):
        self.v1 =  math.sqrt(17) / math.sqrt(self.deice * self.deice + 1)
        self.v2 = self.deice * self.v1
        self.v1 = self.v1 * self.percent / 100
        self.v2 = self.v2 * self.percent / 100
        print 'v:', self.v1, self.v2
    def func(self, x):
        x = x - self.c
        x = x / self.v1
        return x * x / (-64) + self.v2 * x
    def recover(self):
        x = self.bak[256]
        y = self.bak[257]
        for i in range(self.size):
            for j in range(self.size):
                if x + i < 0 or x + i > 255 or y + j < 0 or y + j > 255:
                    continue
                self.mMap[x + i][y + j] = self.bak[(self.size - 1 - j) * self.size + i]
    def getFrame(self, times, color):
        y = int(self.func(times))
        #print times, y
        if y > 255:
            y = 255
        if y < 0:
            y = 0
        #print times, y
        ret = 1
        self.mMap[times][y] = color
        #test------------
        times = times - 8
        y = y - 8      
        self.bak[256] = times
        self.bak[257] = y
        for i in range(self.size):
            for j in range(self.size):
                if times + i < 0 or times + i > 255 or y + j < 0 or y + j > 255:
                    continue
                if self.mMap[times + i][y + j] == 1 and self.mMap[times + i][y + j] == 1:
                    ret = 0
                self.bak[(self.size - 1 - j) * self.size + i] = self.mMap[times + i][y + j]
                self.mMap[times + i][y + j] = self.smile[(self.size - 1 - j) * self.size + i]
        #test end--------------
        strRet = ''
        for i in range(256):
            for j in range(256):
                strRet += chr(self.mMap[j][255 - i])
        return strRet, ret
    def throw(self, angle, percent, c, jump = 10):
        self.deice = math.tan(angle * math.pi / 180)
        self.percent = percent
        self.c = c
        self.calc()
        imgList = []
        ret = 1
        for i in range(256):
            img, tmp = self.getFrame(i, self.color)
            if i % jump == 0:
                imgList.append(img)
            self.recover()
            ret *= tmp
        self.color += 1
        if self.color == 7:
            return imgList, 2
        else:
            return imgList, ret