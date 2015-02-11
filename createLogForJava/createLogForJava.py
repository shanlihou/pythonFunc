#listdir.py
import os 
import sys
import re
def matchClass(funcName, classList):
	for className in classList:
		if (funcName == className):
			print(classList)
			print(funcName)

			return True
	return False

def addImport(fileName):
	packagePat = re.compile(r'^package')
	importPat = re.compile(r'^import android.util.Log;')
	fileRead = open(fileName, 'r')
	fileReadList = fileRead.readlines()
	flagPac = -1
	flagImp = False
	for i in range(len(fileReadList)):
		strPackage = packagePat.search(fileReadList[i])
		if(strPackage):
			flagPac = i
		strImp = importPat.search(fileReadList[i])
		if(strImp):
			flagImp = True
	
	if(flagImp == False):
		fileWrite = open(fileName + '.new', 'w')
		for i in range(len(fileReadList)):
			fileWrite.writelines(fileReadList[i])
			if(i == flagPac):
				fileWrite.writelines('import android.util.Log;\n')
		fileRead.close()
		fileWrite.close()
		os.rename(fileName + '.new', fileName)

		

	
def AddLogByFuncName(fileName, tagName):
#	pattern = re.compile(r'(private|public)(?:\s\w+)*(\s\w+)\s*(')
	pattern = re.compile(r'(private|public)(?:\s\w+)*(\s\w+)\s*\(')
	brackets = re.compile(r'(\)\s*\{)')
	className = re.compile(r'class\s+(\w+)')
	classList = [None]

	fileRead = open(fileName, 'r')
	fileWrite = open(fileName + '.new', 'w')
	flag = 0
	strFuncName = ''
	importLog = 1
	for line in fileRead:
		strClass = className.search(line)
		if(strClass):
			classList[0:0] = [strClass.group(1)]
		strFind = pattern.search(line)		
		if(strFind):
			flag = 1
			strFuncName = strFind.group(2)
	
		strBrackets = brackets.search(line)
		if(flag == 1):
			if(strBrackets):
				strWrite = brackets.sub(r'\1Log.d("' + tagName + '", "' + fileName + ':' + strFuncName + '");', line)
				if(matchClass(strFuncName[1:], classList)):
					fileWrite.writelines(line)
				else:
					fileWrite.writelines(strWrite)
				flag = 0
			else:
				fileWrite.writelines(line)
		else:
			fileWrite.writelines(line)
	fileRead.close()
	fileWrite.close()
	os.rename(fileName + '.new', fileName)

def listyoudir(level, path, tagName): 
	pattern = re.compile(r'.+.java$')
	for i in os.listdir(path): 
		if os.path.isdir(path + '/' + i):
			listyoudir(level+1, path + '/' + i, tagName)
		else:
			strFind = pattern.search(i)
			if(strFind):
				addImport(path + '/' + i)
				AddLogByFuncName(path + '/' + i, tagName)

if (len(sys.argv) == 2 and sys.argv[1] == '-h'):
	print('argv 1 is the path of you want to add log, and it will add the log of func for every java')
elif (len(sys.argv) == 3):
	listyoudir(0, sys.argv[1], sys.argv[2])


