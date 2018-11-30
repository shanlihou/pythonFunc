from __future__ import division, print_function, unicode_literals

from cocos.skeleton import Bone, Skeleton


def Point2(*args): return args


root_bone = Bone('body', 70, -180.0, Point2(0.00, 0.00)).add(
    Bone('upper_arm', 30, 119.99999999999999, Point2(76.00, -55.00)).add(
        Bone('lower_arm', 30, 29.730231531870775, Point2(25.00, -36.00))
    )
)


skeleton = Skeleton(root_bone)
