import os
import sys
def findInner(fileName, keyword):
	fileRead = open(fileName, 'r')
	count = 0
	for line in fileRead:
		count += 1
		if (keyword in line):
			print(fileName + ':' + str(count))
			if len(line) < 200:
				print(line)

		
	
def listDir(path, keyword, level, choice = '-c'):
	pathList = os.listdir(path)
	for i in pathList:
		sonName = path + '/' + i
		if (os.path.isdir(sonName)):
			if i == '.svn':
				continue
			listDir(sonName, keyword, level + 1, choice)
		elif(sonName.endswith('.cpp') or sonName.endswith('.h') or sonName.endswith('.c') or sonName.endswith('.js')):
			findInner(sonName, keyword)
		elif sonName.endswith('.rar') or sonName.endswith('.o') or sonName.endswith('.a') or sonName.endswith('sonia'):
			continue
		else:
			if choice == '-a':
				findInner(sonName, keyword)
if len(sys.argv) == 3:
	listDir(sys.argv[1], sys.argv[2], 0)
elif len(sys.argv) == 4:
	listDir(sys.argv[1], sys.argv[2], 0, '-a')
	
