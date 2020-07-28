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


if __name__ == '__main__':
    aa = [2, 5, 64, 4, 32, 3, 4, 9, 3, 5, 6, 3, 2, 3]
    aa = sorted(aa, reverse=True)
    for index, i in enumerate(getRankBySortedList(aa, lambda x: x)):
        print(index, i, aa[index])
