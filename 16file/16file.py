#!/usr/bin/python
import sys
def file16(fileName):
	fileRead = open(fileName, 'r')
	fileList = []
	index = 0
	for i in range(16):
		fileWrite = open(str(i) + '.txt', 'w')
		fileList.append(fileWrite)
	fileStr = fileRead.read()
	for i in fileStr:
		fileList[index].write(i)
		index = (index + 1) % 16
file16(sys.argv[1])
		
