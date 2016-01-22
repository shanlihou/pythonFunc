import sys
import os
import re
import string
import platform
def createSmaliLog(fileName):
	reLocal = re.compile(r'.locals (\d+)')
	fileName = fileName[:-1]
	print('filename:' + fileName)
	fileRead = open(fileName, 'r')
	fileWrite = open(fileName + '.new', 'w')
	nLocal = 0
	count = 0
	fileName = dealFileName(fileName)
	for line in fileRead:
		localFind = reLocal.search(line)
		if (localFind):
			nLocal = string.atoi(localFind.group(1))
		if (".prologue" in line):
			if (nLocal != 0):
				fileWrite.writelines(line)
				count = count + 1
				fileWrite.writelines("    const-string v0, \"" + fileName + ':' + str(count + 1) +  '"\n')
				fileWrite.writelines("    invoke-static {v0}, Lcrack;->log(Ljava/lang/String;)V\n")
				count = count + 2
		else:
			fileWrite.writelines(line)
			count = count + 1
	fileRead.close()
	fileWrite.close()
	os.remove(fileName)
	os.rename(fileName + '.new', fileName)
def dealFileName(fileName):
	if 'Linux' in platform.system():
		return fileName
	return fileName.replace('\\', '\\\\')
		
def openAllFile(fileName):
	fileRead = open(fileName, 'r')
	for line in fileRead:
		print(line)
		createSmaliLog(line)

if (len(sys.argv) == 2):
	openAllFile(sys.argv[1])
