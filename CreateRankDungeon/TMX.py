from _testcapi import raise_exception
from ast import parse
import math
import random
import xml.sax
import copy


class TmxHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.curTag = ''
        self.mapInfo = {}

    def startElement(self, tag, attrs):
        self.curTag = tag
        if tag == 'map':
            for k, v in attrs.items():
                self.mapInfo[k] = v

    def endElement(self, name):
        self.curTag = ''
        xml.sax.ContentHandler.endElement(self, name)

    def characters(self, content):
        if self.curTag == 'data':
            self.mapData = content
        xml.sax.ContentHandler.characters(self, content)


class TMX(object):
    def __init__(self, path, id):
        self.id = id
        self.path = path
        self.width = 9
        self.dir = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.turnMap = None
        self.turnFunc = [None,
                         lambda x, y: (31 - y, x),
                         lambda x, y: (31 - x, 31 - y),
                         lambda x, y: (y, 31 - x)]

    def init(self):
        self.turnMap = None

    def getMap(self):
        fileRead = open(self.path, 'rb').read()
        spStr = '\\r\\n'
        fileRead = str(fileRead).split(spStr)
        self.mapList = filter(lambda x: x[0].isdigit(), fileRead)
        self.mapList = list(
            map(lambda x: list(filter(lambda x: x, x.split(','))), self.mapList))

    def getMapFromData(self, data):
        print(len(data))

    def getDoor(self):
        pos = (0, 0)
        hw = (self.h, self.w)
        door = []
        for i, d in enumerate(self.dir):
            length = hw[i % 2]
            count1 = 0
            pos = (pos[0] - d[0], pos[1] - d[1])
            for off in range(length):
                pos = (pos[0] + d[0], pos[1] + d[1])
                if self.mapList[pos[0]][pos[1]] == '1':
                    count1 += 1

            door.append(True if count1 >= 4 else False)
        self.door = door

    def parseXml_old(self):
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        handler = TmxHandler()
        parser.setContentHandler(handler)
        parser.parse(self.path)
        self.w = int(handler.mapInfo['width'])
        self.h = int(handler.mapInfo['height'])
        print(self.w, self.h)

    def parseMap(self):
        with open(self.path) as fr:
            w, h = fr.readline().split()
            self.w = int(w)
            self.h = int(h)

            mapStr = fr.readlines()
            mapList = map(lambda x: x.replace('\n', '').split(), mapStr)
            mapList = list(filter(lambda x: x, mapList))
            print(mapList)
            self.mapList = mapList

    def displayMap(self):
        x = 0
        if len(self.mapList) != self.h:
            print('error')

        for line in self.mapList:
            if len(line) != self.w:
                print('error:', len(line), self.w)
            for y in range(len(line)):
                if line[y] == '1':
                    self.drawPoint(x, y, 0x882244)
                else:
                    self.drawPoint(x, y, 0x123456)
            x += 1

    def drawPoint(self, x, y, color):
        pass
        # display.display().drawPoint(x * self.width, y * self.width, color, self.width)

    def x2y(self):
        newMap = []
        for x, line in enumerate(self.turnMap):
            newLine = []
            for y in range(len(line)):
                newLine.append(self.turnMap[y][x])
            newMap.append(newLine)

        self.turnMap = newMap

    def getTurnMap(self, angle):
        if self.turnMap:
            return

        newMap = []
        if not angle:
            self.turnMap = copy.copy(self.mapList)
            self.turnMap.reverse()
            self.x2y()
            return

        func = self.turnFunc[angle // 90]
        for x, line in enumerate(self.mapList):
            newLine = []
            for y in range(len(line)):
                xx, yy = func(x, y)
                newLine.append(self.mapList[xx][yy])

            newMap.append(newLine)

        self.turnMap = newMap
        self.turnMap.reverse()
        self.x2y()

    def printTurnMap(self):
        for line in self.turnMap:
            print(' '.join(line))

    def checkPosValid(self, pos, w, h):
        for x in range(w):
            for y in range(h):
                xx = pos[0] - x
                yy = pos[1] + y
                if not 0 <= xx < 32:
                    return False

                if not 0 <= yy < 32:
                    return False

                if self.turnMap[xx][yy] != '1':
                    return False

        return True

    def markPlace(self, pos, w, h):
        for x in range(w):
            for y in range(h):
                xx = pos[0] - x
                yy = pos[1] + y
                self.turnMap[xx][yy] = '2'

    def placeMonster(self, point, angle):
        self.getTurnMap(angle)
        point = list(map(lambda x: float(x), point.split(',')))
        w, z, h = point
        w = math.ceil(w)
        h = math.ceil(h)
        xCheckList = []
        yCheckList = []
        markSet = set()
        count = 0
        while 1:
            count += 1
            if count == 1000:
                print(markSet)
                self.printTurnMap()
                print(w, h)
                return None, None
            x = random.randint(0, self.w)
            y = random.randint(0, self.h)
            if (x, y) in markSet:
                continue

            markSet.add((x, y))
            if self.checkPosValid((x, y), w, h):
                self.markPlace((x, y), w, h)
                return x, y

    def parseAllInfo(self):
        self.parseMap()
        # self.getMap()
        self.getDoor()

    def test(self):
        self.parseAllInfo()
        self.getTurnMap(270)
