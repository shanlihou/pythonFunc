# coding=utf-8
import cocos
from cocos.actions import *


class Coco(object):
    pass


class MyAction(IntervalAction):
    def __init__(self, duration):
        self.duration = duration

    def update(self, t):
        self.target.opacity = 255 * (1-t)

def spriteUpdate(*args):
    print(args)

class HelloWorld(cocos.layer.Layer):
    def __init__(self):
        super(HelloWorld, self).__init__()
        label = cocos.text.Label(
            '一二三',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center')

        label.position = 320, 240
        self.add(label)

        scale = ScaleBy(3, duration=2)
        label.schedule_interval(spriteUpdate, 0.5, label)
        # label.do(Repeat(scale + Reverse(scale)))
        label.do(scale + Reverse(scale))
        self.schedule(self.update)

    def update(self, *args):
        # print(' im in update:', args)
        pass


if __name__ == '__main__':
    cocos.director.director.init()
    hello_layer = HelloWorld()
    action = Accelerate(RotateBy(360, duration=10))
    hello_layer.do(action)
    main_scene = cocos.scene.Scene(hello_layer)
    cocos.director.director.run(main_scene)
