import re
import sys
import os
def addr2line(fileName, sonia = None):
	pattern = re.compile(r'\[([\w-]+)\]')
	if not sonia:
		sonia = 'Images/user/bin/sonia'
	fileRead = open(fileName, 'r')
	for line in fileRead:
		print line
		listFind = pattern.findall(line)
		for i in listFind:
			print i
			data = i.split('-')
			for j in data:
				print j
				print 'arm-hisiv500-linux-uclibcgnueabi- -e ' + sonia + ' -a ' + j
				#os.system('arm-linux-gnueabihf-4.9.1-addr2line -e ' + sonia + ' -a ' + j)
				os.system('arm-hisiv500-linux-uclibcgnueabi-addr2line -e ' + sonia + ' -a ' + j)
if len(sys.argv) == 2:
	addr2line(sys.argv[1])
elif len(sys.argv) == 3:
	addr2line(sys.argv[1], sys.argv[2])
