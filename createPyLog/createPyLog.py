#listdir.py
import os 
import sys
import re
def countBrackets(strBrack):
	count = 0
	for i in strBrack:
		if (i == '('):
			count = count + 1
		elif (i == ')'):
			count = count - 1
	return count


def AddLogByDef(fileName, tagName):
	pattern = re.compile(r'^(\s*)def\s*(\w+)\(')
	patSpace = re.compile(r'^(\s*)\S')
	fileRead = open(fileName, 'r')
	fileWrite = open(fileName + '.new', 'w')
	flag = -1
	count = 0
	for line in fileRead:
		strFind = pattern.search(line)
		if (strFind):
			if (flag != -1):
				strSpace = patSpace.search(line)
				if (strSpace):
					print(strSpace.group(1) + strWrite)
					count = count + 1
					fileWrite.writelines(strSpace.group(1) + strWrite + '\n')
			strWrite = 'print(\'' + fileName + ':' + strFind.group(2) + ' ' + str(count) + '\')'
			print(line)
			flag = countBrackets(line)
			fileWrite.writelines(line)
			continue
		if (flag == 0):
			strSpace = patSpace.search(line)
			if (strSpace):
				print(strSpace.group(1) + strWrite)
				count = count + 1
				fileWrite.writelines(strSpace.group(1) + strWrite  + '\n')
			flag = -1
		elif (flag > 0):
			flag = flag + countBrackets(line)
		count = count + 1
		fileWrite.writelines(line)
	fileRead.close()
	fileWrite.close()
	os.rename(fileName + '.new', fileName)
	

def listyoudir(level, path, tagName): 
	pattern = re.compile(r'.+.py$')
	if (not os.path.isdir(path)):
		AddLogByDef(path, tagName)
		return
	for i in os.listdir(path): 
		if os.path.isdir(path + '/' + i):
			listyoudir(level+1, path + '/' + i, tagName)
		else:
			strFind = pattern.search(i)
			if(strFind):
				AddLogByDef(path + '/' + i, tagName)

if (len(sys.argv) == 2 and sys.argv[1] == '-h'):
	print('argv 1 is the path of you want to add log, and it will add the log of func for every java')
elif (len(sys.argv) == 3):
	listyoudir(0, sys.argv[1], sys.argv[2])
