#istdir.py
import os 
import sys
import re
def DeleteLogByTag(fileName, tagName):
	fileRead = open(fileName, 'r')
#pattern = re.compile(r'Log.d\(' + tagName + '","' + fileName + ':' + r'.+$')
	pattern = re.compile(r'Log\.d\("' + tagName + '", "' + r'.+$')
	fileWrite = open(fileName + '.new', 'w')
	for line in fileRead:
		strFind = pattern.search(line)
		if(strFind):
			fileWrite.writelines(pattern.sub('', line))
		else:
			fileWrite.writelines(line)
	fileRead.close()
	fileWrite.close()
	os.rename(fileName + '.new', fileName)
			
def listyoudir(level, path, tagName): 
	pattern = re.compile(r'.+.java')
	for i in os.listdir(path): 
		if os.path.isdir(path + '/' + i):
			listyoudir(level+1, path + '/' + i, tagName)
		else:
			strFind = pattern.search(i)
			if(strFind):
				DeleteLogByTag(path + '/' + i, tagName)

if (len(sys.argv) == 2 and sys.argv[1] == '-h'):
	print('argv 1 is the path of you want to add log, and it will add the log of func for every java')
elif (len(sys.argv) == 3):
	listyoudir(0, sys.argv[1], sys.argv[2])


