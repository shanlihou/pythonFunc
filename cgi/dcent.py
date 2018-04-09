import random
import numpy
class dscent:
    def __init__(self):
        self.filename = 'data.txt'
    def f(self, x):
        return 2 * x + 8
        
    def createData(self):
        dataSet = []
        for i in xrange(100):
            x = random.uniform(0, 1000)
            rand = random.uniform(-4, 4)
            y = self.f(x) + rand
            if rand < 0:
                dataSet.append([x, y, 0])
            else:
                dataSet.append([x, y, 1])
        fw = open(self.filename, 'wb')
        for i in dataSet:
            fw.write(str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + '\n')
        return dataSet
    def readData(self):
        fr = open(self.filename)
        dataSet = []
        for line in fr:
            dataSet.append(map(float, line.strip().split(' ')))
        print dataSet
        return dataSet
    def descent(self, dataSet):
        h = 0.000001
        m = 0.0
        b = 0.0
        dLen = len(dataSet)
        for i in xrange(150):
            tmpB = 0.0
            tmpM = 0.0
            for point in dataSet:
                x = point[0]
                y = point[1]
                error = y - (x * m + b)
                tmpM -= h * x * error / dLen
                tmpB -= h * error / dLen
                #print m, b, error, x, y
            m -= tmpM
            b -= tmpB
            print m, b
        print m, b
        return m, b
    def sigmoid(self, x):
        return 1.0 / (1 + numpy.exp(-x))
    def errorByWei(self, dataSet, wei):
        testVec = self.testResult(dataSet, wei)
        return self.calcError(dataSet, testVec)
        
    def calcError(self, dataSet, testVec):
        dataMat = numpy.array(map(lambda x:(x[0], x[1], 1), dataSet))
        dataMat = numpy.mat(dataMat)
        classVec = map(lambda x:x[-1], dataSet)
        testVec = numpy.mat(testVec)
        error = classVec - testVec
        des = error * dataMat
        #print des
        pow2 = numpy.power(error, 2)
        #print pow2
        m, n = numpy.shape(pow2)
        mul = numpy.ones((n, 1))
        #print mul
        ret = numpy.dot(pow2, mul)
        ret = numpy.array(ret)[0][0]
        print 'ret:', ret
        return ret
        
        
    def descent2(self, dataSet):
        dataMat = numpy.array(map(lambda x:(x[0], x[1], 1), dataSet))
        dataMat = numpy.mat(dataMat)
        classVec = map(lambda x:x[-1], dataSet)
        print dataMat
        #print dataMat
        #print classVec
        #print dataMat
        m, n = numpy.shape(dataSet)
        w = numpy.ones((1, n))
        step = 0.001
        errorList = []
        weiList = []
        for nothing in xrange(1500):
            step = 0.1 / (1 + nothing) + 0.0001
            ret = self.sigmoid(w * dataMat.transpose())
            error = classVec - ret
            #print error
            #print 'error:', ret
            des = error * dataMat * step
            w = w + des
            print 'des:', des
            print w
            errorList.append(self.errorByWei(dataSet, w))
            weiList.append(numpy.array(w)[0])
            '''
            for i in xrange(m):
                #print w * dataMat[i].transpose()
                error = self.sigmoid(w * dataMat[i].transpose())
                #print error
                '''
        return w, errorList, weiList
    def plotError(self, errorList, weiList):
        import matplotlib.pyplot as plt
        '''
        dataMat,labelMat=loadDataSet()
        dataArr = array(dataMat)
        n = shape(dataArr)[0] 
        xcord1 = []; ycord1 = []
        xcord2 = []; ycord2 = []
        for i in range(n):
            if int(labelMat[i])== 1:
                xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
            else:
                xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])
                '''
        fig = plt.figure()
        ax = fig.add_subplot(111)
        '''
        ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
        ax.scatter(xcord2, ycord2, s=30, c='green')'''
        x = numpy.arange(0, 150, 1)
        y = errorList
        print 'x:', x
        print 'y:', y
        ax.plot(x, y)
        print weiList
        y = map(lambda x:x[0], weiList)
        ax.plot(x, y, color='blue')
        y = map(lambda x:x[1], weiList)
        ax.plot(x, y, color='red')
        y = map(lambda x:x[2], weiList)
        ax.plot(x, y, color='yellow')
        plt.xlabel('X1'); plt.ylabel('X2');
        plt.show()
    def plotResult(self, dataSet, weights, weiList):
        import matplotlib.pyplot as plt
        xcord1 = []; ycord1 = []
        xcord2 = []; ycord2 = []
        m, n = numpy.shape(dataSet)
        for i in range(m):
            if int(dataSet[i][2])== 1:
                xcord1.append(dataSet[i][0]); ycord1.append(dataSet[i][1])
            else:
                xcord2.append(dataSet[i][0]); ycord2.append(dataSet[i][1])
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
        ax.scatter(xcord2, ycord2, s=30, c='green')
        x = numpy.arange(0, 1500.0, 1)
        weights = numpy.array(weights)[0]
        y = (-weights[2]-weights[0]*x)/weights[1]
        ax.plot(x, y)
        y = map(lambda x: x[0] / x[1], weiList)
        ax.plot(x, y, color='red')
        plt.xlabel('X1'); plt.ylabel('X2');
        plt.show()
    
    def testResult(self, dataSet, w):
        w = w.getA()[0]
        #print 'w:', w, w[0]
        retList = []
        for i in dataSet:
            z = i[0] * w[0] + i[1] * w[1] + w[2]
            retList.append(self.sigmoid(z))
            #print self.sigmoid(z), i[2]
        return retList
        
    def test(self):
        dataSet = self.readData()
        if 1:
            w, errorList, weiList = self.descent2(dataSet)
            self.testResult(dataSet, w)
            m, n = numpy.shape(dataSet)
            self.calcError(dataSet, numpy.zeros((1, m)))
            self.calcError(dataSet, numpy.ones((1, m)))
            #self.plotError(errorList, weiList)
            self.plotResult(dataSet, w, weiList)
        else:
            m, b = self.descent(dataSet)
            print 'end:', m,b
if __name__ == '__main__':
    des = dscent()
    des.test()