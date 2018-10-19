import RankDungeon
import TMX
import config
import math
from _operator import pos


class PlunderCard(object):
    def __init__(self, id, tmx, pos, angle):
        self.id = id
        self.tmx = tmx
        self.pos = pos
        self.angle = angle
        self.useDoor = -1

    def isCollide(self, pos):
        w = self.tmx.w
        h = self.tmx.h

        x = self.pos[0]
        y = self.pos[1]
        if self.id == 62000005:
            y = -64

        if pos[0] + 32 > x and pos[0] < x + w and\
                pos[1] < y + h and pos[1] + 32 > y:
            return True

        return False


class RecordCard(object):
    def __init__(self, cardId, pos, angle):
        self.id = cardId
        self.pos = pos
        self.angle = angle

    def getCardStr(self):
        self.cardStr = '|'.join([str(self.id), '%d,%d' %
                                 self.pos, str(self.angle)])


class PlunderMonster(object):
    card2Crystal = {62000006: (-4.2, -4.22),
                    62000007: (1.8, 0),
                    62000012: (6.94, -3.74)}

    def __init__(self, tmxs, HDBD, endId):
        self.tmxs = tmxs
        self.HDBD = HDBD
        self.endId = endId
        self.getBiggestArea()

    def getBiggestArea(self):
        maxW = 0
        maxH = 0
        for data in filter(lambda x: x['isOpen'], self.HDBD.values()):
            area = data['areaRange']
            w, z, h = eval(area)
            maxW = max(w, maxW)
            maxH = max(h, maxH)
        self.maxW, self.maxH = maxW, maxH
        self.pointStr = '%d,0,%d' % (maxH, maxW)

    def getRandomInfo(self):
        self.randomCards()
        self.createCrystals()

    def createCrystals(self):
        crystals = ['%d: %s' % (k, str(v))
                    for k, v in self.card2Crystal.items()]
        crystals = (',\n' + ' ' * 4).join(crystals)
        crystals = 'crystals = {\n' + ' ' * 4 + crystals + '\n}\n'
        self.crystals = crystals

    def randomCards(self):
        monsters = [self.randomCard(cardId)
                    for cardId in self.card2Crystal.keys()]
        monsters.append(self.randomCard(self.endId))
        monsters = (',\n' + ' ' * 4).join(monsters)
        monsters = 'monsters = {\n' + ' ' * 4 + monsters + '\n}\n'
        self.monsters = monsters

    def randomCard(self, cardId):
        monsterGroup = []
        while len(monsterGroup) < 10:
            retStrs = self.randomCardOnce(cardId)
            if not retStrs:
                continue

            monsterGroup.append(retStrs)

        monsterGroup = (',\n' + ' ' * 8).join(monsterGroup)
        monsterGroup = '%d: [\n' % cardId + ' ' * \
            8 + monsterGroup + '\n' + ' ' * 4 + ']'
        return monsterGroup

    def randomCardOnce(self, cardId):
        tmx = self.tmxs[cardId]
        tmx.init()
        tmx.getTurnMap(0)
        if cardId != self.endId:
            crystalPos = self.card2Crystal[cardId]
            crystalPos = (
                math.ceil(crystalPos[0]) + 16, math.ceil(crystalPos[1] + 16))
            tmx.markPlace(crystalPos, 4, 4)

        pointList = []
        for i in range(4):
            x, y = tmx.placeMonster(self.pointStr, 0)
            if not x and not y:
                return None

            pointList.append((x, y))
        pointList = ['(%d,%d)' % (point[0], point[1]) for point in pointList]
        pointStrs = '[' + ','.join(pointList) + ']'
        return pointStrs


class Plunder(object):
    cardFilter = [62000006, 62000007, 62000012]
    oppoDoorDir = [2, 3, 0, 1]
    startPos = (64, -64)
    addPos = [(-32, 0), (0, -32), (32, 0), (0, 32)]

    def __init__(self, root, startID, endID, count, everyMonCount):
        self.root = root
        self.startId = startID
        self.endId = endID
        self.count = count
        self.everyMonCount = everyMonCount
        self.rank = RankDungeon.RankDungeon(self.root, self.startId,
                                            self.endId, self.count, self.everyMonCount)
        self.rank.loadRank()
        self.rank.loadTmx()
        tmxs = list(map(lambda id: TMX.TMX(
            self.rank.tmxList[id], id), self.cardFilter))
        [tmx.parseAllInfo() for tmx in tmxs]
        self.tmxs = {}
        for index in range(len(self.cardFilter)):
            self.tmxs[self.cardFilter[index]] = tmxs[index]

        self.endTmx = TMX.TMX(self.rank.tmxList[self.endId], self.endId)
        self.startTmx = TMX.TMX(self.rank.tmxList[self.startId], self.startId)
        self.endTmx.parseAllInfo()
        self.startTmx.parseAllInfo()

        self.tmxs[self.startId] = self.startTmx
        self.tmxs[self.endId] = self.endTmx
        self.plunderMonster = PlunderMonster(
            self.tmxs, self.rank.HDBD, self.endId)
        self.plunderMonster.getRandomInfo()

    def isCardUse(self, cardId, cardList):
        return list(filter(lambda card: card.id == cardId, cardList))

    def getDoorDir(self, door, angle):
        angle /= 90
        return int((door - angle + 4) % 4)

    def getTurnAngle(self, oppoDoor, curDoor):
        return ((curDoor + 4 - oppoDoor) % 4) * 90

    def isCollide(self, cardList, pos):
        for card in cardList:
            if card.isCollide(pos):
                return True

        return False

    def getNextCard(self, cardList, cardId):
        lastCard = cardList[-1]
        tmx = self.tmxs[cardId]
        # print(lastCard.tmx.door)
        for index in filter(lambda x: lastCard.tmx.door[x], range(4)):
            doorDir = self.getDoorDir(index, lastCard.angle)
            oppoDoor = self.oppoDoorDir[doorDir]
            for curDoor in filter(lambda x: tmx.door[x], range(4)):
                # print('newIndex:', curDoor)
                newPos = (lastCard.pos[0] + self.addPos[doorDir][0],
                          lastCard.pos[1] + self.addPos[doorDir][1])

                if self.isCollide(cardList, newPos):
                    continue

                turnAngle = self.getTurnAngle(oppoDoor, curDoor)
                yield PlunderCard(cardId, tmx, newPos, turnAngle)

    def recCreateMap(self, cardList, deep):
        if deep == 0:
            for lastCard in self.getNextCard(cardList, self.startId):
                cardList.append(lastCard)
                newList = [RecordCard(card.id, card.pos, card.angle)
                           for card in cardList]
                newList[0].pos = self.startPos
                self.mapRecord.append(newList)
                if len(self.mapRecord) >= config.PLUNDER_AMOUNT:
                    return
                del cardList[-1]
            return

        for cardId in self.cardFilter:
            '''
            if self.isCardUse(cardId, cardList):
                continue
            '''
            for newCard in self.getNextCard(cardList, cardId):
                cardList.append(newCard)
                self.recCreateMap(cardList, deep - 1)
                if len(self.mapRecord) >= config.PLUNDER_AMOUNT:
                    return

                del cardList[-1]

    def createAllMap(self, deep):
        self.mapRecord = []
        firstCard = PlunderCard(self.endId, self.endTmx, (64, -48), 0)
        cardList = [firstCard]
        self.recCreateMap(cardList, deep)
        print(len(self.mapRecord))
        [list(map(lambda x: x.getCardStr(), record))
         for record in self.mapRecord]
        self.mapRecord = ['#'.join(map(lambda x: x.cardStr, record))
                          for record in self.mapRecord]
        cardStrs = '[\n' + ' ' * 8 + "'" + \
            ("',\n" + ' ' * 8 + "'").join(self.mapRecord) + "'\n" + ' ' * 4 + ']'
        cardStrs = '%d: ' % deep + cardStrs
        return cardStrs

    def printOneRecord(self, record):
        strRet = ''
        for card in record:
            strRet += '%d:(%d,%d):%d   ' % (card.id,
                                            card.pos[0], card.pos[1], card.angle)

        return strRet

    def printRecord(self):
        for cardList in self.mapRecord:
            print(self.printOneRecord(cardList))

    def generate(self, fileName):
        fw = open(fileName, 'w')

        csList = []
        for deep in range(config.PLUNDER_CARDS_LOWER, config.PLUNDER_CARDS_LIMIT + 1):
            cardStrs = self.createAllMap(deep)
            csList.append(cardStrs)
        csStrs = (',\n' + ' ' * 4).join(csList)
        csStrs = 'cards = {\n' + ' ' * 4 + csStrs + '\n}\n'
        fw.write(csStrs)
        fw.write(self.plunderMonster.monsters)
        fw.write(self.plunderMonster.crystals)

    def test(self):
        self.generate(config.PLUNDER_FILE_NAME)
        '''
        import plunder_test as PSD
        data = PSD.cards[4][20]
        for i in data.split('#'):
            print(i)'''
