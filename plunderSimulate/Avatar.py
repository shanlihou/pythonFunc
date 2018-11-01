import random
from RobStub import RobStub
from DATA import PSD
from DATA import BCKD
from DATA import BED
from singleton import singleton

import plunder
import config
import copy


class Avatar(object):
    def __init__(self, name, ownerGbId):
        self.score = 2000
        self.lqLv = random.randint(*config.lingqiLevel)
        self.ckLv = self.lqLv
        self.name = name
        self.ownerGbId = ownerGbId
        self.warpGates = []
        self.ling = config.A1 * self.getLingMax()
        self.hun = config.A2 * self.getHunMax()
        self.dailyLing = 0
        self.dailyHun = 0
        self.exData = {}
        self.attackTimes = 0
        self.beingAttackTimes = 0

    def modifyLing(self, value):
        if value > 0:
            self.ling = min(self.getLingMax(), self.ling + value)
        else:
            self.ling = max(0, self.ling + value)

    def modifyHun(self, value):
        if value > 0:
            self.hun = min(self.getHunMax(), self.hun + value)
        else:
            self.hun = max(0, self.hun + value)

    def getDailyProduce(self):
        jiuguanData = BED.datas.get(self.ckLv)
        if not jiuguanData:
            return 0, 0

        predictproduct = jiuguanData['predictproduct']
        return predictproduct, predictproduct

    def daily(self):
        self.warpGates = []
        self.dailyLing = 0
        self.dailyHun = 0
        preLing, preHun = self.getDailyProduce()
        ling = config.A1 * self.ling + config.A2 * preLing
        hun = config.A1 * self.hun + config.A2 * preHun
        self.modifyLing(ling)
        self.modifyHun(hun)


    def stole(self, ling, hun):
        limitLing, limitHun = self.getDailyProduce()
        limitRate = float(PSD.datas['plunderLimit']['value'])
        limitLing = int(limitLing * limitRate)
        limitHun = int(limitHun * limitRate)
        ling = min(min(ling, limitLing - self.dailyLing), self.ling)
        hun = min(min(hun, limitHun - self.dailyHun), self.hun)
        if ling > 0:
            self.modifyLing(-ling)
            self.dailyLing += ling

        if hun > 0:
            self.modifyHun(-hun)
            self.dailyHun += hun

        self.beingAttackTimes +=1

    def award(self, data):
        self.modifyLing(data.pop(30000006))
        self.modifyHun(data.pop(30000007))
        for id, num in data.items():
            self.exData[id] = self.exData.get(id, 0) + num

    def getLingMax(self):
        return BCKD.datas[self.ckLv]['lingStoneMax']

    def getHunMax(self):
        return BCKD.datas[self.ckLv]['lingStoneMax']

    def addToStub(self):
        RobStub().addRobInfo(self.ownerGbId, self.lqLv, self.score, self.name)

    def match(self):
        randNum = random.randint(int(PSD.datas['minPosNum']['value']), int(PSD.datas['maxPosNum']['value']))
        RobStub().getMatchList(self, self.ownerGbId, copy.copy(self.warpGates), self.lqLv, 0, self.score, randNum)

    def onGetMatchList(self, matchList, robScore, lingqiLevel, cangkuLv):
        for gbId, name, lingqiLevel in matchList:
            self.warpGates.append(gbId)

    def attack(self):
        index = random.randint(0, len(self.warpGates) - 1)
        plunder.plunder(self.ownerGbId, self.warpGates[index])
        del self.warpGates[index]
        self.attackTimes += 1


@singleton
class AvatarPool(object):
    def __init__(self):
        self.avatars = []

    def initAvatars(self, num):
        self.num = num
        self.avatars = [Avatar(str(i), i) for i in range(100000, 100100)]
        [avatar.addToStub() for avatar in self.avatars]

    def allMatch(self):
        for avatar in self.avatars:
            for i in range(config.random_times):
                avatar.match()

    def allDaily(self):
        for avatar in self.avatars:
            avatar.daily()

    def test(self):
        avatar = self.avatars[0]
        avatar.match()
        print(avatar.score)
        avatar.attack()
        print(avatar.score)

    def getAvatar(self, gbId):
        return self.avatars[gbId - 100000]

    def allAttack(self):
        for avatar in self.avatars:
            for i in range(config.attack_times):
                avatar.attack()

    def go(self, days):
        for i in range(days):
            self.allDaily()
            self.allMatch()
            self.allAttack()

        self.out()

    def out(self):
        with open(config.output_file, 'w') as fw:
            for avatar in self.avatars:
                strPrint = 'name:{}\n'.format(avatar.name)
                strPrint += 'score:{}\n'.format(avatar.score)
                strPrint += 'lingqiLevel:{}\n'.format(avatar.lqLv)
                strPrint += 'lingStone:{}\n'.format(avatar.ling)
                strPrint += 'hunStone:{}\n'.format(avatar.hun)
                strPrint += 'xiantao:{}\n'.format(avatar.exData.get(30000008, 0))
                strPrint += 'xiancao:{}\n'.format(avatar.exData.get(30000009, 0))
                strPrint += 'attackTimes:{}\n'.format(avatar.attackTimes)
                strPrint += 'beingAttack:{}\n'.format(avatar.beingAttackTimes)

                strPrint += '\n' + '-' * 30 + '\n'
                fw.write(strPrint)




if __name__ == '__main__':
    AvatarPool().initAvatars(config.avatar_num)
    AvatarPool().test()

