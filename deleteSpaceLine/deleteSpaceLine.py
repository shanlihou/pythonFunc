#listdir.py
import os 
import sys
import re
import datetime
import shutil
import string
def deleteLine(fileName):
	fileRead = open(fileName, 'r')
	fileWrite = open(fileName + '.new', 'w')
	pattern = re.compile(r'^\s*$')
	for line in fileRead:
		strFind = pattern.search(line)
		if(not strFind):
			fileWrite.writelines(line)
		else:
			print(line)

if (len(sys.argv) == 2 and sys.argv[1] == '-h'):
	print('just input the fileName')
elif (len(sys.argv) == 2):
	deleteLine(sys.argv[1])

#ReadFileWithList(sys.argv[1])
#SingleConv(sys.argv[1])
#txtToCsvPath(sys.argv[1])
#txtToCsv(sys.argv[1])
#Rootpath = os.path.abspath('.') 
#print (Rootpath) 
#listyoudir(0, Rootpath)
#patchFile(sys.argv[1])
#cpFileByTime(sys.argv[1])
