import random
import TMX

class CardVal(object):
    def __init__(self, cardId, tmx):
        self.cardId = cardId
        self.tmx = tmx


class Cards(list):
    cardFilter = [62000006, 62000007, 62000012]

    def __init__(self, tmxList):
        self.tmxList = tmxList

    def cardFilt(self, cardId):
        return cardId in self.cardFilter

    def parseTmx(self, tmxID):
        tmx = TMX.TMX(self.tmxList[tmxID])
        tmx.parseAllInfo()
        return tmx

    def randomCards(self, startId, endId, count):
        cards = []
        cards.extend((startId, endId))
        count = count - 2
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
            self.append(CardVal(card, tmx))

class MapCardVal(object):
    def __init__(self, pos, id, card, angle, useDoor):
        self.pos = pos
        self.id = id
        self.card = card
        self.angle = angle
        self.useDoor = useDoor

    def getCardStr(self):
        self.cardStr = '|'.join([str(self.id), str(self.pos), str(self.angle)])


class MapCards(list):
    oppoDoorDir = [2, 3, 0, 1]
    addPos = [(-32, 0), (0, -32), (32, 0), (0, 32)]
    startPos = (64, -64)

    def __init__(self, cards):
        self.cards = cards

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

    def getDoorDir(self, door, angle):
        angle /= 90
        return int((door - angle + 4) % 4)

    def getChoiceDoor(self, door, useDoor):
        Door = list(filter(lambda x: door[x] and x not in useDoor, range(4)))
        return random.choice(Door)

    def getTurnAngle(self, oppoDoor, curDoor):
        return ((curDoor + 4 - oppoDoor) % 4) * 90

    def getNewCardInfo(self, info, card, useDict):
        newInfo = {}
        couldUseDoorList = self.getCouldUseDoor(
            useDict, info.card.door, card.tmx.door, info.useDoor)
        if not couldUseDoorList:
            return None, useDict
        # door = self.getChoiceDoor(info['card'].door, info['useDoor'])
        door = random.choice(couldUseDoorList)
        doorDir = self.getDoorDir(door, info.angle)
        oppoDoor = self.oppoDoorDir[doorDir]
        curDoor = self.getChoiceDoor(card.tmx.door, useDict.get(door, []))
        newPos = (info.pos[0] + self.addPos[doorDir][0],
                  info.pos[1] + self.addPos[doorDir][1])

        turnAngle = self.getTurnAngle(oppoDoor, curDoor)
        newInfo = MapCardVal(newPos, card.cardId, card.tmx, turnAngle, curDoor)
        newInfo.getCardStr()
        useDict.setdefault(door, [])
        useDict[door].append(curDoor)
        return newInfo, useDict

    def isValidCardPos(self, mapCards, pos):
        for index, mapCard in enumerate(mapCards):
            cPos = mapCard.pos
            if not index:
                cPos = self.startPos

            w = mapCard.card.w
            h = mapCard.card.h
            if pos[0] + 32 > cPos[0] and pos[0] < cPos[0] + w and\
                    pos[1] < cPos[1] + h and pos[1] + 32 > cPos[1]:
                return False

        return True

    def recPlaceCard(self, mapCards, deep):
        print('recP', len(self.cards), deep)
        card = self.cards[deep]
        useDict = {}
        while 1:
            info, useDict = self.getNewCardInfo(mapCards[-1], card, useDict)
            if not info:
                break

            if not self.isValidCardPos(mapCards, info.pos):
                continue

            mapCards.append(info)
            if deep == len(self.cards) - 1:
                return True

            ret = self.recPlaceCard(mapCards, deep + 1)
            if ret:
                return True

            del mapCards[-1]

        return False

    def placeCards(self):
        mapCards = []
        # fix end card
        cardInfo = MapCardVal((64, -48), self.cards[1].cardId, self.cards[1].tmx, 0, -1)
        mapCards.append(cardInfo)
        tmpCards = self.cards[2:]
        tmpCards.append(self.cards[0])
        self.cards = tmpCards
        self.recPlaceCard(mapCards, 0)
        mapCards[0].pos = self.startPos
        mapCards[0].getCardStr()

        for card in mapCards:
            print(card)
            print(card.card.door)

        self.extend(mapCards)

