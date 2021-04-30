import testImport
import random
import time


def getRankBySortedList(sortList, keyFunc):
    rank = 0
    curRank = 0
    lastVal = -1
    retList = []
    for i in sortList:
        rank += 1
        val = keyFunc(i)
        if val != lastVal:
            lastVal = val
            curRank = rank

        yield curRank


class Test(object):
    dic = {
        'a': {
            'b': {
                'd': {
                    0: 1
                }
            },
            'c': {
                'e': {
                    0: 2
                }
            }
        }
    }

    @classmethod
    def matchPlayDic(cls, itemList, index, dic):
        if 0 in dic:
            return dic[0]

        if index >= len(itemList):
            return 0

        curItemId = itemList[index]
        ret = 0
        if curItemId in dic:
            ret = cls.matchPlayDic(itemList, index + 1, dic[curItemId])

        if not ret:
            ret = cls.matchPlayDic(itemList, index + 1, dic)

        return ret

    @classmethod
    def test(cls):
        ret = cls.matchPlayDic(['a', 'b', 'c', 'e'], 0, cls.dic)

        print(ret)
        aa = [1, 2, 3, 4]
        bb = aa[3:]
        print(bb)
        testImport.abcd()


CORRECT_TIME = time.localtime(0).tm_hour


def getDayOffsetFromEpoch(now):
    return now // 86400


def getDay(now):
    gameTS = now + (CORRECT_TIME - 5) * 3600
    return getDayOffsetFromEpoch(gameTS)


if __name__ == '__main__':
    t = int(time.time())
    t = (2021, 2, 4, 5, 0, 0, 1, 48, 0)
    t = time.mktime(t)
    print(t)
    print(time.localtime(t))
    print(getDay(t - 5))
    print(getDay(t + 5))
    aa = {}
    for i in range(10):
        aa[i] = random.random()

    _it = iter(aa.keys())
    aa.pop(5)
    aa.pop(9)
    for i in _it:
        print(i)
