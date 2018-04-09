def printDataIn16(data):
    strPrint = ''
    for i in data:
        strPrint += '%x ' % ord(i)
    print strPrint
if __name__ == '__main__':
    test = [1, 3, 4, 2, 5, 9]
    print test[::2]
    print test[-3:]
    print reduce(lambda x,y:x+y,map(lambda x:test[x] + 3, range(0, len(test), 2)))
    print reduce(lambda x,y:x+y,map(lambda x: x+3, test[::2]))