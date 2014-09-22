#listdir.py
import os 
import sys
import re
import datetime
import shutil
import string
def CreateSplit(fileName):
	pattern = re.compile(r'\\x(\w+)')
	fileRead = open(fileName, 'r')
	fileWrite = open(fileName[:-3] + 'new.txt', 'w')
	for line in fileRead:
		ordList = pattern.findall(line)
		print(ordList)
		numList = range(len(ordList))
		for i in range(len(ordList)):
			numList[i] = Conv16StrToNum(ordList[i])
			Conv16StrTo2Str(ordList[i])
			fileWrite.writelines(chr(numList[i]))
		print(numList)
def Conv16StrToNum(str16):
	count = 0
	for i in str16:
		num = ord(i)
		if num >= ord('a') and num <= ord('z'):
			count = count * 16 + num - ord('a') + 10
		elif num >= ord('0') and num <= ord('9'):
			count = count * 16 + num - ord('0')
	return count

def Conv16StrTo2Str(str16):
	count = 0
	str2 = ''
	print(str16)
	for i in str16:
		num = ord(i)
		if num >= ord('a') and num <= ord('z'):
			count = count * 16 + num - ord('a') + 10
		elif num >= ord('0') and num <= ord('9'):
			count = count * 16 + num - ord('0')
		for i in range(4):
			if (count & (1 << (3 - i))) != 0:
				str2 = str2 + str(1)
			else :
				str2 = str2 + str(0)
		str2 = str2 + ' '
	print(str2)

result = 0x2b243428 - 0x2b238000
print(result)
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
