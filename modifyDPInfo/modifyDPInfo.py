import re
import sys
import string
def modifyDPInfo(compPath, DPPath):
	dictDP = {}
	dictUrl = {}
	dictHash = {}
	patName = re.compile(r'name\s*=\s*"([^"]+)"')
	patVer = re.compile(r'(revision\s*=\s*")([^"]+)"')
	patUrl = re.compile(r'url\s*=\s*"([^"]+)"')
	fileComp = open(compPath, 'r')
	fileDPOri = open(DPPath, 'r')
	fileDPDst = open(DPPath + '.new', 'w')
	fileOut = open('file.out', 'w')
	for line in fileComp:
		nameFind = patName.search(line)
		if nameFind:
			verFind = patVer.search(line)
			urlFind = patUrl.search(line)
			if verFind:
				dictDP[urlFind.group(1)] = verFind.group(2)
				dictUrl[urlFind.group(1)] = nameFind.group(1)
				dictHash[urlFind.group(1)] = 1
	for line in fileDPOri:
		urlFind = patUrl.search(line)
		if urlFind:
			url = urlFind.group(1)
			nameFind = patName.search(line)
			name = nameFind.group(1)
			verFind = patVer.search(line)
			ver = verFind.group(2)
			if dictDP.has_key(url) and dictDP[url] != ver:
				out = dictUrl[url] + ':' + dictDP[url] + '\t' + name + ':' + ver + '\n'
				fileOut.writelines(out)
				ver1 = string.atoi(dictDP[url])
				ver2 = string.atoi(ver)
				if ver1 > ver2:
					fileDPDst.writelines(patVer.sub(verFind.group(1) + str(ver1) + '"', line))
				else:
					fileDPDst.writelines(patVer.sub(verFind.group(1) + str(ver2) + '"', line))
					
				continue
		fileDPDst.writelines(line)
				


modifyDPInfo(sys.argv[1], sys.argv[2])
