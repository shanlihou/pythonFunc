import cocos
from cocos.director import director
from cocos import skeleton
import human_bone
import human_skin
import pickle


class TestLayer(cocos.layer.Layer):
    def __init__(self):
        super(TestLayer, self).__init__()

        x, y = director.get_window_size()
        self.skin = skeleton.BitmapSkin(
            human_bone.skeleton, human_skin.skin)
        self.add(self.skin)
        x, y = director.get_window_size()
        self.skin.position = x / 2, y / 2
        anim = pickle.load(open("sample.anim", 'rb'))
        self.skin.do(cocos.actions.Repeat(skeleton.Animate(anim)))


def main():
    director.init()
    test_layer = TestLayer()
    bg_layer = cocos.layer.ColorLayer(255, 255, 255, 255)
    main_scene = cocos.scene.Scene()
    main_scene.add(bg_layer, z=-10)
    main_scene.add(test_layer, z=10)
    director.run(main_scene)


if __name__ == '__main__':
    main()
