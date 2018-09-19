# coding=utf-8
import json
import os
import random
import sys
import math
import re
import time
import shutil

import TMX
# import mapDisplay
from _operator import pos
import config


class Crystal(object):
    def __init__(self, id, pos, group):
        self.id = id
        self.pos = pos
        self.group = group
        self.oriPos = pos

    def getCrystalStr(self):
        self.cryStr = '|'.join(
            [str(self.id), '%.2f,%.2f' % self.pos, '0', '2', '0'])


class RankDungeon(object):
    def __init__(self, root, startID, endID, count, everyMonCount):
        self.startID = startID
        self.endID = endID
        self.count = count
        self.root = root
        self.startPos = (64, -64)
        self.everyMonCount = everyMonCount
        self.tmxList = {}
        self.oppoDoorDir = [2, 3, 0, 1]
        self.addPos = [(-32, 0), (0, -32), (32, 0), (0, 32)]
        self.cardFilter = [62000006, 62000007, 62000012]
        self.card2Crystal = {62000006: (-4.2, -4.22),
                             62000007: (1.8, 0),
                             62000012: (6.94, -3.74)}
        self.init()

    def init(self):
        self.cards = []
        self.monsters = []
        self.boss = -1

    def loadRank(self):
        dataPath = os.path.join(self.root, 'scripts\\data')
        # print(dataPath)
        sys.path.append(dataPath)
        import innerWorldDungeon_rankDungeonInfo as IWDRDID
        import field_base as FBD
        import homeDefence_base as HDBD
        import innerWorldDungeon_dungeon as IWDDD
        import homeDefence_circle as HDCD
        #import creep_base as CBD
        self.IWDRDID = IWDRDID.datas
        self.FBD = FBD.datas
        self.HDBD = HDBD.datas
        self.IWDDD = IWDDD.datas
        self.HDCD = HDCD.datas
        #self.CBD = CBD.datas
        # self.parseDungeonString(self.IWDDD[51000010]['dungeonString'])

    def loadTmx(self):
        tmxPath = os.path.join(self.root, r'res\spaces\field')
        for i in os.listdir(tmxPath):
            if not i.endswith('.tmx'):
                continue

            fullpath = os.path.join(tmxPath, i)
            i = i.split('.')
            if len(i) < 2:
                continue

            i = i[0].split('_')
            if len(i) < 2:
                continue

            i = i[1]
            id = (int(i))
            fb = self.FBD[id]
            print(id, fb['isOpen'])
            if not fb['isOpen']:
                continue
            self.tmxList[id] = fullpath

    def randomMonster(self):
        monCount = (self.count - 1) * self.everyMonCount
        monIds = list(map(lambda x: x['ID'], filter(
            lambda x: x['isOpen'], self.HDBD.values())))
        commonMons = list(filter(lambda x: self.HDBD[x]['type'] != 1, monIds))
        bossMons = list(filter(lambda x: self.HDBD[x]['type'] == 1, monIds))
        monsters = []
        while monCount:
            mon = random.choice(commonMons)
            monsters.append(mon)
            monCount -= 1

        while self.boss == -1:
            mon = random.choice(bossMons)
            self.boss = mon

        for i in range(self.count - 1):
            monAdds = monsters[i *
                               self.everyMonCount:(i + 1) * self.everyMonCount]
            if i:
                monAdds.append(random.choice(bossMons))

            self.monsters.append(monAdds)

    def cardFilt(self, cardId):
        return cardId in self.cardFilter

    def randomCards(self):
        cards = []
        cards.extend((self.startID, self.endID))
        count = self.count - 2
        # 过滤地块id
        tmxIds = list(filter(self.cardFilt, self.tmxList.keys()))
        while count:
            tmxs = random.sample(tmxIds, count)
            for tmx in tmxs:
                if tmx not in cards:
                    cards.append(tmx)
                    count -= 1

        for card in cards:
            tmx = self.parseTmx(card)
            self.cards.append((card, tmx))

    def getDoorDir(self, door, angle):
        angle /= 90
        return int((door - angle + 4) % 4)

    def getChoiceDoor(self, door, useDoor):
        Door = list(filter(lambda x: door[x] and x not in useDoor, range(4)))
        return random.choice(Door)

    def getTurnAngle(self, oppoDoor, curDoor):
        return ((curDoor + 4 - oppoDoor) % 4) * 90

    def getCouldUseDoor(self, useDict, fDoor, bDoor, useDoor):
        retList = []
        for fIndex, fd in enumerate(fDoor):
            if not fd:
                continue

            if fIndex == useDoor:
                continue

            if fIndex in useDict:
                bList = useDict[fIndex]
                for bIndex, bd in enumerate(bDoor):
                    if not bd:
                        continue

                    if bIndex in bList:
                        continue

                    retList.append(fIndex)
                    break
            else:
                retList.append(fIndex)
        return retList

    def getNewCardInfo(self, info, card, useDict):
        newInfo = {}
        print(info['id'], info['card'].door,
              info['useDoor'], card[1].door, useDict)
        couldUseDoorList = self.getCouldUseDoor(
            useDict, info['card'].door, card[1].door, info['useDoor'])
        if not couldUseDoorList:
            return None, useDict
        # door = self.getChoiceDoor(info['card'].door, info['useDoor'])
        door = random.choice(couldUseDoorList)
        doorDir = self.getDoorDir(door, info['angle'])
        oppoDoor = self.oppoDoorDir[doorDir]
        curDoor = self.getChoiceDoor(card[1].door, useDict.get(door, []))
        newPos = (info['pos'][0] + self.addPos[doorDir][0],
                  info['pos'][1] + self.addPos[doorDir][1])

        turnAngle = self.getTurnAngle(oppoDoor, curDoor)
        print(door, doorDir, oppoDoor, curDoor)
        newInfo['pos'] = newPos
        newInfo['angle'] = turnAngle
        newInfo['card'] = card[1]
        newInfo['id'] = card[0]
        newInfo['useDoor'] = curDoor
        newInfo['cardStr'] = self.getCardStr(newInfo)
        useDict.setdefault(door, [])
        useDict[door].append(curDoor)
        return newInfo, useDict

    def getCardStr(self, info):
        return '|'.join([str(info['id']), str(info['pos']), str(info['angle'])])

    def placeCards(self):
        mapCards = []
        info = {}
        # fix end card
        info['pos'] = (64, -48)
        info['id'] = self.cards[1][0]
        info['card'] = self.cards[1][1]
        info['angle'] = 0
        info['useDoor'] = -1
        mapCards.append(info)
        cards = self.cards[2:]
        cards.append(self.cards[0])
        self.cards = cards
        self.recPlaceCard(mapCards, 0)
        mapCards[0]['pos'] = self.startPos
        mapCards[0]['cardStr'] = self.getCardStr(mapCards[0])

        for card in mapCards:
            print(card)
            print(card['card'].door)
        self.mapCards = mapCards

    def isValidCardPos(self, mapCards, pos):
        for index, mapCard in enumerate(mapCards):
            cPos = mapCard['pos']
            if not index:
                cPos = self.startPos

            w = mapCard['card'].w
            h = mapCard['card'].h
            if pos[0] + 32 > cPos[0] and pos[0] < cPos[0] + w and\
                    pos[1] < cPos[1] + h and pos[1] + 32 > cPos[1]:
                return False

        return True

    def recPlaceCard(self, mapCards, deep):
        print('recP', mapCards, deep)
        card = self.cards[deep]
        useDict = {}
        while 1:
            info, useDict = self.getNewCardInfo(mapCards[-1], card, useDict)
            if not info:
                break

            if not self.isValidCardPos(mapCards, info['pos']):
                continue

            mapCards.append(info)
            if deep == len(self.cards) - 1:
                return True

            ret = self.recPlaceCard(mapCards, deep + 1)
            if ret:
                return True

            del mapCards[-1]

        return False

    def turnCrystal(self, pos, angle):
        angle = 360 - angle
        angle = angle * math.pi / 180
        cosTheta = math.cos(angle)
        sinTheta = math.sin(angle)
        x, y = pos
        x, y = (cosTheta * x - sinTheta * y, sinTheta * x + cosTheta * y)
        return x, y

    def getCrystalPos(self, cryPos, cardPos):
        x = cryPos[0] + cardPos[0] + 16
        y = cryPos[1] + cardPos[1] + 16
        return x, y

    def randomCrystals(self):
        '''
        crystals = list(
            filter(lambda x: self.HDCD[x]['isOpen'], self.HDCD.keys()))
        crystalSet = set()
        '''
        self.crystals = []
        for index, card in enumerate(self.mapCards):
            cardId = card['id']
            if not self.cardFilt(cardId):
                continue
            '''
            while 1:
                crystalId = random.choice(crystals)
                if crystalId not in crystalSet:
                    crystalSet.add(crystalId)
                    break
            '''
            pos = self.card2Crystal[cardId]
            cardPos = card['pos']
            cardAngle = card['angle']
            crystal = Crystal(30040001, pos, index)
            pos = self.turnCrystal(pos, cardAngle)
            pos = self.getCrystalPos(pos, cardPos)
            crystal.pos = pos
            crystal.getCrystalStr()
            self.crystals.append(crystal)

    def getMonStr(self, monID, pos, group):
        return '|'.join([str(monID), str(pos), '180.0', '2', str(group)])

    def placeOneMonster(self, monID, info, group):
        areaRange = self.HDBD[monID]['areaRange']
        pos = info['card'].placeMonster(areaRange, info['angle'])
        monInfo = {}
        monInfo['id'] = monID
        monInfo['area'] = areaRange
        monInfo['pos'] = (info['pos'][0] + pos[0],
                          info['pos'][1] + pos[1])
        monInfo['name'] = self.HDBD[monID]['name']
        monInfo['monStr'] = self.getMonStr(monID, monInfo['pos'], group)
        print(monInfo['monStr'])
        return monInfo

    def placeMonster(self):
        monsterInfos = []
        # self.mapCards[0]['card'].getTurnMap(90)
        group = 2
        for index, info in enumerate(self.mapCards[0: -1]):
            monsters = self.monsters[index]
            for monID in monsters:
                monInfo = self.placeOneMonster(monID, info, group)
                monsterInfos.append(monInfo)

            group += 1

        self.bossInfo = self.placeOneMonster(
            self.boss, self.mapCards[0], 2)
        # monsterInfos.append(monInfo)
        self.mapCards[-1]['card'].getTurnMap(self.mapCards[-1]['angle'])
        self.monInfos = monsterInfos

    def makeUpString(self):
        strDict = {}
        strDict['cards'] = '#'.join(map(lambda x: x['cardStr'], self.mapCards))
        strDict['Monster'] = '#'.join(
            map(lambda x: x['monStr'], self.monInfos))
        cryStr = '#'.join(map(lambda x: x.cryStr, self.crystals))
        strDict['Monster'] = strDict['Monster'] + '#' + cryStr
        strDict['Boss'] = self.bossInfo['monStr']
        finalStr = json.dumps(strDict).replace(' ', '')
        self.finalStr = finalStr
        print(finalStr)
        print('$createhome ' + finalStr)
        self.parseDungeonString(finalStr)

    def generate(self):
        self.randomCards()
        self.randomMonster()
        self.placeCards()
        self.placeMonster()
        self.randomCrystals()
        self.makeUpString()

    def parseDungeonString(self, data):
        jsonData = json.loads(data)
        for k, v in jsonData.items():
            print('-' * 60)
            mod = v.split('#')
            print(k)
            for i in mod:
                print(i)
            print('-' * 60)

    def parseTmx(self, tmxID):
        tmx = TMX.TMX(self.tmxList[tmxID])
        tmx.parseAllInfo()
        return tmx

    def getDungeonStr(self):
        self.loadRank()
        self.loadTmx()
        self.generate()
        return self.finalStr

    def test(self):
        self.loadRank()
        self.loadTmx()
        self.generate()
        tmx = TMX.TMX(self.tmxList[62000012])
        tmx.test()
        print(self.cards)
        self.turnCrystal((9, 7), 45)
        '''
        print('parse1')
        self.parseDungeonString('{"cards":"62000004|(-16,-16)|0#62000005|(-16,16)|0#62000007|(-48,-16)|0#62000006|(-48,16)|180","Monster":"61000102|(4.31,5.04)|186.63|2|2#61000074|(-23.14,-33.79)|85.58|2|3#61000078|(-26.35,-3.23)|137.52|2|4","Crystal":"6592054069488451585|(-30.2,-32)|0|2|3#6592054069488451591|(-27.8,4.22)|180|2|4"}')
        print('parse2')
        self.parseDungeonString('{"cards":"62000004|(-16,-16)|0#62000005|(-16,16)|0#62000007|(-48,-16)|0#62000006|(-48,16)|180","Monster":"61000102|(4.31,5.04)|186.63|2|2#61000074|(-23.14,-33.79)|85.58|2|3#61000078|(-26.35,-3.23)|137.52|2|4","Crystal":"6592054065193484297|(-30.2,-32)|0|2|3#6592054065193484289|(-27.8,4.22)|180|2|4"}')
        print('parse3')
        self.parseDungeonString('{"cards":"62000004|(-16,-16)|0#62000005|(-16,16)|0#62000007|(-48,-16)|0#62000006|(-48,16)|180","Monster":"61000102|(4.31,5.04)|186.63|2|2#61000074|(-23.14,-33.79)|85.58|2|3#61000078|(-26.35,-3.23)|137.52|2|4","Crystal":"6592054060898516993|(-30.2,-32)|0|2|3#6592054065193484293|(-27.8,4.22)|180|2|4"}')
        print('parse4')
        self.parseDungeonString('{"cards":"62000004|(-16,-16)|0#62000005|(-16,16)|0#62000007|(-48,-16)|0#62000006|(-48,16)|180","Monster":"61000102|(4.31,5.04)|186.64|2|2#61000074|(-23.14,-33.79)|85.58|2|3#61000078|(-26.35,-3.23)|137.51|2|4#30040001|(-30.2,-32)|0|2|3","Crystal":"6592054065193484289|(-30.2,-32)|0|2|3#6592054065193484293|(-27.8,4.22)|0|2|4#6592054069488451589|(-27.8,4.22)|0|2|4"}')
        '''
        print('parse:')
        self.parseDungeonString(
            '{"cards":"62000004|(32,-80)|0#62000005|(64,-64)|0#62000007|(32,-48)|90#62000012|(0,-48)|180","Boss":"61000610|(73.4,-24.73)|212.89|2|2","Monster":"30040001|(48,-33.8)|0|2|3#30040001|(9.06,-28.26)|180|2|4"}')

        # display

        mapDisp = mapDisplay.MapDisplay(
            self.mapCards,  self.monInfos, self.crystals)
        mapDisp.test()


class Generator(object):
    def __init__(self, root, startID, endID, count, everyMonCount):
        self.root = root
        self.startId = startID
        self.endId = endID
        self.count = count
        self.everyMonCount = everyMonCount
        self.rank = RankDungeon(self.root, self.startId,
                                self.endId, self.count, self.everyMonCount)
        self.rank.loadRank()
        self.rank.loadTmx()

    def generator(self):
        finalStrs = []
        for i in range(10):
            rank.init()
            rank.generate()
            print(rank.finalStr)
            finalStrs.append(rank.finalStr)
        print(finalStrs)

    def createNewFile(self):
        import innerWorldDungeon_rankDungeonInfo as IWDRID
        fileName = config.SVN_ROOT + \
            r'\Dev\Server\kbeWin\kbengine\assets\scripts\data\innerWorldDungeon_rankDungeonInfo.py'
        fileNew = fileName + time.strftime('.%Y-%m-%H-%M-%S')
        pattern = re.compile(r'("dungeonString": )(.+)(,*$)')
        with open(fileName) as fr:
            fw = open(fileNew, 'w')
            for line in fr:
                find = pattern.search(line)
                if find:
                    self.rank.init()
                    self.rank.generate()
                    print(find.group(1))
                    newLine = pattern.sub(
                        r"\1'" + self.rank.finalStr + r"'\3", line)
                    fw.write(newLine)
                    continue
                fw.write(line)
            fw.close()

        dstDir = config.SVN_ROOT + r'\配置表\data\python'
        shutil.copy(fileNew, dstDir)


if __name__ == '__main__':
    if len(sys.argv) == 6:
        path = sys.argv[1]
        startId = int(sys.argv[2])
        endId = int(sys.argv[3])
        count = int(sys.argv[4])
        everyMonCount = int(sys.argv[5])
        rank = RankDungeon(path, startId, endId, count, everyMonCount)
    else:
        opt = 1
        if opt == 0:
            rank = RankDungeon(
                r'E:\svn\Dev\Server\kbeWin\kbengine\assets', 62000004, 62000005, 4, 3)
            rank.test()
        else:
            gen = Generator(
                r'E:\svn\Dev\Server\kbeWin\kbengine\assets', 62000004, 62000005, 4, 3)
            gen.createNewFile()
