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

            if files[0] == 'M' or files[0] == '!':
                revertList.append(files[1])

        for i in revertList:
            svnStr = 'svn revert %s' % i
            os.system(svnStr)

        os.system('svn up')


if __name__ == '__main__':
    rev = Revert('E:\svn\Dev\Client')
    rev.test()

    rev = Revert('E:\client2')
    rev.test()

    rev = Revert(
        r'E:\svn\Dev\Server\kbeWin\kbengine\assets\scripts\kbengine_unity3d_plugins')
    rev.test()
