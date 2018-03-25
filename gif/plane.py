import math
import random
from operator import pos
class plane(object):
    def __init__(self, count):
        self.mMap = [([0] * 256) for i in range(256)]
        self.mBox = [[0, 0, 0, 0, 0, 1, 4, 3, 2, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 0, 3, 0, 0, 2, 0, 0, 0, 0], [0, 3, 2, 1, 0, 0, 0, 3, 0, 0, 0, 1, 4, 3, 0], [4, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 2], [1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1], [2, 2, 2, 2, 2, 2, 2, 0, 4, 4, 4, 4, 4, 4, 4], [3, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3], [4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2], [0, 1, 2, 3, 0, 0, 0, 1, 0, 0, 0, 3, 4, 1, 0], [0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 4, 1, 2, 3, 0, 0, 0, 0, 0]]
        self.chess = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0], [0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]]
        self.route = [(4, 1), (4, 2), (4, 3), (3, 4), (2, 4), (1, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 10), (2, 10), (3, 10), (4, 11), (4, 12), (4, 13), (5, 14), (6, 14), (7, 14), (8, 14), (9, 14), (10, 13), (10, 12), (10, 11), (11, 10), (12, 10), (13, 10), (14, 9), (14, 8), (14, 7), (14, 6), (14, 5), (13, 4), (12, 4), (11, 4), (10, 3), (10, 2), (10, 1), (9, 0), (8, 0), (7, 0), (6, 0), (5, 0)]
        self.startPos = [[(13, 0), (13, 1), (14, 0), (14, 1)], [(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 13), (0, 14), (1, 13), (1, 14)], [(13, 13), (13, 14), (14, 13), (14, 14)]]
        self.gamePos = [(33, 30), (0, 41), (11, 8), (22, 19)]
        #self.chessPos = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]
        self.chessPos = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]
        self.chessGamePos = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]
        self.ran = 0
        self.curColor = 0
        self.go = 0
        self.imgList = []
        self.memberCount = count
        self.drawMap()
    def rollRan(self):
        self.ran = random.randint(1, 6)
        if self.ran == 6 and self.go == 0:
            self.go = 1
        return self.ran
    def getRan(self):
        return self.ran
    def goBack(self, gamePos, color):
        for i in range(self.memberCount):
            if i == color:
                continue
            for j in range(4):
                if gamePos == self.chessGamePos[i][j]:
                    self.chessPos[i][j] = -1
                    self.chessGamePos[i][j] = -1
                    self.drawChess(-1, j, i)
                    self.imgList.append(self.createFrame())
    def getGamePos(self, pos, color):
        if pos > -1 and pos < 42:
            start = self.gamePos[color][0]
            gamePos = (start + pos) % 44
            return gamePos
        else:
            return -1
    def fetchFirst(self):
        for i in range(self.memberCount):
            if self.chessPos[self.curColor][i] != -1 and self.chessPos[self.curColor][i] != 48:
                return i
        return -1
    def fetchFirstReady(self):
        for i in range(self.memberCount):
            if self.chessPos[self.curColor][i] == -1:
                return i
        return -1
        
    def getCurColor(self):
        return self.curColor
    def getGamePosColor(self, gamePos):
        for i in range(self.memberCount):
            for j in range(4):
                if self.chessGamePos[i][j] == gamePos:
                    return i, j
        return None
    def getSameColor(self, pos, color):
        if pos == -1:
            return -1
        for i in range(4):
            if self.chessPos[color][i] == pos:
                return i
        return -1
        
    def doMove(self, num, done = False):
        curPos = self.chessPos[self.curColor][num]
        if curPos == 48:
            return None
    def isEnd(self, color):
        for i in self.chessPos[color]:
            if i != 48:
                return False
        return True
    
    def goChess(self, num, step = 0):
        if step == 0:
            step = self.ran
        print 'start:', self.curColor, step, '------------------------------------'
        print 'chessPos:', self.chessPos, '\nchessGamePos:\n', self.chessGamePos
        curPos = self.chessPos[self.curColor][num]
        if self.go == 0:
            if curPos == -1 or curPos == 48:
                num = self.fetchFirst()
                if num == -1:
                    self.curColor = (self.curColor + 1) % self.memberCount
                    self.rollRan()
                    return None, 2
        elif self.go == 1:
            if curPos == -1:
                self.go = 2
                self.rollRan()
                return None, 3
            elif curPos == 48:
                num = self.fetchFirstReady()
                if num != -1:
                    self.go = 2
                    self.rollRan()
                    return None, 3
                num = self.fetchFirst()
                self.got = 0
        elif self.go == 2:
            if curPos != -1:
                num = self.fetchFirstReady()
                self.go = 0
                
        curPos = self.chessPos[self.curColor][num]
        endPos = curPos         
        self.imgList = []
        endPos += step
        print 'endPos:', endPos
        self.chessGamePos[self.curColor][num] = -1
        if endPos > -1 and endPos < 42:
            self.chessPos[self.curColor][num] = endPos
            self.drawMove(curPos, step, num, self.curColor)
            start = self.gamePos[self.curColor][0]
            pos = (start + endPos) % 44
            tmpX = self.route[pos][0]
            tmpY = self.route[pos][1]
            #print self.mBox[tmpX][tmpY], self.curColor + 1, tmpX, tmpY
            if self.mBox[tmpX][tmpY] == self.curColor + 1 and tmpX != 7 and tmpY != 7:
                endPos += 4
                pos = (pos + 4) % 44
                tmp = self.getGamePosColor(pos)
                self.chessPos[self.curColor][num] = endPos
                if tmp:
                    self.drawChess(self.chessPos[tmp[0]][tmp[1]], tmp[1], tmp[0])
                else:
                    self.drawChess(endPos - 4, num, self.curColor, 1)
                self.drawChess(endPos, num, self.curColor, 0)
                self.imgList.append(self.createFrame())
            self.goBack(pos, self.curColor)
            self.chessGamePos[self.curColor][num] = pos
            self.chessPos[self.curColor][num] = endPos
        else:
            self.chessGamePos[self.curColor][num] = -1  
            if endPos > 48:
                self.chessPos[self.curColor][num] = 48
                self.drawMove(curPos, 48 - curPos, num, self.curColor)
                endPos = 48 * 2 - endPos
                self.chessPos[self.curColor][num] = endPos
                self.drawMove(48, 48 - endPos, num, self.curColor, True)
            else:
                self.chessPos[self.curColor][num] = endPos
                self.drawMove(curPos, step, num, self.curColor)
        print 'end:', self.chessPos[self.curColor][num], self.chessGamePos[self.curColor][num]
        if (self.isEnd(self.curColor)):
            return self.imgList, 0
        if step != 6:
            self.curColor = (self.curColor + 1) % self.memberCount
        self.go = 0
        self.rollRan()      
        print 'end:', self.curColor
        print 'chessPos:', self.chessPos, '\nchessGamePos:\n', self.chessGamePos
        return self.imgList, 1
    
    def drawMove(self, pos, step, num, color, reverse = False):
        for i in range(step):
            gamePos = self.getGamePos(pos + i, color)
            #print pos, gamePos, step, num, color, reverse
            if gamePos != -1:
                tmp = self.getGamePosColor(gamePos)
                if tmp:
                    print self.chessPos[tmp[0]][tmp[1]], tmp[1], tmp[0], gamePos, '----------------------------------------'
                    self.drawChess(self.chessPos[tmp[0]][tmp[1]], tmp[1], tmp[0])
                else:
                    self.drawChess(pos + i, num, color, 1)
            elif reverse:
                self.drawChess(pos - i, num, color, 1)
            else:
                self.drawChess(pos + i, num, color, 1)
            if reverse:
                self.drawChess(pos - i - 1, num, color, 0) 
            else:
                self.drawChess(pos + i + 1, num, color, 0) 
            self.imgList.append(self.createFrame())
    def drawMap(self):
        for i in range(15):
            for j in range(15):
                self.drawBox(i, j, self.mBox[i][j])
        for i in range(self.memberCount):
            for j in range(4):
                self.drawChess(self.chessPos[i][j], j, i, 0)
    def drawChess(self, pos, num, color, erase = 0):
        if pos == -1:
            x = self.startPos[color][num][0]
            y = self.startPos[color][num][1]
        elif pos < 42:
            start = self.gamePos[color][0]
            gamePos = (start + pos) % 44
            x = self.route[gamePos][0]
            y = self.route[gamePos][1]
        else:
            end = self.gamePos[color][1]
            x = self.route[end][0]
            y = self.route[end][1]
            if x == 0:
                x = pos - 41
            elif x == 14:
                x = 14 + 41 - pos
            if y == 0:
                y = pos - 41    
            elif y == 14:
                y = 14 + 41 - pos
                  
        if erase:
            tmpNum = self.getSameColor(pos, color)
            if tmpNum != -1:
                num = tmpNum
                color += 1
            else:
                color = 0
        else:
            color += 1
        for i in range(8):
            for j in range(8):
                if self.chess[num][(7 - j) * 8 + i] == 1:
                    self.mMap[x * 17 + 4 + i][y * 17 + 4 + j] = color
                else:
                    self.mMap[x * 17 + 4 + i][y * 17 + 4 + j] = 0                   
    def drawBox(self, x, y, value):
        if value < 7:
            for i in range(17):
                r = 5
                if i >= 8 - 5 and i <= 8 + 5:
                    tmp = 8 - math.sqrt(25 - (8 - i) * (8 - i))
                else:
                    tmp = 9
                for j in range(int(tmp)):
                    self.mMap[x * 17 + i][y * 17 + j] = value
                    self.mMap[x * 17 + i][y * 17 + 16 - j] = value                  
            return    
    def createAnimation(self):
        imgList = []
        for i in range(50):
            self.drawChess(i - 1, 2, 1, 0)
            imgList.append(self.createFrame()) 
        return imgList     
    def createFrame(self):
        strRet = ''
        for i in range(256):
            for j in range(256):
                strRet += chr(self.mMap[j][255 - i])
        return strRet
    def getRoute(self, pos, retList):
        dir = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        dir2 = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
        x = pos[0]
        y = pos[1]
        xEnd = pos[2]
        yEnd = pos[3]
        print 'path:', x, y
        retList.append((x, y))
        go = 0
        for i in range(4):
            tmpX = x + dir[i][0]
            tmpY = y + dir[i][1]
            if tmpX < 0 or tmpX > 14 or tmpY < 0 or tmpY > 14:
                continue
            if self.mBox[tmpX][tmpY] == 0:
                continue
            if self.mBox[tmpX][tmpY] == self.mBox[x][y]:
                continue
            if tmpX == xEnd and tmpY == yEnd:
                print 'end'
                return
            go = 1
            tmpColor = self.mBox[x][y]
            self.mBox[x][y] = 0
            self.getRoute((tmpX, tmpY, xEnd, yEnd), retList)
            self.mBox[x][y] = tmpColor
        if go == 1:
            return
        for i in range(4):
            tmpX = x + dir2[i][0]
            tmpY = y + dir2[i][1]
            if tmpX < 0 or tmpX > 14 or tmpY < 0 or tmpY > 14:
                continue
            if self.mBox[tmpX][tmpY] == 0:
                continue
            if self.mBox[tmpX][tmpY] == self.mBox[x][y]:
                continue
            if tmpX == xEnd and tmpY == yEnd:
                return
            tmpColor = self.mBox[x][y]
            self.mBox[x][y] = 0
            go = 1
            self.getRoute((tmpX, tmpY, xEnd, yEnd), retList)
            self.mBox[x][y] = tmpColor
        if go == 0:
            print 'end'
        
