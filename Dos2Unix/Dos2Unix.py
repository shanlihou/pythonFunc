import sys
def dos2unix(fileName):
	print(fileName)
	fileRead = open(fileName, 'rb')
	fileWrite = open(fileName + '.new', 'wb')
	count = 0
	for i in fileRead.read():
		if (ord(i) == 13):
			count = count + 1
			continue
		fileWrite.write(i)
	print(count)
dos2unix(sys.argv[1])
