from math import log
import matplotlib.pyplot as plt
from seaborn.tests import PlotTestCase
#from createPlot import plotTree

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.axl.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', 
                            xytext=centerPt, textcoords='axes fraction',
                            va='center', ha='center', bbox=nodeType, arrowprops=arrow_args)
def createPlot(tree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.axl = plt.subplot(111, frameon=False, **axprops)
    print createPlot.axl
    plotTree.totalW = float(getTotalLeaves(tree))
    plotTree.totalD = float(getTreeDepth(tree))
    plotTree.xOff = -0.5 / plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(tree, (0.5, 1.0), '')
    
    #plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
    #plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
    plt.show()
def plotMidString(cntrPt, parentPt, txtString):
    xMid = (cntrPt[0] + parentPt[0]) / 2.0
    yMid = (cntrPt[1] + parentPt[1]) / 2.0
    createPlot.axl.text(xMid, yMid, txtString)
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
    bestInfoGain = -100.0
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
    return bestFeat
def getMaxTimesClass(classList):
    classDict = {}
    maxTimes = 0
    retClass = None
    for i in classList:
        classDict[i] = classDict.get(i, 0) + 1
        if maxTimes < classDict[i]:
            maxTimes = classDict[i]
            retClass = i
    return retClass
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(dataSet):
        return classList[0]
    if len(dataSet[0]) == 1:
        return getMaxTimesClass(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueValue = set(featValues)
    for value in uniqueValue:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree
def getTotalLeaves(tree):
    totalLeaves = 0
    if not isinstance(tree, dict):
        return 1
    for key in tree:
        totalLeaves += getTotalLeaves(tree[key])
    return totalLeaves

def getTreeDepth(tree):
    deep = 0
    if not isinstance(tree, dict):
        return 0
    
    for key in tree:
        tmpDep = getTreeDepth(tree[key])
        if isinstance(key, int):
            tmpDep += 1
        
        if deep < tmpDep:
            deep = tmpDep
    return deep
def plotTree(tree, parentPt, nodeText):
    numLeaves = getTotalLeaves(tree)
    depth = getTreeDepth(tree)
    firstStr = tree.keys()[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeaves)) / 2.0 / plotTree.totalW,
              plotTree.yOff)
    plotMidString(cntrPt, parentPt, nodeText)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = tree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if isinstance(secondDict[key], dict):
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidString((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD
def classify(tree, featLabels, testVec):
    firstStr = tree.keys()[0]
    secondDict = tree[firstStr]
    featIndex = featLabels.index(firstStr)
    for i in secondDict:
        if testVec[featIndex] == i:
            if isinstance(secondDict[i], dict):
                classLabel = classify(secondDict[i], featLabels, testVec)
            else:
                classLabel = secondDict[i]
    return classLabel
def storeTree(tree, filename):
    import pickle
    with open(filename, 'w') as fw:
        pickle.dump(tree, fw)
def grabTree(filename):
    import pickle
    with open(filename, 'r') as fr:
        return pickle.load(fr)
def test():
    dataSet, labels = createDataSet()
    tmp = []
    map(lambda x:tmp.append(x), labels)
    print calcEntropy(dataSet)
    print splitDataSet(dataSet, 0, 1)
    print 'ret:', chooseBestFeatureToSplit(dataSet)
    tree = createTree(dataSet, labels)
    print tree
    print 'leaf:', getTotalLeaves(tree)
    print 'deep:', getTreeDepth(tree)
    print tmp
    print classify(tree, tmp, [0, 1])
    print classify(tree, tmp, [1, 1])
    print classify(tree, tmp, [1, 0])
    storeTree(tree, r'D:\tree.txt')
    createPlot(tree)
def test1():
    tree = grabTree(r'D:\tree.txt')
    dataSet, labels = createDataSet()
    createPlot(tree)
    
if __name__ == '__main__':
    test1()