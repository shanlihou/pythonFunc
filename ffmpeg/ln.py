#!/usr/bin/python
import sys
import os
def cp():
	argLen = len(sys.argv)
	src = sys.argv[argLen - 2]
	dst = '/usr/lib/' + sys.argv[argLen - 1]
	cmd = 'cp %s %s' % (src, dst)
	print cmd
	os.system(cmd)
if __name__ == '__main__':
	cmdStr = '/bin/ln_ori'
	for i in range(1, len(sys.argv), 1):
		cmdStr += ' ' + sys.argv[i]
	print cmdStr
	curcwd = os.getcwd()
	if curcwd.startswith('/mnt/hgfs/E/github/others/ffmpeg'):
		cp()
	else:
		os.system(cmdStr)

