import cocos
from cocos.actions import *
from django.utils import duration


class HelloWorld(cocos.layer.Layer):
    def __init__(self):
        super(HelloWorld, self).__init__()
        label = cocos.text.Label(
            'Hello, world',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center')

        label.position = 320, 240
        self.add(label)

        sprite = cocos.sprite.Sprite(r'1.jpg')
        sprite.position = 320, 240
        sprite.scale = 3
        self.add(sprite, z=1)

        scale = ScaleBy(3, duration=2)
        label.do(Repeat(scale + Reverse(scale)))
        moveBy = MoveBy((50, 100), duration=2)
        wave = Waves3D(duration=2)
        lens = Lens3D(duration=2)
        twril = Twirl( grid=(16,12), duration=4)
        sprite.do(Repeat(Reverse(scale) + scale + twril))


if __name__ == '__main__':

    cocos.director.director.init()
    hello_layer = HelloWorld()
    action = Accelerate(RotateBy(360, duration=10))
    hello_layer.do(action)
    main_scene = cocos.scene.Scene(hello_layer)
    cocos.director.director.run(main_scene)
