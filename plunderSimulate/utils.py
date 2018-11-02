from DATA import BSGD



def getWarpGateLevel(robScore):
    for level, dataDict in BSGD.datas.items():
        scoreLowerLimit = dataDict['scoreLowerLimit']
        scoreLimit = dataDict['scoreLimit']
        if robScore < scoreLowerLimit:
            continue

        if scoreLimit != -1 and robScore > scoreLimit:
            continue

        return level

    return 0


def isAvatar(gbId):
    return gbId >= 10000
