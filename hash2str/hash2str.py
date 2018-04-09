import sys
import string
def hash2str(fileName):
	fileRead = open(fileName, 'r')
	strTest = 'ClientMac'
	for i in strTest:
		print ord(i) / 16
		print ord(i) % 16
	for line in fileRead:
		hashList = line.split()
		#print hashList
		strHash = ''
		for i in hashList:
			num = string.atoi(i, base=16)
			if (num >= 32 and num <= 126):
				strHash += '  ' + chr(num)
			else:
				strHash += ' ' + i
		print strHash
			

hash2str(sys.argv[1])
