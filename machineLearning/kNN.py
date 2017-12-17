from numpy import *
import matplotlib
import matplotlib.pyplot as plt
import operator
def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels
def classify0(intX, dataSet, labes, k):
    print dataSet.shape
    dataSetSize = dataSet.shape[0]
    diffMat = tile(intX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    print sqDiffMat
    distances = sqDiffMat.sum(axis = 1) ** 0.5
    print distances
    sortedRet = distances.argsort()
    print sortedRet
    classCount = {}
    help(classCount.get)
    for i in xrange(k):
        tmpLabel = labes[sortedRet[i]]
        classCount[tmpLabel] = classCount.get(tmpLabel, 0) + 1
    sortedClass = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    print sortedClass
    return sortedClass[0][0]
def test():
    group, labels = createDataSet()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(group[:, 0], group[:, 1])
    plt.show()
    print group
    print labels
    classify0((3, 2), group, labels, 3)

if __name__ == '__main__':
    test()