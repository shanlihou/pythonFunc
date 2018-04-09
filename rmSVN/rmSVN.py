import sys
import os
def rmSVN(path):
	print path + '/.svn'
	os.system('rm ' + path + '/.svn -rf')
	for i in os.listdir(path):
		newPath = path + '/' + i
		if (os.path.isdir(newPath)):
			rmSVN(newPath)
rmSVN(sys.argv[1])
