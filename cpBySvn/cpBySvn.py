import sys
import os
import re
def mkdir(fileName):
	pat = re.compile(r'(^.+/)[^/]+$')
	find = pat.search(fileName)
	if find:
		return find.group(1)
def cpBySvn(fileName, pathSrc, pathDst):
	typeDict = {}
	fileRead = open(fileName, 'r')
	for line in fileRead:
		listLine = line.split()
		print listLine[1]
		if not typeDict.has_key(listLine[1]):
			typeDict[listLine[1]] = []
		typeDict[listLine[1]].append(listLine[0])
	print typeDict.keys()
	print typeDict['Deleted']
	print typeDict['Normal']
	for i in typeDict['Added']:
		srcName = pathSrc + '/' + i
		dstName = pathDst + '/' + i
		dstDir = mkdir(dstName)
		if not os.path.exists(dstDir):
			os.makedirs(dstDir)
		os.system('cp %s %s' % (srcName, dstName))
	for i in typeDict['Modified']:
		srcName = pathSrc + '/' + i
		dstName = pathDst + '/' + i
		dstDir = mkdir(dstName)
		if not os.path.exists(dstDir):
			os.makedirs(dstDir)
		os.system('cp %s %s' % (srcName, dstName))
		
if len(sys.argv) == 4:
	cpBySvn(sys.argv[1], sys.argv[2], sys.argv[3])

