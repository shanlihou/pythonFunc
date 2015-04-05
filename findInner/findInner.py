#listdir.py
import os 
import sys
import re
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
	pattern = re.compile(inner)
	fileRead = open(fileName, 'r')
	count = 0
	for line in fileRead:
		count = count + 1
		strFind = pattern.search(line)
		if(strFind):
			print(fileName + ':' + str(count))
			print(line)
	return False

def listyoudir(level, path, inner, lineFile): 
	pattern = re.compile(inner)
	for i in os.listdir(path): 
#		print ('     '*(level+1) + i)
		if os.path.isdir(path + '/' + i):
#			print ('     '*(level+1) + i)
			listyoudir(level+1, path + '/' + i, inner, lineFile)
		else:
			if (findInner(path + '/' + i, inner)):
				print(path + '/' + i)
				findLine(lineFile, path + '/' + i)

def findYourDir(level, path, inner):
	filetype = re.compile(r'.py$')
	for i in os.listdir(path):
		if os.path.isdir(path + '/' + i):
			findYourDir(level + 1, path + '/' + i, inner)
		else:
			fileFind = filetype.search(i)
			if (not fileFind):
				continue
			if(findInner(path + '/' + i, inner)):
				print(path + '/' + i)

if (len(sys.argv) == 2 and sys.argv[1] == '-h'):
	print('the first argv is path')
	print('the second argv is inner which you want to search')
elif (len(sys.argv) == 4):
	listyoudir(0, sys.argv[1], sys.argv[2], sys.argv[3])
elif (len(sys.argv) == 3):
	findYourDir(0, sys.argv[1], sys.argv[2])



