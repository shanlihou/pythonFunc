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
from cocos import skeleton


def killAfterStop(t, label, func):
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



def getAnim(dirName):
    boneName = os.path.join(dirName, 'human_bone.py')
    skinName = os.path.join(dirName, 'human_skin.py')
    animName = os.path.join(dirName, 'sample.anim')
    sk = imp.load_source('skeleton', boneName).skeleton
    skin = imp.load_source('skin', skinName).skin
    anim = pickle.load(open(animName, 'rb'))
    skin = skeleton.BitmapSkin(sk, skin)
    return skin, anim


class Coco(cocos.layer.Layer):
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

    def getSpeed(self, dir):
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
        self.addLabel(task['data'], task['act'], task)


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
