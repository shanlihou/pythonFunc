import re
import sys
import string
def modifyTime(fileName):
	fileRead = open(fileName, 'r')
	fileWrite = open(fileName + '.new', 'w')
	firstTime = -1
	for line in fileRead:
		ret,strRet = modifyLine(line)
		if (ret == 0):
			fileWrite.write(line)
			continue
		if (firstTime == -1):
			firstTime = ret
		print(ret - firstTime)
		fileWrite.write(str(ret - firstTime) + strRet)

def modifyLine(line):	
	pat = re.compile(r'^(\d{2}):(\d{2}):(\d{2})')
	result = pat.search(line)
	ret = 0
	strRet = line
	if (result):
		ret = string.atoi(result.group(3))
		ret = ret + string.atoi(result.group(2)) * 60
		ret = ret + string.atoi(result.group(1)) * 3600
		strRet = line[result.end(3):]
	return ret, strRet
modifyTime(sys.argv[1])
