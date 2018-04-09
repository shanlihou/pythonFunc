import os
import sys
import re
def func(m):
	return m.group(1) + 'true'
def modifyPD(fileName):
	pat = re.compile(r'("SupportDevInit"\s:\s)(false)')
	fileRead = open(fileName, 'r')
	fileWrite = open(fileName + '.new', 'w')
	for line in fileRead:
		find = pat.search(line)
		if (find):
			print find.group()
			print find.group(1)
			print pat.subn(func, line)
			fileWrite.write(pat.subn(func, line)[0])
		else:
			fileWrite.write(line)
	fileRead.close()
	fileWrite.close()
	os.rename(fileName + '.new', fileName)
def getCount(strLine):
	count = 0
	rePlus = re.compile('([\{\[])')
	reMinus = re.compile('([\}\]])')
	count += len(rePlus.findall(strLine))
	count -= len(reMinus.findall(strLine))
	return count
def modifyKey(fileName, key, addFile):
	print fileName
	print key
	pat = re.compile(r'\s+"' + key + '"\s*:')
	count = 0
	flag = 0
	fileRead = open(fileName, 'r')
	fileAdd = open(addFile, 'r')
	fileWrite = open(fileName + '.new', 'w')
	strAdd = fileAdd.read()
	for line in fileRead:
		if flag == 0:
			find = pat.search(line)
			if find:
				print 'find'
				if ',' not in line:
					flag = 1
				else:
					fileWrite.write(strAdd)
			else:
				fileWrite.write(line)
					
		else:
			count += getCount(line)
			if count <= 0:
				flag = 0
				fileWrite.write(strAdd)
	fileRead.close()
	fileWrite.close()
	os.rename(fileName + '.new', fileName)
			
		
def recAddpd(path, key, addFile):
	pathList = os.listdir(path)
	for i in pathList:
		iName = path + '/' + i
		if (os.path.isdir(iName)):
			recAddpd(iName, key, addFile)
		elif i == 'ProductDefinition':
			modifyKey(iName, key, addFile)
recAddpd(sys.argv[1], sys.argv[2], sys.argv[3])
#modifyKey(sys.argv[1], sys.argv[2], sys.argv[3])
