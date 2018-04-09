import os
import sys
def addPd(fileName, strInsert):
	fileRead = open(fileName, 'r')
	fileWrite = open(fileName + '.new', 'w')
	fileStr = fileRead.read()
	index = 0
	index2 = 0
	for i in range(len(fileStr)):
		if fileStr[i] != ' ' and fileStr[i] != '\t' and fileStr[i] != '\n' and fileStr[i] != '\r':
			index = index2
			index2 = i
	print fileStr[index]
	print ord(fileStr[index])
	if index != 0:
		fileWrite.write(fileStr[:index + 1])
		fileWrite.write(strInsert)
		fileWrite.write(fileStr[index + 1:])
	fileRead.close()
	fileWrite.close()
	os.rename(fileName + '.new', fileName)
		
def recAddpd(path, strInsert):
	pathList = os.listdir(path)
	for i in pathList:
		iName = path + '/' + i
		if (os.path.isdir(iName)):
			recAddpd(iName, strInsert)
		elif i == 'ProductDefinition':
			addPd(iName, strInsert)
filepd = open(sys.argv[2])
strInsert = filepd.read()
recAddpd(sys.argv[1], strInsert)

