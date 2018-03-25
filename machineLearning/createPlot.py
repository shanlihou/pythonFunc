import matplotlib.pyplot as plt
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.axl.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', 
                            xytext=centerPt, textcoords='axes fraction',
                            va='center', ha='center', bbox=nodeType, arrowprops=arrow_args)
def createPlot():
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    createPlot.axl = plt.subplot(111, frameon=False)
    print createPlot.axl
    plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
    plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
    plt.show()
def plotMidString(cntrPt, parentPt, txtString):
    xMid = (cntrPt[0] + parentPt[0]) / 2.0
    yMid = (cntrPt[1] + parentPt[1]) / 2.0
    createPlot.axl.text(xMid, yMid, txtString)

def plotTree(myTree, parentPt, nodeText):
    pass
if __name__ == '__main__':
    createPlot()
    