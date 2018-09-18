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
                if files[1] == '+':
                    fileName = ' '.join(files[2:])
                else:
                    fileName = ' '.join(files[1:])

                revertList.append((fileName, line))

            elif files[0] == 'D':
                revertList.append((files[2], line))
            elif files[0] == 'R':
                revertList.append((files[3], line))

        for i, line in revertList:
            svnStr = 'svn revert "%s"' % i
            print('revert:', svnStr)
            print('origin:', line)
            os.system(svnStr)

        os.system('svn up')

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

        rev = Revert('E:\client2')
        rev.test()

        rev = Revert(
            r'E:\svn\Dev\Server\kbeWin\kbengine\assets\scripts\kbengine_unity3d_plugins')
        rev.test()
    elif opt == 1:

        rev = Revert(r'E:\svn\Dev\Client')
        rev.show()
