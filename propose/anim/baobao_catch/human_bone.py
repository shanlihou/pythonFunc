from cocos.skeleton import Bone, Skeleton

def Point2(*args): return args

root_bone = Bone('body', 70, -183.9360034140333, Point2(-10.00, -43.00)).add(
    Bone('upper_arm1', 30, 667.2359312032213, Point2(-31.00, -116.00))    .add(
        Bone('lower_arm1', 30, 55.16242123536883, Point2(-2.00, -53.00))
)
).add(
    Bone('upper_arm2', 30, 456.6358013024077, Point2(25.00, -112.00))    .add(
        Bone('lower_arm2', 30, 352.3856149855908, Point2(2.00, -57.00))
)
).add(
    Bone('head', 30, -1.6576430948267917, Point2(0.00, -122.00))
).add(
    Bone('upper_leg1', 30, 566.7716441184316, Point2(-18.00, -3.00))    .add(
        Bone('lower_leg1', 30, 364.9171422299325, Point2(-2.00, -50.00))
)
).add(
    Bone('upper_leg2', 30, 523.3509496623373, Point2(18.00, 0.00))    .add(
        Bone('lower_leg2', 30, 22.80787630729788, Point2(-1.00, -53.00))
)
)


skeleton = Skeleton( root_bone )