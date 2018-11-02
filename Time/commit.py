import os


class Commit(object):
    def __init__(self, path):
        self.path = path

    def push(self):
        os.system('git add -A')
        os.system("git commit -m 'auto'")
        os.system("git push origin master")

    def test(self):
        os.chdir(self.path)
        gitStr = 'git status'
        ret = os.popen(gitStr)
        isNeed = False
        for line in ret:
            print(line)
            if 'modified' in line or 'Untracked' in line:
                isNeed = True

        print(isNeed)
        if isNeed:
            self.push()


if __name__ == '__main__':
    commit = Commit(r'E:\shgithub\python\pythonFunc')
    commit.test()
