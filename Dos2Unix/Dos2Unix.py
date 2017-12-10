#listdir.py
import os 
import sys
import re
import platform

def listyourdir(path): 
	pattern = re.compile(r'\.sh$')
	for i in os.listdir(path): 
		fileName = path + '/' + i
		if os.path.isdir(fileName):
#			print ('     '*(level+1) + i)
			listyourdir(fileName)
		else:
			find = pattern.search(fileName)
			if (find):
				print(fileName)
				os.system('dos2unix ' + fileName)

listyourdir(sys.argv[1])


