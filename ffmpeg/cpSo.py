import os
import re
class cpSo:
	def __init__(self):
		cmd = os.popen('ldd ffmpeg')
		pat = re.compile(r'(\S+)\s*=>\s*not found')
		self.sos = []
		for line in cmd:
			find = pat.search(line)
			if not find:
				continue
			print find.group(1)
			self.sos.append(find.group(1))
	def getPath(self, name):
		cmd = os.popen('find . -name "%s"' % name)
		return cmd.read()

	def cp(self):
		for i in self.sos:
			src = self.getPath(i).replace('\n', '')
			cmdStr = 'cp %s %s' % (src, '/usr/lib/' + i)
			print cmdStr
			os.system(cmdStr)
if __name__ == '__main__':
	cp = cpSo()
	cp.cp()

	
