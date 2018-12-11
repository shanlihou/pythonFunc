from cocos.skeleton import Bone, Skeleton

def Point2(*args): return args

root_bone = Bone('body', 70, -176.55261314813475, Point2(0.00, 0.00)).add(
    Bone('upper_arm1', 30, 562.0043744244753, Point2(-18.00, -15.00))    .add(
        Bone('lower_arm1', 30, -13.4762851295763, Point2(0.00, -31.00))
)
).add(
    Bone('upper_arm2', 30, 507.2153951616356, Point2(22.00, -12.00))    .add(
        Bone('lower_arm2', 30, 34.48170986038606, Point2(0.00, -32.00))
)
).add(
    Bone('head', 30, 0.4701067409211115, Point2(0.00, 0.00))
)


skeleton = Skeleton( root_bone )