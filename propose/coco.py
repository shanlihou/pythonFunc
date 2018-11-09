# coding=utf-8
import cocos
from cocos.actions import *
from singleton import singleton
import const


def killAfterStop(t, label):
    isActionRunning = label.are_actions_running()
    if not isActionRunning:
        label.kill()


@singleton
class Coco(cocos.layer.Layer):
    def __init__(self):
        super(Coco, self).__init__()

    def addLabel(self, data, actType, args):
        label = cocos.text.Label(
            data,
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center')

        label.position = 320, 240
        self.add(label)
        label.schedule_interval(killAfterStop, 0.5, label)
        # label.do(Repeat(scale + Reverse(scale)))
        if actType == const.ActType.move:
            act = MoveBy((-50, 0), duration=2)
        elif actType == const.ActType.scale:
            scale = ScaleBy(3, duration=2)
            act = scale + Reverse(scale)

        label.do(act)

    def update(self, *args):
        # print(' im in update:', args)
        pass


def start():
    cocos.director.director.init()
    main_layer = Coco()
    action = Accelerate(RotateBy(360, duration=10))
    main_layer.do(action)
    main_scene = cocos.scene.Scene(main_layer)
    cocos.director.director.run(main_scene)


if __name__ == '__main__':
    start()
