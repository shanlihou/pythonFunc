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


class MapCards(list):
    def __init__(self, cards):
        self.cards = cards

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

    def placeCards(self):
        mapCards = []
        # fix end card
        cardInfo = MapCardVal((64, -48), self.cards[1].cardId, self.cards[1].tmx, 0, -1)
        mapCards.append(cardInfo)
        tmpCards = Cards(self.cards[2:])
        tmpCards.append(self.cards[0])
        self.cards = tmpCards
        self.recPlaceCard(mapCards, 0)
        mapCards[0]['pos'] = self.startPos
        mapCards[0]['cardStr'] = self.getCardStr(mapCards[0])

        for card in mapCards:
            print(card)
            print(card['card'].door)
        self.mapCards = mapCards

