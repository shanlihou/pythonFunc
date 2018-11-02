# coding=utf-8
import os
import sys
import random
import utils
from singleton import singleton

g_root = r'E:\svn'
dataPath = os.path.join(
    g_root, r'Dev\Server\kbeWin\kbengine\assets\scripts\server_common')
sys.path.append(dataPath)
dataPath = os.path.join(
    g_root, r'Dev\Server\kbeWin\kbengine\assets\scripts\data')
sys.path.append(dataPath)
from DATA import gameconst
from DATA import BSGD
from DATA import PSD
from DATA import SWD


class RobCacheVal(object):
    def __init__(self, ownerGbId, lingqiLevel, robScore, name):
        self.ownerGbId = ownerGbId
        self.lingqiLevel = lingqiLevel
        self.robScore = robScore
        self.name = name

    def __lt__(self, other):
        return self.robScore < other.robScore

    def __ge__(self, other):
        return self.robScore >= other.robScore

    def __eq__(self, other):
        return self.robScore == other.robScore


class MatchPool(dict):
    def __init__(self, owner, lingqiKey):
        self.owner = owner
        self.lingqiKey = lingqiKey
        self.sortList = []
        self.sortTimer = 0

    def __setitem__(self, key, value):
        super(MatchPool, self).__setitem__(key, value)
        self.addSort(5)

    def pop(self, key, *args):
        super(MatchPool, self).pop(key, *args)
        self.addSort(5)

    def addSort(self, sortTime):
        self.onTimerSort()

    def onTimerSort(self):
        self.sortTimer = 0
        self.sortList = sorted(self.values())

    def _search(self, score):
        tmpVal = RobCacheVal(0, 0, score, '')
        low = 0
        high = len(self.sortList) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.sortList[mid] >= tmpVal:
                high = mid - 1
            else:
                low = mid + 1

        return low

    def getMatchList(self, warpGates, startScore, endScore):
        start = self._search(startScore)
        end = self._search(endScore)
        matchList = self.sortList[start:end]
        return list(filter(lambda x: x.ownerGbId not in warpGates, matchList))


@singleton
class RobStub(object):
    def __init__(self):
        self.matchPools = {}

    def _calcLingqiKey(self, lingqiLevel):
        # TODO rob:calc poolKey
        return lingqiLevel // 10

    def addRobInfo(self, ownerGbId, lingqiLevel, robScore, name):
        poolKey = self._calcLingqiKey(lingqiLevel)
        self.matchPools.setdefault(poolKey, MatchPool(self, poolKey))
        matchPool = self.matchPools[poolKey]
        matchPool[ownerGbId] = RobCacheVal(
            ownerGbId, lingqiLevel, robScore, name)

    def modifyLingqiLevel(self, originLevel, ownerGbId, lingqiLevel):
        oriKey = self._calcLingqiKey(originLevel)
        newKey = self._calcLingqiKey(lingqiLevel)
        matchPool = self.matchPools.get(oriKey, {})
        if ownerGbId not in matchPool:
            #ERROR_MSG('ckz: oriKey not in matchPool:', originLevel, ownerGbId, lingqiLevel)
            return

        if oriKey == newKey:
            matchPool[ownerGbId].lingqiLevel = lingqiLevel
            return

        robCacheVal = matchPool.pop(ownerGbId)
        robCacheVal.lingqiLevel = lingqiLevel
        self.matchPools.setdefault(newKey, MatchPool(self, newKey))
        matchPool = self.matchPools[newKey]
        matchPool[ownerGbId] = robCacheVal

    def _getMatchRegion(self, robScores, robScore, warpGateLv):
        beyond = 0
        for otherScore in robScores:
            if otherScore > robScore:
                beyond += 1

        firstMatchRange = BSGD.datas[warpGateLv]['firstMatchRange']
        return (robScore - firstMatchRange, robScore) if beyond > (len(robScores) / 2) else (robScore, robScore + firstMatchRange)

    def _calcNoOwnerAmount(self, warpGates):
        amount = 0
        for gbId in warpGates:
            if gbId < gameconst.PLUNDER_MAX_ID:
                amount += 1
        return amount

    def _randomNoOwner(self, key):
        return key * gameconst.PLUNDER_MAX_COUNT + min(random.randint(0, len(SWD.cards[4]) - 1), gameconst.PLUNDER_MAX_COUNT - 1)

    def getMatchList(self, box, playerGbId, warpGates, lingqiLevel, cangkuLv, robScore, num):
        matchList = []
        while num:
            num -= 1
            retData = self._match(playerGbId, warpGates, lingqiLevel, robScore)
            matchList.append(retData)
            warpGates.append(retData[0])

        box.onGetMatchList(matchList, robScore, lingqiLevel, cangkuLv)

    def onTimerSort(self, lingqiKey):
        matchPool = self.matchPools[lingqiKey]
        matchPool.onTimerSort()

    def _match(self, playerGbId, warpGates, lingqiLevel, robScore):
        noOwnerAmount = self._calcNoOwnerAmount(warpGates)
        warpGateLv = utils.getWarpGateLevel(robScore)
        matchProbability = BSGD.datas[warpGateLv]['matchProbability']
        maxSystemWorldNum = int(PSD.datas['maxSystemWorldNum']['value'])
        if noOwnerAmount < maxSystemWorldNum and random.random() < matchProbability:
            return self._randomNoOwner(4), 'no owner', 0

        lingqiKey = self._calcLingqiKey(lingqiLevel)
        matchPool = self.matchPools[lingqiKey]
        robScores = []
        for gbId in warpGates:
            if gbId in matchPool:
                robScores.append(matchPool[gbId].robScore)

        start, end = self._getMatchRegion(robScores, robScore, warpGateLv)
        addRange = 0
        enlargeRange = BSGD.datas[warpGateLv]['enlargeRange']
        enlargeRangeMax = BSGD.datas[warpGateLv]['enlargeRangeMax']
        while addRange <= enlargeRangeMax:
            matchList = matchPool.getMatchList(
                warpGates, start - addRange, end + addRange)
            matchList = list(
                filter(lambda x: x.ownerGbId != playerGbId, matchList))
            if not matchList:
                if not enlargeRange:
                    break

                addRange += enlargeRange
                continue

            data = random.choice(matchList)
            return data.ownerGbId, data.name, data.lingqiLevel

        return self._randomNoOwner(4), 'no owner', 0


if __name__ == '__main__':
    pass
