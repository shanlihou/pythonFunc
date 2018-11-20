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
import Cards
import Plunder
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
    dungeonKey = ['groupFourWithBoss', 'groupThreeWithBoss', 'groupThreeWithoutBoss', 'groupTwoWithBoss', 'groupTwoWithoutBoss']
    def __init__(self, root, startID, endID, count, everyMonCount):
        self.startID = startID
        self.endID = endID
        self.count = count
        self.root = root
        self.startPos = (64, -64)
        self.everyMonCount = everyMonCount
        self.tmxList = {}
        self.cardFilter = [62000006, 62000007, 62000012]
        self.card2Crystal = {62000006: (-4.2, -4.22),
                             62000007: (1.8, 0),
                             62000012: (6.94, -3.74)}
        self.init()

    def init(self, count=0, randomCount=0):
        if count:
            self.count = count + 1
        self.randomCount = randomCount
        self.monsters = []
        self.boss = -1

    def loadRank(self):
        dataPath = os.path.join(self.root, 'scripts\\data')
        # print(dataPath)
        sys.path.append(dataPath)
        import innerWorldDungeon_rankDungeonInfo as IWDRDID
        import innerWorldDungeon_rankDungeon as IWDRDD
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
        self.IWDRDD = IWDRDD
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

    def randomMonsterOld(self):
        monCount = (self.count - 1) * self.everyMonCount
        monIds = list(map(lambda x: x['ID'], filter(
            lambda x: x['isOpen'], self.HDBD.values())))
        commonMons = list(filter(lambda x: self.HDBD[x]['type'] != 1, monIds))
        bossMons = list(filter(lambda x: self.HDBD[x]['type'] == 1, monIds))
        monsters = []
        bossIter = iter(random.sample(bossMons, self.count - 1))
        while monCount:
            mon = random.choice(commonMons)
            monsters.append(mon)
            monCount -= 1

        while self.boss == -1:
            self.boss = next(bossIter)

        for i in range(self.count - 1):
            monAdds = monsters[i *
                               self.everyMonCount:(i + 1) * self.everyMonCount]
            if i:
                monAdds.append(next(bossIter))

            self.monsters.append(monAdds)

    def getGroupMonster(self, groupName, bossId, commonMons, bossMons):
        groups = self.IWDRDD.datas[groupName]['value']
        groups = list(filter(lambda x: x[0] != bossId, groups))
        bossMons = list(filter(lambda x: x != bossId, bossMons))
        mons = random.choice(groups)
        print(mons)
        retList = []
        if groupName == 'groupFourWithBoss':
            retList.extend(mons)
        elif groupName == 'groupThreeWithBoss':
            retList.extend(mons)
            retList.append(random.choice(commonMons))
        elif groupName == 'groupThreeWithoutBoss':
            retList.append(random.choice(bossMons))
            retList.extend(mons)
        elif groupName == 'groupTwoWithBoss':
            retList.extend(mons)
            retList.extend(random.sample(commonMons, 2))
        elif groupName == 'groupTwoWithoutBoss':
            retList.append(random.choice(bossMons))
            retList.append(random.choice(commonMons))
            retList.extend(mons)

        return retList

    def getGroupRandom(self, bossId, commonMons, bossMons):
        bossMons = list(filter(lambda x: x != bossId, bossMons))
        retList = []
        retList.append(random.choice(bossMons))
        retList.extend(random.sample(commonMons, 3))
        return retList

    def randomMonster(self):
        monIds = list(map(lambda x: x['ID'], filter(
            lambda x: x['isOpen'], self.HDBD.values())))
        commonMons = list(filter(lambda x: self.HDBD[x]['type'] != 1, monIds))
        bossMons = list(filter(lambda x: self.HDBD[x]['type'] == 1, monIds))

        rCount = self.randomCount
        count = self.count - self.randomCount - 1
        index = 0
        bossId = 0
        self.monsters = []
        while rCount or count:
            index += 1
            rand = random.randint(1, rCount + count)
            if rand <= rCount:
                rCount -= 1
                groupName = random.choice(self.dungeonKey)
                mons = self.getGroupMonster(groupName, bossId, commonMons, bossMons)
            else:
                count -= 1
                mons = self.getGroupRandom(bossId, commonMons, bossMons)

            if index == 1:
                bossId = mons[0]
                self.monsters.append(mons[1:])
            else:
                self.monsters.append(mons)

        self.boss = bossId

    def randomCards(self):
        self.cards = Cards.Cards(self.tmxList)
        self.cards.randomCards(self.startID, self.endID, self.count)

    def placeCards(self):
        self.mapCards = Cards.MapCards(self.cards)
        self.mapCards.placeCards()

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

    def cardFilt(self, cardId):
        return cardId in self.cardFilter

    def randomCrystals(self):
        '''
        crystals = list(
            filter(lambda x: self.HDCD[x]['isOpen'], self.HDCD.keys()))
        crystalSet = set()
        '''
        self.crystals = []
        for index, card in enumerate(self.mapCards):
            cardId = card.id
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
            cardPos = card.pos
            cardAngle = card.angle
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
        pos = info.card.placeMonster(areaRange, info.angle)
        monInfo = {}
        monInfo['id'] = monID
        monInfo['area'] = areaRange
        monInfo['pos'] = (info.pos[0] + pos[0],
                          info.pos[1] + pos[1])
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
        self.mapCards[-1].card.getTurnMap(self.mapCards[-1].angle)
        self.monInfos = monsterInfos

    def makeUpString(self):
        strDict = {}
        strDict['cards'] = '#'.join(map(lambda x: x.cardStr, self.mapCards))
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

    def getDungeonStr(self):
        self.loadRank()
        self.loadTmx()
        self.generate()
        return self.finalStr

    def test(self):
        self.init(5, 3)
        self.loadRank()
        self.loadTmx()
        self.generate()
        tmx = TMX.TMX(self.tmxList[62000012], 62000012)
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
            '{"Boss":"61000601|(95,-41)|180.0|2|2","Monster":"61000330|(66,-37)|180.0|2|2#61000412|(72,-37)|180.0|2|2#61000518|(69,-35)|180.0|2|2#61000311|(49,-29)|180.0|2|3#61000530|(56,-33)|180.0|2|3#61000418|(57,-28)|180.0|2|3#61000601|(51,-37)|180.0|2|3#61000419|(18,-36)|180.0|2|4#61000517|(16,-44)|180.0|2|4#61000308|(21,-22)|180.0|2|4#61000601|(12,-34)|180.0|2|4#30040001|41.06,-28.26|0|2|0#30040001|16.00,-33.80|0|2|0","cards":"62000005|(64,-64)|0#62000012|(32,-48)|180#62000007|(0,-48)|90#62000004|(0,-80)|0"}')

        # display
        import mapDisplay
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
        self.bossList = []
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

    def createObj(self, index, dungeonId, bossId):
        retStr = '"%d": {\n' % index + ' ' * 8 + '"ID": %d,\n' % dungeonId
        retStr += ' ' * 8 + '"BOSSID": %d\n' % bossId + ' ' * 4 + '}'
        return retStr

    def createClientFile(self):
        import innerWorldDungeon_rankDungeonInfo as IWDRID
        dungeons = list(IWDRID.datas.keys())
        dungeons.sort()
        bossIter = iter(self.bossList)
        objList = []
        for index, dungeonId in enumerate(dungeons):
            objStr = self.createObj(index + 1, dungeonId, next(bossIter))
            objList.append(objStr)

        dataStr = (',\n' + ' ' * 4).join(objList)
        dataStr = '{\n' + ' ' * 4 + dataStr + '\n}'
        filename = 'innerWorldDungeon.rankDungeonInfo.txt'
        file1 = os.path.join(
            config.SVN_ROOT, config.RANK_INFO_CLIENT1, filename)
        with open(file1, 'w') as fw:
            fw.write(dataStr)

        file2 = os.path.join(
            config.SVN_ROOT, config.RANK_INFO_CLIENT2, filename)
        with open(file2, 'w') as fw:
            fw.write(dataStr)

    def getMonsterArgs(self, rank):
        for start, end, arg1, arg2 in config.MONSTER_RANDOM_RULES:
            if start <= rank <= end:
                return arg1, arg2
        else:
            return 5, 0

    def createNewFile(self):
        import innerWorldDungeon_rankDungeonInfo as IWDRID
        fileName = config.SVN_ROOT + \
            r'\Dev\Server\kbeWin\kbengine\assets\scripts\data\innerWorldDungeon_rankDungeonInfo.py'
        fileNew = fileName + time.strftime('.%Y-%m-%H-%M-%S')
        pattern = re.compile(r'("dungeonString": )(.+)(,*$)')
        self.rankClass = 1

        def rep(m):
            monArgs = self.getMonsterArgs(self.rankClass)
            self.rank.init(*monArgs)
            self.rank.generate()
            retStr = m.group(1) + "'" + self.rank.finalStr + "'"
            self.bossList.append(self.rank.boss)
            if m.group(2).endswith(','):
                retStr += ','
            retStr += m.group(3)
            self.rankClass += 1
            return retStr

        with open(fileName) as fr:
            fw = open(fileNew, 'w')
            for line in fr:
                find = pattern.search(line)
                if find:
                    # newLine = pattern.sub(r"\1'" + self.rank.finalStr + r"'\3", line)
                    newLine = pattern.sub(rep, line)
                    fw.write(newLine)
                    continue
                fw.write(line)
            fw.close()

        dstDir = config.SVN_ROOT + r'\配置表\data\python'
        shutil.copy(fileNew, dstDir)

        self.createClientFile()


if __name__ == '__main__':
    assetsPath = os.path.join(
        config.SVN_ROOT, r'Dev\Server\kbeWin\kbengine\assets')
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
                assetsPath, 62000004, 62000005, 4, 3)
            rank.test()
        elif opt == 1:
            gen = Generator(
                assetsPath, 62000004, 62000005, 4, 4)
            gen.createNewFile()
        else:
            plunder = Plunder.Plunder(
                assetsPath, 62000004, 62000005, 4, 3)
            plunder.test()
