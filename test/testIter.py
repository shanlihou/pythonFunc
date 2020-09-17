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


if __name__ == '__main__':
    aa = [2, 5, 64, 4, 32, 3, 4, 9, 3, 5, 6, 3, 2, 3]
    #print(len(filter(lambda x: x >5,aa)))
    print([0] * 10)

    aa = sorted(aa, reverse=True)
    for index, i in enumerate(getRankBySortedList(aa, lambda x: x)):
        print(index, i, aa[index])
    
    Test.test()
