import os
import os


class Revert(object):
    def __init__(self, path):
        self.path = path

    def test(self):
        os.chdir(self.path)
        ret = os.popen('svn st')
        revertList = []
        for line in ret:
            files = line.split()
            if len(files) < 2:
                continue

            if files[0] == 'M' or files[0] == '!' or files[0] == 'C':
                if files[1] == '+' or files[1] == 'C' or files[1] == 'L':
                    fileName = ' '.join(files[2:])
                else:
                    fileName = ' '.join(files[1:])

                revertList.append((fileName, line))

            elif files[0] == 'D':
                revertList.append((files[2], line))
            elif files[0] == 'R':
                revertList.append((files[3], line))
            elif len(files) > 3 and ''.join(files[0:3]) == 'A+C':
                revertList.append((files[3], line))

        for i, line in revertList:
            svnStr = 'svn revert --depth infinity "%s"' % i
            if 'fmod' in line:
                continue

            print('revert:', svnStr)
            print('origin:', line)
            os.system(svnStr)

        os.system('svn up')

    def update(self):
        os.chdir(self.path)
        os.system('svn up')

    def cpWin2Linux(self, winPath, linuxPath):
        os.chdir(winPath)
        ret = os.popen('svn st')
        for line in ret:
            files = line.split()
            if not files:
                continue

            if files[0] == 'M':
                dstPath = os.path.join(linuxPath, files[1])
                cpStr = 'copy %s %s' % (files[1], dstPath)
                print(cpStr)
                os.system(cpStr)

    def show(self):
        os.chdir(self.path)
        ret = os.popen('svn st')
        revertList = []
        for line in ret:
            files = line.split()
            print(files)


if __name__ == '__main__':
    opt = 0
    if opt == 0:
        rev = Revert('E:\svn\Dev\Client')
        rev.test()

#         rev = Revert(r'C:\Users\Administrator\AppData\Local\clientC')
#         rev.test()
        rev = Revert(r'F:\Client2')
        rev.test()

        rev = Revert(
            r'E:\svn\Dev\Server\kbeWin\kbengine\assets\scripts\kbengine_unity3d_plugins')
        rev.test()

        rev = Revert(
            r'E:\server\scripts\kbengine_unity3d_plugins')
        rev.test()
        
        rev = Revert(r'E:\svn\Dev\Server\kbeLinux\kbengine\assets\scripts\kbengine_unity3d_plugins')
        rev.test()

        os.system('svn up E:\svn\Dev\Server')

        os.system(r'svn up E:\assets2')
    elif opt == 1:
        rev = Revert(r'E:\svn\Dev\Client')
        rev.cpWin2Linux(r'E:\svn\Dev\Server\kbeWin\kbengine\assets\scripts',
                        r'E:\svn\Dev\Server\kbeLinux\kbengine\assets\scripts')
