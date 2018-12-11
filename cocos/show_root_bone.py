import cocos
from cocos import skeleton

# import the skeleton we have created
import human_bone


class TestLayer(cocos.layer.Layer):
    def __init__(self):
        super(TestLayer, self).__init__()

        x, y = cocos.director.director.get_window_size()

        # create a ColorSkin for our skeleton
        self.skin = skeleton.ColorSkin(human_bone.skeleton, (255, 0, 0, 255))

        # add the skin to the scene
        self.add(self.skin)
        x, y = cocos.director.director.get_window_size()
        self.skin.position = x / 2, y / 2


if __name__ == '__main__':
    cocos.director.director.init(width=800, height=100, caption="cici")
    main_layer = TestLayer()
    main_scene = cocos.scene.Scene(main_layer)
    cocos.director.director.run(main_scene)
