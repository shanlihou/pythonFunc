import sys
def calcTab(num):
	ret = ''
	for i in range(num):
		ret = ret + '\t'
	return ret
def addEnter(strNeedAdd):
	tab = 0
	retStr = ''
	for i in strNeedAdd:
		if (i == ';'):
			retStr = retStr + ';\n' + calcTab(tab)
		elif (i == '{'):
			tab = tab
			retStr = retStr + '\n' + calcTab(tab)
			tab = tab + 1
			retStr = retStr + '{\n' + calcTab(tab)
		elif (i == '}'):
			tab = tab - 1
			retStr = retStr + '\n' + calcTab(tab) + '}\n' + calcTab(tab)
		else:
			retStr = retStr + i
	print(retStr)
def readFile(path):
	fileRead = open(path, 'r')
	for line in fileRead:
		addEnter(line)
readFile(sys.argv[1])
