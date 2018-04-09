import sys

def cmpSvn(file1, filePrep):
	dictSvn = {}
	file1Read = open(file1, 'r')
	filePrepRead = open(filePrep, 'r')
	for line in filePrepRead:
		tmp = line.split(' ')
		dictSvn[tmp[1].replace('\n', '')] = tmp[0]
	for line in file1Read:
		tmp = line.split(' ')
		if dictSvn.has_key(tmp[0]):
			tmp1 = tmp[1].replace('\n', '')
			if tmp1 != dictSvn[tmp[0]]:
				print tmp[0]
				print tmp1
				print dictSvn[tmp[0]]
		else:
			print 'not has:' + tmp[0]

cmpSvn(sys.argv[1], sys.argv[2])
	
