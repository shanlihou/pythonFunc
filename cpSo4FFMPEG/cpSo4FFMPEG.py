import os
import re 
class CPSO4FF:
    def getSOList(self):
        pattern = re.compile('(\S+)\s=>\snot found')
        out = os.popen('ldd ffmpeg')
        for line in out:
            find = pattern.search(line)
            if not find:
                continue
            
            soName = find.groups()[0]
            findStr = 'find . -name "' + soName + '"'
            print findStr
            findOut = os.popen(findStr)
            soPath = findOut.readlines()[0].replace('\n', '')
            print soPath
            mvStr = 'cp ' + soPath + ' ~/ffmpeg/'
            os.system(mvStr)
if __name__ == '__main__':
    test = CPSO4FF()
    test.getSOList()