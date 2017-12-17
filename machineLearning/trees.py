from math import log

def calcEntropy(dataSet):
    numEntries = len(dataSet)
    labelDict = {}
    for featVec in dataSet:
        label = featVec[-1]
        labelDict[label] = labelDict.get(label, 0) + 1
    entropy = 0.0
    for key in labelDict:
        prob = float(labelDict[key]) / numEntries
        entropy -= prob * log(prob, 2)
    return entropy
def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcEntropy(dataSet)
    bestInfoGain = 0.0
    bestFeat = -1
    for i in xrange(numFeatures):
        featList = [example[i] for example in dataSet]
        featSet = set(featList)
        newEntropy = 0.0
        for j in featSet:
            subDataSet = splitDataSet(dataSet, i, j)
            prob = len(subDataSet) / float(len(dataSet))
            print 'prob:', prob
            newEntropy += prob * calcEntropy(dataSet)
            print newEntropy
        infoGain = baseEntropy - newEntropy
        print 'infoGain:', infoGain
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeat = i
    return bestInfoGain, bestFeat
def test():
    dataSet, labels = createDataSet()
    print calcEntropy(dataSet)
    print splitDataSet(dataSet, 0, 1)
    print 'ret:', chooseBestFeatureToSplit(dataSet)
if __name__ == '__main__':
    test()