import json
import os
import random
import sys

import TMX
#import mapDisplay


class RankDungeon(object):
    def __init__(self, root, startID, endID, count, everyMonCount):
        self.startID = startID
        self.endID = endID
        self.count = count
        self.root = root
        self.startPos = (-16, 0)
        self.cards = []
        self.monsters = []
        self.boss = -1
        self.everyMonCount = everyMonCount
        self.tmxList = {}
        self.oppoDoorDir = [2, 3, 0, 1]
        self.addPos = [(-32, 0), (0, -32), (32, 0), (0, 32)]

    def loadRank(self):
        dataPath = os.path.join(self.root, 'scripts\\data')
        # print(dataPath)
        sys.path.append(dataPath)
        import innerWorldDungeon_rankDungeonInfo as IWDRDID
        import field_base as FBD
        import homeDefence_base as HDBD
        import innerWorldDungeon_dungeon as IWDDD
        #import creep_base as CBD
        self.IWDRDID = IWDRDID.datas
        self.FBD = FBD.datas
        self.HDBD = HDBD.datas
        self.IWDDD = IWDDD.datas
        #self.CBD = CBD.datas
        self.parseDungeonString(self.IWDDD[51000027]['dungeonString'])

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
        monsters = []
        while monCount:
            mon = random.choice(monIds)
            monInfo = self.HDBD[mon]
            if monInfo['type'] == 1:
                if self.boss == -1:
                    self.boss = mon
                continue

            monsters.append(mon)
            monCount -= 1

        while self.boss == -1:
            mon = random.choice(monIds)
            monInfo = self.HDBD[mon]
            if monInfo['type'] != 1:
                continue

            self.boss = mon

        for i in range(self.count - 1):
            self.monsters.append(monsters[i * self.everyMonCount:(i + 1) * self.everyMonCount])

    def randomCards(self):
        cards = []
        cards.extend((self.startID, self.endID))
        count = self.count - 2
        tmxIds = self.tmxList.keys()
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
        Door = list(filter(lambda x: door[x] and x != useDoor, range(4)))
        return random.choice(Door)

    def getTurnAngle(self, oppoDoor, curDoor):
        return ((curDoor + 4 - oppoDoor) % 4) * 90

    def getNewCardInfo(self, info, card):
        newInfo = {}
        print(info['id'], info['card'].door, info['useDoor'])
        door = self.getChoiceDoor(info['card'].door, info['useDoor'])
        doorDir = self.getDoorDir(door, info['angle'])
        oppoDoor = self.oppoDoorDir[doorDir]
        curDoor = self.getChoiceDoor(card[1].door, -1)
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
        return newInfo

    def getCardStr(self, info):
        return '|'.join([str(info['id']), str(info['pos']), str(info['angle'])])

    def placeCards(self):
        mapCards = []
        info = {}
        info['pos'] = self.startPos
        info['id'] = self.cards[0][0]
        info['card'] = self.cards[0][1]
        info['angle'] = 90
        info['useDoor'] = -1
        info['cardStr'] = self.getCardStr(info)
        mapCards.append(info)
        for card in self.cards[2:]:
            info = self.getNewCardInfo(info, card)
            mapCards.append(info)

        info = self.getNewCardInfo(info, self.cards[1])
        mapCards.append(info)

        for card in mapCards:
            print(card)
            print(card['card'].door)
        self.mapCards = mapCards

    def getMonStr(self, monID, pos, group):
        return '|'.join([str(monID), str(pos), '180.0', '2', str(group)])

    def placeOneMonster(self, monID, info, group):
        areaRange = self.HDBD[monID]['areaRange']
        pos = info['card'].placeMonster(areaRange, info['angle'])
        monInfo = {}
        monInfo['id'] = monID
        monInfo['area'] = areaRange
        monInfo['pos'] = (info['pos'][0] + pos[0],
                          info['pos'][1] + pos[1] - 32)
        monInfo['name'] = self.HDBD[monID]['name']
        monInfo['monStr'] = self.getMonStr(monID, monInfo['pos'], group)
        print(monInfo['monStr'])
        return monInfo

    def placeMonster(self):
        monsterInfos = []
        self.mapCards[0]['card'].getTurnMap(90)
        group = 2
        for index, info in enumerate(self.mapCards[1:]):
            monsters = self.monsters[index]
            for monID in monsters:
                monInfo = self.placeOneMonster(monID, info, group)
                monsterInfos.append(monInfo)

            group += 1

        monInfo = self.placeOneMonster(self.boss, self.mapCards[-1], group - 1)
        monsterInfos.append(monInfo)
        self.monInfos = monsterInfos

    def makeUpString(self):
        strDict = {}
        strDict['cards'] = '#'.join(map(lambda x: x['cardStr'], self.mapCards))
        strDict['Monster'] = '#'.join(
            map(lambda x: x['monStr'], self.monInfos))
        finalStr = json.dumps(strDict).replace(' ', '')
        print(finalStr)
        print('$createhome ' + finalStr)

    def generate(self):
        self.randomCards()
        self.randomMonster()
        self.placeCards()
        self.placeMonster()
        self.makeUpString()

    def parseDungeonString(self, data):
        jsonData = json.loads(data)
        for k, v in jsonData.items():
            print('-' * 60)
            mod = v.split('#')
            print(k)
            for i in mod:
                print(i)

    def parseTmx(self, tmxID):
        tmx = TMX.TMX(self.tmxList[tmxID])
        tmx.parseAllInfo()
        return tmx

    def test(self):
        self.loadRank()
        self.loadTmx()
        self.generate()
        tmx = TMX.TMX(self.tmxList[62000011])
        tmx.test()
        print(self.cards)

        #mapDisp = mapDisplay.MapDisplay(self.mapCards,  self.monInfos)
        # mapDisp.test()


if __name__ == '__main__':
    if len(sys.argv) == 6:
        path = sys.argv[1]
        startId = int(sys.argv[2])
        endId = int(sys.argv[3])
        count = int(sys.argv[4])
        everyMonCount = int(sys.argv[5])
        rank = RankDungeon(path, startId, endId, count, everyMonCount)
    else:
        rank = RankDungeon(
            r'E:\svn\Dev\Server\kbeWin\kbengine\assets', 62000004, 62000005, 5, 3)
        rank.test()
