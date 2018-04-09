import sys
def modify(path1, path):
	fileRead1 = open(path1, 'rb')
	fileRead = open(path, 'rb')
	fileWrite = open('sonia', 'wb')
	elf = fileRead1.read(64)
	fileWrite.writelines(elf)
	for line in fileRead:
		for i in line:
			fileWrite.writelines(i)
modify(sys.argv[1], sys.argv[2])


