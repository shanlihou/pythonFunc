import re
import sys
def AddLog(path):
	pattern = re.compile(r'^\s*[\w\*]+\s+([^\s\(]+)\(')
	patternBra = re.compile(r'^\{')
	fileRead = open(path, 'r')
	fileWrite = open(path + '.new', 'w')
	funcFlag = 0
	num = 0
	funcName = ''
	for line in fileRead:
		fileWrite.writelines(line)
		num = num + 1
		if(funcFlag == 0):
			patFind = pattern.search(line)
			if (patFind):
				funcFlag = 1
				funcName = patFind.group(1)
				print(funcName)
				print(line)
		else:
			patFind = patternBra.search(line)
			if (patFind):
				funcFlag = 0
				print(line)
				num = num + 1
				fileWrite.writelines('errorf("shanlihou %s:%s:%d\\n", __FILE__, __FUNCTION__, __LINE__);\n')

			
		
AddLog(sys.argv[1])
		
