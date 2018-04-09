import sys
import re
def addLogMutex(fileName):
	pattern = re.compile(r'm_Mutex')
	fileRead = open(fileName, 'r')
	fileWrite = open(fileName + '.new', 'w')
	strLog = 'errorf("shanlihou mutex add line:%d\\n", __LINE__);\n';
	strLogEnd = 'errorf("shanlihou mutex add enter line:%d\\n", __LINE__);\n';
	for line in fileRead:
		find = pattern.search(line)
		if (find):
			print(line)
			fileWrite.writelines(strLog)
			fileWrite.writelines(line)
			fileWrite.writelines(strLogEnd)
			continue
		fileWrite.writelines(line)
	
addLogMutex(sys.argv[1])
