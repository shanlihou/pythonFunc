import re
import sys
import os
def DeletePyLog(fileName, pat):
	patSearch = re.compile(pat)
	fileRead = open(fileName, 'r')
	fileWrite = open(fileName + '.new', 'w')
	for line in fileRead:
		patFind = patSearch.search(line)
		if (patFind):
			print(line)
		else:
			fileWrite.writelines(line)
	fileRead.close()
	fileWrite.close()
	os.rename(fileName + '.new', fileName)

def listyoudir(level, path, tagName): 
	pattern = re.compile(r'.+.py$')
	for i in os.listdir(path): 
		if os.path.isdir(path + '/' + i):
			listyoudir(level+1, path + '/' + i, tagName)
		else:
			strFind = pattern.search(i)
			if(strFind):
				DeletePyLog(path + '/' + i, tagName)


listyoudir(0, sys.argv[1], sys.argv[2])
