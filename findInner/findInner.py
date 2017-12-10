#listdir.py
import os 
import sys
import re
import platform
syst = 0#linux
if 'Windows' in platform.system():
	syst = 1
fileSet = set()
def findLine(fileName, pat):
	pattern = re.compile('nginx-1.6.0/(.+)$')
	strPat = pattern.search(pat)
	inner = re.compile(strPat.group(1))
	fileRead = open(fileName, 'r')
	listRead = fileRead.readlines()
	for i in range(len(listRead)):
		strFind = inner.search(listRead[i])
		if(strFind):
			print(strPat.group(1))
			print(i)
		

def findInner(fileName, inner):
#	pattern = re.compile(inner, re.I)
	global fileSet
	fileRead = open(fileName, 'r')
	count = 0
	for line in fileRead:
		count = count + 1
#		strFind = pattern.search(line)
		if(inner in line):
			if fileName not in fileSet:
				fileSet.add(fileName)
			print(fileName + ':' + str(count))
			print(line)
	return False
	
def qqCrackPrint():
	global fileSet
	fileWrite = open('qq.activity', 'w')
	for i in fileSet:
		print i
		fileWrite.writelines(i + '\n')

def listyoudir(level, path, inner, lineFile): 
	pattern = re.compile(inner)
	for i in os.listdir(path): 
#		print ('     '*(level+1) + i)
		fileName = ''
		if (syst == 0):
			fileName = path + '/' + i
		else:
			fileName = path + '\\' + i
		if os.path.isdir(fileName):
#			print ('     '*(level+1) + i)
			listyoudir(level+1, fileName, inner, lineFile)
		else:
			if (findInner(fileName)):
				print(fileName)
				findLine(lineFile, fileName)

def findYourDir(level, path, inner, code):
	filetype = re.compile(r'(\.py|\.java|\.smali)$')
	for i in os.listdir(path):
		fileName = ''
		if (syst == 0):
			fileName = path + '/' + i
		else:
			fileName = path + '\\' + i
	
		if os.path.isdir(fileName):
			findYourDir(level + 1, fileName, inner, code)
		else:
			if (code == 'p'):
				fileFind = filetype.search(i)
				if (not fileFind):
					continue
			if(findInner(fileName, inner)):
				print(fileName)

if (len(sys.argv) == 2 and sys.argv[1] == '-h'):
	print('the first argv is path')
	print('the second argv is inner which you want to search')
elif (len(sys.argv) == 4):
	if (sys.argv[3] == '-a'):
		findYourDir(0, sys.argv[1], sys.argv[2], 'a')
	else:
		listyoudir(0, sys.argv[1], sys.argv[2], sys.argv[3])

elif (len(sys.argv) == 3):
	findYourDir(0, sys.argv[1], sys.argv[2], 'p')
#	qqCrackPrint()



