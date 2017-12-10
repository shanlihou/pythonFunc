import sys
def formatJS(fileIn):
	fileRead = open(fileIn, 'r')
	fileWrite = open(fileIn + '.new', 'w')
	strRead = fileRead.read()
	indent = 0
	for i in strRead:
		if (i == '{'):
			fileWrite.write('\n')
			fileWrite.write(indent * '\t' + '{\n')
			indent = indent + 1
			fileWrite.write(indent * '\t')
		elif (i == '}'):
			fileWrite.write('\n')
			indent = indent - 1
			fileWrite.write(indent * '\t' + '}\n')
			fileWrite.write(indent * '\t')
		elif (i == ';' or i == ','):
			fileWrite.write(i + '\n')
			fileWrite.write(indent * '\t')
		else:
			fileWrite.write(i)
			
formatJS(sys.argv[1])
