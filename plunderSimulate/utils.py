from DATA import BSGD


def getWarpGateLevel(robScore):
    for level, dataDict in BSGD.datas.items():
        scoreLowerLimit = dataDict['scoreLowerLimit']
        scoreLimit = dataDict['scoreLimit']
        if scoreLowerLimit and robScore < scoreLowerLimit:
            continue

        if scoreLimit and robScore > scoreLimit:
            continue

        return level


def isAvatar(gbId):
    return gbId >= 10000
