#listdir.py
import os 
import sys
import re
funcSet = set()
def findFunc(fileName, inner):
	pattern = re.compile('L[\w/]*' + inner + '[\w/]*', re.I)
	pattern = re.compile('Lcom/tencent/mobileqq/activity/[\w/]*' + inner + '[\w/]*', re.I)
	global funcSet
	fileRead = open(fileName, 'r')
	for line in fileRead:
		strFind = pattern.search(line)
		if (strFind):
			funcSet.add(strFind.group())
		


def findYourDir(level, path, inner, code):
	filetype = re.compile(r'(\.py|\.java)$')
	for i in os.listdir(path):
		if os.path.isdir(path + '/' + i):
			findYourDir(level + 1, path + '/' + i, inner, code)
		else:
			if (code == 'p'):
				fileFind = filetype.search(i)
				if (not fileFind):
					continue
			findFunc(path + '/' + i, inner)
				

def printSet():
	global funcSet
	print(len(funcSet))
	for i in funcSet:
		print(i)

if (len(sys.argv) == 2 and sys.argv[1] == '-h'):
	print('the first argv is path')
	print('the second argv is inner which you want to search')
if (len(sys.argv) == 3):
	findYourDir(0, sys.argv[1], sys.argv[2], 'a')

	printSet()

