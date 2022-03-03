#coding:utf-8
import re
import os


G_PATH = r'F:\wxtmp\WXWork\1688851680425036\Cache\File\2022-03\12001_20220303_061851_dblog\maintenceAll.log'
G_ROOT = r'G:\tmp\all_log'

def parseAll():
    for i in os.listdir(G_ROOT):
        dirName = os.path.join(G_ROOT, i)
        if os.path.isdir(dirName):
            newName = os.path.join(dirName, 'maintenceAll.log')
            po = ParseOne(newName)
            print(newName)
            po.test()


class ParseOne(object):
    def __init__(self, filename) -> None:
        self.filename = filename
        self.sendNum = 0
        self.signUpNum = 0
        self.occupy = 0
        self.couldSign = 0
        self.deleteSign = 0

    def checkTime(self, tups):
        val = [int(i) for i in tups]
        if val[0] == 3 and val[1] == 3 and val[2] == 5:
            return True

        return False

    def parse(self):
        timePat = re.compile(r'\[\d+-(\d+)-(\d+) (\d+):\d+:\d+')
        with open(self.filename, encoding='utf-8') as fr:
            for line in fr:
                ret = timePat.search(line)
                if ret:
                    if not self.checkTime(ret.groups()):
                        continue

                    if 'will modify guild' in line:
                        self.sendNum += 1
                    elif 'sign up info' in line:
                        self.signUpNum += 1
                    elif 'cur occupy info line' in line:
                        self.occupy += 1
                    elif 'INSERT INTO tbl_GuildBattleStub_couldJoinGuilds' in line:
                        self.couldSign = line.count('(1, ')
                    elif 'DELETE FROM tbl_GuildBattleStub_guildBattleInfo_signUpSet' in line:
                        self.deleteSign = line.count(',')

    def finalLog(self):
        print(f'send:{self.sendNum}, signUp:{self.signUpNum}, occupy:{self.occupy}, couldSign:{self.couldSign}, deleteSign:{self.deleteSign}')

    def test(self):
        self.parse()
        self.finalLog()


def main():
    # po = ParseOne(G_PATH)
    # po.test()
    parseAll()

if __name__ == '__main__':
    main()