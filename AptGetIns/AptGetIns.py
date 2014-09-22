#listdir.py
import os 
import sys
import re
def getCmdAptGet(fileName):
	pattern = re.compile(r'sudo apt-get install .+$')
	suffix = re.compile(r'\\\s*$')
	fileRead = open(fileName, 'r')
	flag = 0
	for line in fileRead:
#		print(line)
		if(flag == 1):
			print(line)
			lineLen = len(line)
			suffixFind = suffix.search(line)
			if(suffixFind):
				continue
			else:
				flag = 0

		strFind = pattern.search(line)

		if(strFind):
			findLen = len(strFind.group())
			if(strFind.group()[findLen - 1] == '\\'):
				flag = 1
			print(strFind.group())
getCmdAptGet(sys.argv[1])

#if (len(sys.argv) == 2 and sys.argv[1] == '-h'):
#	print('the first argv is path')
#	print('the second argv is inner which you want to search')
#elif (len(sys.argv) == 4):
#	listyoudir(0, sys.argv[1], sys.argv[2], sys.argv[3])
#

