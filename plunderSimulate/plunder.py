import Avatar
import dropAward
import random
import utils
import config
from DATA import BCKD
from DATA import PSD
from DATA import gameconst
from DATA import BSGD

class PlunderRewardCtx(object):
    def __init__(self, selfLingqiLv, lingStone, hunStone, targetSpaceGateLv, completion, selfSpaceGateLv, targetCangkuLv,
                 targetLingqiLv, selfScore, targetScore, selfCangkuLv):
        self.selfLingqiLv = selfLingqiLv
        self.lingStone = lingStone
        self.hunStone = hunStone
        self.targetSpaceGateLv = targetSpaceGateLv
        self.completion = completion
        self.selfSpaceGateLv = selfSpaceGateLv
        self.targetCangkuLv = targetCangkuLv
        self.targetLingqiLv = targetLingqiLv
        self.selfScore = selfScore
        self.targetScore = targetScore
        self.selfCangkuLv = selfCangkuLv


def _randomValue(origin, rangeStr, minValue):
    rangeValue = int(PSD.datas[rangeStr]['value'])
    return max(random.randint(origin - rangeValue, origin + rangeValue), minValue)


def calcCompletion(Ra, Rb):
    return (1 + random.randint(1, config.K) / 100) / (1 + 10 ** ((Ra - Rb) / 400))


def eloCalc(Ra, Rb, completion):
        eloSa = eval(PSD.datas['eloSa']['value'])
        completion = int(completion * 100)
        for start, end, sa in eloSa:
            if start <= completion <= end:
                Sa = sa
                break

        Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
        Eb = 1 / (1 + 10 ** ((Ra - Rb) / 400))
        K = int(PSD.datas['eloK']['value'])
        Ra2 = max(int(Ra + K * (Sa - Ea)), 0)
        Rb2 = max(int(Rb - K * (Sa - Ea)), 0)
        return Ra2, Rb2


def plunder(aGbId, dGbId):
    aAvatar = Avatar.AvatarPool().getAvatar(aGbId)
    aSpaceGateLv = utils.getWarpGateLevel(aAvatar.score)
    if utils.isAvatar(dGbId):
        dAvatar = Avatar.AvatarPool().getAvatar(dGbId)
        targetScore = dAvatar.score
        completion = calcCompletion(aAvatar.score, dAvatar.score)
        dSpaceGateLv = utils.getWarpGateLevel(dAvatar.score)
        prCtx = PlunderRewardCtx(aAvatar.lqLv, dAvatar.ling, dAvatar.hun, dSpaceGateLv, completion, aSpaceGateLv, dAvatar.ckLv,
                         dAvatar.lqLv, aAvatar.score, dAvatar.score, aAvatar.ckLv)
    else:
        targetScore = _randomValue(aAvatar.score, 'systemWorldScoreRange', 0)
        dSpaceGateLv = utils.getWarpGateLevel(targetScore)

        lingqiMax = gameconst.HomeBuildingType.getMaxLevel(gameconst.HomeBuildingType.LINGQI)
        targetLingqiLv = min(_randomValue(aAvatar.lqLv, 'systemWorldLingqiRange', 1), lingqiMax)

        cangkuMax = gameconst.HomeBuildingType.getMaxLevel(gameconst.HomeBuildingType.CANGKU)
        targetCangkuLv = min(_randomValue(aAvatar.ckLv, 'systemWorldCangkuRange', 1), cangkuMax)

        cangkuData = BCKD.datas[targetCangkuLv]
        lingStoneMax = cangkuData['lingStoneMax']
        lingStone = random.randint(int(lingStoneMax * cangkuData['systemWorldLingStoneMin']),
                                   int(lingStoneMax * cangkuData['systemWorldLingStoneMax']))

        hunStoneMax = cangkuData['hunStoneMax']
        hunStone = random.randint(int(hunStoneMax * cangkuData['systemWorldHunStoneMin']),
                                  int(hunStoneMax * cangkuData['systemWorldHunStoneMax']))

        completion = calcCompletion(aAvatar.score, targetScore)

        prCtx = PlunderRewardCtx(aAvatar.lqLv, lingStone, hunStone, dSpaceGateLv, completion, aSpaceGateLv, targetCangkuLv,
                 targetLingqiLv, aAvatar.score, targetScore, aAvatar.ckLv)

    award = dropAward.getDropAward(aAvatar, int(PSD.datas['plunderRewardID']['value']), 1,
                                   rewardType=gameconst.RewardType.PLUNDER, ctx=prCtx)[0]

    ling = int(award.get(30000006, 0))
    hun = int(award.get(30000007, 0))
    if utils.isAvatar(dGbId):
        dAvatar.stole(ling, hun)

    exRate = BSGD.datas[prCtx.selfSpaceGateLv]['exAddRatio']
    award[30000006] = int(ling * (1 + exRate))
    award[30000007] = int(hun * (1 + exRate))


    exAward = dropAward.getDropAward(aAvatar, int(PSD.datas['attackExRewardID']['value']), 1,
                                     rewardType=gameconst.RewardType.PLUNDER, ctx=prCtx)[0]

    for id, num in exAward.items():
        award[id] = award.get(id, 0) + num

    ling = award.get(30000006, 0)
    hun = award.get(30000007, 0)
    tao = award.get(30000008, 0)
    cao = award.get(30000009, 0)

    aAvatar.award(award)
    aNew, dNew = eloCalc(aAvatar.score, targetScore, completion)
    aAvatar.score = aNew
    if utils.isAvatar(dGbId):
        dAvatar.score = dNew

    attackInfo = {'defenceOwner': dGbId,
                  'completion': completion,
                  'ling': ling,
                  'hun': hun,
                  'tao': tao,
                  'cao': cao}
    aAvatar.addAttackInfo(attackInfo)
