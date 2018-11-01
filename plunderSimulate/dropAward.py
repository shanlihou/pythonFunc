from DATA import MPPD
import random
from DATA import RDDT
# from DATA import IDIDD
import math

def addItemInfo(srcItemDic, dstItemDic):
    for itemId, num in srcItemDic.items():
        dstItemDic[itemId] = dstItemDic.get(itemId, 0) + num
    return dstItemDic


def checkDailyAwardNum(entity, dropId, num):
    gainNum = entity.dailyAwardDic.get(dropId, 0)
    dailyLimit = RDDT.datas[dropId].get('dailyLimit')
    if dailyLimit != -1 and gainNum + num > dailyLimit:
        # print('checkDailyAwardNum warning-------------------', dropId, num, dailyLimit, gainNum)
        num = dailyLimit - gainNum
    return num


def getDropAward(entity, dropId, num, level=1, rewardType=1, ctx=None):

    if num <= 0:
        return {}, 0, 0, 0, 0, 0

    allAwardDic = {}
    awardEquipDic = {}

    exp = 0
    bindingCoin = 0
    coin = 0
    bindingMoney = 0
    money = 0
    rewardData = RDDT.datas.get(dropId, {})
    expCfg = rewardData.get('exp')
    bindingCoinCfg = rewardData.get('bindingCoin')
    coinCfg = rewardData.get('coin')
    bindingMoneyCfg = rewardData.get('bindingMoney')
    moneyCfg = rewardData.get('money')
    fixReward = rewardData.get('fixReward')
    nestFixReward = rewardData.get('nestFixReward')
    exReward = rewardData.get('exReward')
    nestExReward = rewardData.get('nestExReward')

    for i in range(num):
        if expCfg:
            if callable(expCfg):
                expEx = MPPD.datas[level].get('killExp')
                exp += expCfg(expEx, level)
            else:
                exp += expCfg

        if bindingCoinCfg:
            if callable(bindingCoinCfg):
                bindingCoin += bindingCoinCfg(level)
            else:
                bindingCoin += bindingCoinCfg

        if coinCfg:
            if callable(coinCfg):
                coin += coinCfg(level)
            else:
                coin += coinCfg

        if bindingMoneyCfg:
            if callable(bindingMoneyCfg):
                bindingMoney += bindingMoneyCfg(level)
            else:
                bindingMoney += bindingMoneyCfg

        if moneyCfg:
            if callable(moneyCfg):
                money += moneyCfg(level)
            else:
                money += moneyCfg

        if fixReward:
            for rewardInfo in fixReward:
                itemId, itemNum = rewardInfo
                # print('fixReward', itemId, itemNum)
                if callable(itemNum):
                    itemNum = itemNum(ctx)
                allAwardDic[itemId] = allAwardDic.get(itemId, 0) + itemNum

        if nestFixReward:
            for rewardInfo in nestFixReward:
                dropId, num = rewardInfo
                # print('nestFixReward', dropId, num)
                if callable(num):
                    num = num(level)
                nestAwardDic, nestEquipAwardDic, nestExp, nestBindingCoin, nestCoin, nestBindingMoney, nestMoney = getDropAward(entity,
                                                                                                             dropId,
                                                                                                             num, level,
                                                                                                             rewardType,
                                                                                                             ctx)
                addItemInfo(nestAwardDic, allAwardDic)
                for equipItemId, equipList in nestEquipAwardDic.items():
                    awardEquipDic.setdefault(equipItemId, []).extend(equipList)
                exp += nestExp
                bindingCoin += nestBindingCoin
                coin += nestCoin
                bindingMoney += nestBindingMoney
                money += nestMoney
        if exReward:
            for rewardInfo in exReward:
                itemId, num, prob = rewardInfo
                # print('exReward', itemId, num, prob)
                if callable(num):
                    num = num(level)
                if callable(prob):
                    prob = prob(level)
                for j in range(num):
                    if random.randint(1, prob) == 1:
                        allAwardDic[itemId] = allAwardDic.get(itemId, 0) + 1

        if nestExReward:
            for rewardInfo in nestExReward:
                dropId, num, prob = rewardInfo
                # print('nestExReward', dropId, num, prob)
                if callable(num):
                    num = num(level)
                if callable(prob):
                    prob = prob(level)
                for k in range(num):
                    if random.randint(1, prob) == 1:
                        nestExRewardDic, nestEquipAwardDic, nestExp, nestBindingCoin, nestCoin, nestBindingMoney, nestMoney = getDropAward(
                            entity, dropId, 1, level, rewardType, ctx)
                        addItemInfo(nestExRewardDic, allAwardDic)
                        for equipItemId, equipList in nestEquipAwardDic.items():
                            awardEquipDic.setdefault(equipItemId, []).extend(equipList)
                        exp += nestExp
                        bindingCoin += nestBindingCoin
                        coin += nestCoin
                        bindingMoney += nestBindingMoney
                        money += nestMoney

    #对于装备，需要在这里生成对象
    return allAwardDic, awardEquipDic, int(exp), int(bindingCoin), int(coin), int(bindingMoney), int(money)


def getStackSize(itemId):
    return 0


def getRewardOccupy(rewardId, amount, level):
    itemDict = {}
    _getRewardOccupy(rewardId, amount, level, itemDict)
    occupy = 0
    for itemId, num in itemDict.items():
        stackSize = getStackSize(itemId)
        occupy += math.ceil(num / stackSize)

    return occupy


def _getRewardOccupy(rewardId, amount, level, itemDict):
    if rewardId not in RDDT.datas:
        return 0

    rewardData = RDDT.datas[rewardId]
    rewardList = ['fixReward', 'exReward']
    nestRewardList = ['nestFixReward', 'nestExReward']
    for rewardStr in rewardList:
        reward = rewardData[rewardStr]
        if not reward:
            continue

        for itemInfo in reward:
            itemId = itemInfo[0]
            num = itemInfo[1]
            if callable(num):
                num = num(level)

            itemDict[itemId] = itemDict.get(itemId, 0) + num * amount

    for nestRewardStr in nestRewardList:
        nestReward = rewardData[nestRewardStr]
        if not nestReward:
            continue

        for nestInfo in nestReward:
            tmpRewardId = nestInfo[0]
            num = nestInfo[1]
            if callable(num):
                num = num(level)

            _getRewardOccupy(tmpRewardId, num, level, itemDict)
