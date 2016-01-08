import sys
import os
def createSmaliLog(fileName):
	fileRead = open(fileName, 'r')
	fileWrite = open(fileName + '.new', 'w')
	for line in fileRead:
		if (".prologue" in line):
			fileWrite.writelines(line)
			fileWrite.writelines("    const-string v0, \"" + fileName + '"\n')
			fileWrite.writelines("    invoke-static {v0}, Lcrack;->log(Ljava/lang/String;)V\n")
		else:
			fileWrite.writelines(line)
	fileRead.close()
	fileWrite.close()
	os.rename(fileName + '.new', fileName)
createSmaliLog(sys.argv[1])
