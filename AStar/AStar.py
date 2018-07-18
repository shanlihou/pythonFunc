# coding=utf8
from _functools import reduce
import heapq
import random
import re

from jpg import display


def calcManhattan(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


class Point(object):
    def __init__(self, x, y, src, dst):
        self.x = x
        self.y = y
        self.src = src
        self.dst = dst
        self.dis = calcManhattan((x, y), self.dst) + calcManhattan((x, y), self.src)
        self.father = None
        self.son = None

    def update(self, x, y):
        self.x = x
        self.y = y
        self.dis = calcManhattan((x, y), self.dst) + calcManhattan((x, y), self.src)

    def __str__(self):
        return '%d, %d, %d' % (self.x, self.y, self.dis)

    def __lt__(self, other):
        return self.dis < other.dis

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def end(self):
        return self.x == self.dst[0] and self.y == self.dst[1]

    def setFather(self, other):
        self.father = other
        other.son = self

    def str(self):
        return self.__str__()


class PointList(list):
    def __init__(self):
        self.items = set()

    def pushback(self, point):
        heapq.heappush(self, point)
        self.items.add((point.x, point.y))

    def popMin(self):
        ret = heapq.heappop(self)
        self.items.remove((ret.x, ret.y))
        return ret

    def has(self, point):
        return (point.x, point.y) in self.items

    def __str__(self):
        large = heapq.nlargest(len(self), self)
        return reduce(lambda x, y: x + ':' + y.str(), large, '')


class AStar(object):
    def __init__(self, mapPath):
        self.mapPath = mapPath
        self.width = 8
        self.dir = [(0, 1), (-1, 0), (0, -1), (1, 0)]
        self.find = False

    def parseMap(self, mapPath):
        fileRead = open(mapPath, 'rb').read()
        spStr = '\\r\\n'
        fileRead = str(fileRead).split(spStr)
        self.mapList = filter(lambda x: x[0].isdigit(), fileRead)
        self.mapList = list(map(lambda x: x.split(','), self.mapList))

    def displayMap(self):
        x = 0
        for line in self.mapList:
            for y in range(len(line)):
                if line[y] == '1':
                    self.drawPoint(x, y, 0x882244)
            x += 1
        self.end = (10, 18)
        self.start = Point(10, 8, (10, 8), self.end)
        self.drawPoint(self.end[0], self.end[1], 0x598302)
        self.drawPoint(self.start.x, self.start.y, 0x598302)

    def getMapPoint(self, point):
        return self.mapList[point.x][point.y]

    def step(self):
        if self.find:
            return self.find
        cur = self.openList.popMin()
        print(cur)
        self.closeList.pushback(cur)
        for dirIter in self.dir:
            newPoint = Point(cur.x + dirIter[0], cur.y + dirIter[1], (self.start.x, self.start.y), self.end)

            if self.getMapPoint(newPoint) != '1' or self.closeList.has(newPoint):
                continue

            if newPoint.end():
                newPoint.setFather(cur)
                self.find = True
                self.endPoint = newPoint
                return self.find

            if not self.openList.has(newPoint):
                newPoint.setFather(cur)
                self.openList.pushback(newPoint)
            elif newPoint < cur:
                newPoint.setFather(cur)

        return self.find

    def calcPath(self):
        self.openList = PointList()
        self.closeList = PointList()
        self.openList.pushback(self.start)

    def drawPoint(self, x, y, color):
        display.display().drawPoint(x * self.width, y * self.width, color, self.width)

    def drawPath(self):
        cur = self.endPoint
        while cur != self.start:
            self.drawPoint(cur.x, cur.y, 0x123456)
            cur = cur.father

    def test(self):
        display.display()
        self.parseMap(self.mapPath)
        self.displayMap()
        self.calcPath()

        while(not self.find):
            self.step()

        self.drawPath()

        display.display().display()
        display.display().test()


if __name__ == '__main__':
    astart = AStar(
        r'E:\shtest\test.tmx')
    astart.test()
