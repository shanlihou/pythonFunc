#listdir.py
import os 
import sys
import re
import datetime
import shutil
import string
def GetDynamicLibrary(fileName, address):
	fileRead = open(fileName, 'r')
	pattern = re.compile(r'([0-9a-f]+)-([0-9a-f]+)\s+[rwxp-]+\s+[0-9a-f]+\s+\w+:\w+\s+\d+\s+(/.+)$')
	for line in fileRead:
		strFind = pattern.search(line)
		if (strFind):
			number1 = string.atoi(strFind.group(1), base=16)
			number2 = string.atoi(strFind.group(2), base=16)
			numberAddress = string.atoi(address, base=16)
			if(numberAddress < number2 and numberAddress > number1):
				retList = [strFind.group(3), numberAddress - number1]
				return retList
	return None

def GetAddressTable(fileName, fileMap):
	fileRead = open(fileName, 'r')
	pattern = re.compile(r'Dumping Not-Freed Pointers Changed Since Start:')
	patAddress = re.compile(r'\d+:\s+\d+:\s+\d+\s+\d+\s+ra=0x([0-9a-f]+)')
	fileWrite = open(fileName + '.new.txt', 'w')
	flagSearch = 0
	for line in fileRead:
		strFlag = pattern.search(line)
		if(strFlag):
			flagSearch = 1
		if(flagSearch == 1):
			strAddress = patAddress.search(line)
			if(strAddress):
				strLib = GetDynamicLibrary(fileMap, strAddress.group(1))
				if(strLib != None):
					number = '%x' %strLib[1]
					fileWrite.writelines(line[0:-1] + '      -------' + strLib[0] + '    ' + number + '\n')
				else:
					fileWrite.writelines(line)
			else:
				fileWrite.writelines(line)
		else:
			fileWrite.writelines(line)
if(len(sys.argv) == 3):
	GetAddressTable(sys.argv[1], sys.argv[2])
elif(len(sys.argv) == 2 and sys.argv[1] == '-h'):
	print('the first arg is the path of dmalloc.log')
	print('the second arg is the path of maps')

#CreateSplit(sys.argv[1])
#ReadFileWithList(sys.argv[1])
#SingleConv(sys.argv[1])
#txtToCsvPath(sys.argv[1])
#txtToCsv(sys.argv[1])
#Rootpath = os.path.abspath('.') 
#print (Rootpath) 
#listyoudir(0, Rootpath)
#patchFile(sys.argv[1])
#cpFileByTime(sys.argv[1])
