import cocos
from cocos.director import director
from cocos import skeleton
#from me_send.getAnim import getAnim
import pickle
import imp
import os

def getAnim(dirName):
    boneName = os.path.join(dirName, 'human_bone.py')
    skinName = os.path.join(dirName, 'human_skin.py')
    animName = os.path.join(dirName, 'sample.anim')
    sk = imp.load_source('skeleton', boneName).skeleton
    skin = imp.load_source('skin', skinName).skin
    anim = pickle.load(open(animName, 'rb'))
    skin = skeleton.BitmapSkin(sk, skin)
    return skin, anim


class TestLayer(cocos.layer.Layer):
    def __init__(self):
        super(TestLayer, self).__init__()
        skin, anim = getAnim('me_send')
        x, y = director.get_window_size()
        self.skin = skin
        self.add(self.skin)
        x, y = director.get_window_size()
        self.skin.position = x / 2, y / 2
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
