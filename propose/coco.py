# coding=utf-8
import cocos
import threading
from cocos.actions import *
from center import center
import functools
import const
import os
import imp
import pickle
import time
import math
import random
from cocos import skeleton


def killAfterStop(t, label, func):
    print(t)
    isActionRunning = label.are_actions_running()
    if not isActionRunning:
        label.kill()
        func()


class State(object):
    idle = 0
    act = 1


def isIdle(func):
    @functools.wraps(func)
    def _(self, *args, **kwargs):
        if self.state != State.idle:
            return

        return func(self, *args, **kwargs)

    return _


class TaskType(object):
    label = 0
    anim = 1
    zoo = 2


class AnimMixin(object):
    animDict = {
        'baobao_recv':
        {
            'anim': [0, 0, 5],
            'sprite': [1, 3, 0.4, 'message.png']
        },
        'me_send':
        {
            'anim': [0, 0, 5],
            'sprite': [1, 3, 0.4, 'message.png']
        }
    }

    @staticmethod
    def getAnim(dirName):
        dirName = os.path.join('anim', dirName)
        boneName = os.path.join(dirName, 'human_bone.py')
        skinName = os.path.join(dirName, 'human_skin.py')
        animName = os.path.join(dirName, 'sample.anim')
        sk = imp.load_source('skeleton', boneName).skeleton
        skin = imp.load_source('skin', skinName).skin
        anim = pickle.load(open(animName, 'rb'))
        skin = skeleton.BitmapSkin(sk, skin)
        return skin, anim

    def getMidXY(self):
        x, y = cocos.director.director.get_window_size()
        return x // 2, y // 2

    def getAnimData(self, name):
        return self.animDict[name]['anim']

    def getSpriteData(self, name):
        return self.animDict[name]['sprite']

    @isIdle
    def addAnimTask(self, task):
        name = task['name']
        x, y, delay = self.getAnimData(name)
        if not x and not y:
            x, y = self.getMidXY()
        self.addAnim(x, y, delay, name)

        dire, delay, scale, spName = self.getSpriteData(name)
        spSpeed = self.getSpeed(dire, x, y)
        if name == 'baobao_recv':
            x = 0

        self.addSprite(x, y, spSpeed, delay, scale, spName)

    def addAnim(self, x, y, delay, name):
        skin, anim = self.getAnim(name)
        self.add(skin)
        skin.position = x, y
        skin.do(cocos.actions.Repeat(skeleton.Animate(anim)))
        finalTime = time.time() + delay
        skin.schedule_interval(self.killFunc, 0.1, skin, finalTime)

    def addSprite(self, x, y, speed, duration, scale, pngname):
        sprite = cocos.sprite.Sprite(pngname)
        sprite.position = x, y
        sprite.scale = scale
        self.add(sprite)
        act = MoveBy(speed, duration=duration)
        sprite.do(act + CallFunc(sprite.kill))

    @isIdle
    def addZoo(self, task):
        delay = task['duration']
        midX, midY = self.getMidXY()
        r = midY // 2
        theta = 0
        finalTime = time.time() + delay
        batch = cocos.batch.BatchNode()
        for aName in os.listdir('animal'):
            piT = theta * math.pi / 180
            x = midX + r * math.cos(piT)
            y = midY + r * math.sin(piT)
            sprite = cocos.sprite.Sprite('animal/' + aName)
            sprite.scale = 0.5
            sprite.position = x, y
            act = MoveBy((0, r * 0.5), duration=0.5 + random.random() * 0.5)
            act = act + Reverse(act)
            sprite.do(Repeat(act))
            batch.add(sprite)

            theta += 360 / 7
        batch.schedule_interval(self.killFunc, 0.1, batch, finalTime)
        self.add(batch)
        
    @isIdle    
    def addThrow(self):
        skin, anim = self.getAnim('me_throw')
        self.add(skin)
        x, y = self.getMidXY()
        skin.position = x, y
        skin.do(cocos.actions.Repeat(skeleton.Animate(anim)))
        finalTime = time.time() + delay
        skin.schedule_interval(self.killFunc, 0.1, skin, finalTime)
        
        

    def killFunc(self, t, skin, final):
        if time.time() > final:
            skin.kill()


class Coco(cocos.layer.Layer, AnimMixin):
    def __init__(self):
        print('coco init')
        super(Coco, self).__init__()
        self.taskList = []
        self.resetState()
        self.schedule(self.update)

    def getPos(self, dir):
        x, y = cocos.director.director.get_window_size()
        if dir == 0:
            return x // 2, y
        elif dir == 1:
            return 0, y // 2
        elif dir == 2:
            return x // 2, 0
        elif dir == 3:
            return x, y // 2

    def getSpeed(self, dir, x=0, y=0):
        if not x and not y:
            x, y = cocos.director.director.get_window_size()
        if dir == 0:
            return 0, -y
        elif dir == 1:
            return x, 0
        elif dir == 2:
            return 0, y
        elif dir == 3:
            return -x, 0

    @isIdle
    def addLabel(self, data, actType, args):
        label = cocos.text.Label(
            data,
            font_name='Times New Roman',
            font_size=1,
            anchor_x='center', anchor_y='center')

        self.add(label)
        label.schedule_interval(killAfterStop, 0.1, label, self.resetState)
        # label.do(Repeat(scale + Reverse(scale)))
        duration = args.get('duration', 2)
        if actType == const.ActType.move:
            dir = args.get('dir', 0)
            label.position = self.getPos(dir)
            act = MoveBy(self.getSpeed(dir), duration=duration)
        elif actType == const.ActType.scale:
            scale = ScaleBy(3, duration=duration)
            act = scale + Reverse(scale)

        self.state = State.act
        label.do(act)

    def resetState(self):
        self.state = State.idle

    def update(self, *args):
        if self.state == State.idle and self.taskList:
            self.doTask()

    def addTask(self, task):
        print('add task:', task)
        self.taskList.append(task)

    @isIdle
    def doTask(self):
        if not self.taskList:
            return

        task = self.taskList[0]
        del self.taskList[0]
        tType = task.get('type', 0)
        if tType == TaskType.label:
            self.addLabel(task['data'], task['act'], task)
        elif tType == TaskType.anim:
            self.addAnimTask(task)
        elif tType == TaskType.zoo:
            self.addZoo(task)


def start(*args):
    cocos.director.director.init(width=800, height=600, caption="cici")
    main_layer = Coco()
    center.register('coco', main_layer)
    main_scene = cocos.scene.Scene(main_layer)
    cocos.director.director.run(main_scene)


def threadCoco():
    t = threading.Thread(target=start, args=())
    t.start()


if __name__ == '__main__':
    start()
