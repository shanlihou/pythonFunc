from cocos.skeleton import Bone, Skeleton

def Point2(*args): return args

root_bone = Bone('body', 70, -180.0, Point2(0.00, 0.00)).add(
    Bone('upper_arm', 30, 507.2153951616356, Point2(40.00, -66.00))    .add(
        Bone('lower_arm', 30, 29.999999999999996, Point2(8.00, -41.00))
)
)


skeleton = Skeleton( root_bone )