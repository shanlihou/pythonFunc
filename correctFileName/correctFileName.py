import os
import sys
import re
import platform
syst = 0#linux
if 'Windows' in platform.system():
	syst = 1
def correctName(path, fileName):
	orgName = ''
	if (syst == 1):
		orgName = path + '\\' + fileName
	else:
		orgName = path + '/' + fileName
	newName = ''
	if (not fileName.endswith(".png")):
		return
	for i in fileName:
		if (i <= '9' and i >= '0'):
			newName += i
			continue
		elif(i <= 'z' and i >= 'a'):
			newName += i
			continue
		elif(i == '.'):
			newName += i
			continue
		elif(i == '_'):
			newName += i
			continue
		elif(i <= 'Z' and i >= 'A'):
			i = chr(ord(i) - ord('A') + ord('a'))
			newName += i
			continue
		else:
			newName += '_'
	print(newName)
	if (syst == 1):
		newName = path + '\\' + newName
	else:
		newName = path + '/' + newName
	os.rename(orgName, newName)
		
def listyoudir(level, path): 
	for i in os.listdir(path): 
#		print ('     '*(level+1) + i)
		fileName = ''
		if (syst == 0):
			fileName = path + '/' + i
		else:
			fileName = path + '\\' + i
		if os.path.isdir(fileName):
#			print ('     '*(level+1) + i)
			listyoudir(level+1, fileName)
		else:
			print(fileName)
			correctName(path, i)

if (len(sys.argv) == 2):
	listyoudir(0, sys.argv[1])