import os
import sys


class Branch2Trunk(object):
    def __init__(self, src, dst):
        print(src, dst)
        self.src = src
        self.dst = dst

    def test(self):
        os.chdir(self.src)
        ret = os.popen('svn st')
        for line in ret:
            # sprint(line)
            ret = line.split()
            if len(ret) != 2:
                continue

            status, path = ret
            if status != 'M' and status != '?' and status != 'A':
                continue

            cpStr = 'copy %s %s' % (path, os.path.join(self.dst, path))
            print(cpStr)
            os.system(cpStr)


if __name__ == '__main__':
    opt = 0
    print(sys.argv)
    if len(sys.argv) == 3:
        test = Branch2Trunk(sys.argv[1], sys.argv[2])
    elif opt == 1:
        print(opt)
        test = Branch2Trunk(
            r'E:\svn\Dev\Server\kbeLinux\kbengine\assets\scripts',
            r'E:\svn\Dev\Server\kbeWin\kbengine\assets\scripts')
    else:
        test = Branch2Trunk(
            r'E:\svn\Dev\Server\kbeWin\kbengine\assets\scripts\kbengine_unity3d_plugins',
            r'E:\svn\Dev\Client\Assets\Scripts\ScriptsKBE\kbengine\kbengine_unity3d_plugins')

    test.test()
