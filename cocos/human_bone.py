from cocos.skeleton import Bone, Skeleton

def Point2(*args): return args

root_bone = Bone('body', 70, -177.46383696945762, Point2(5.00, -33.00)).add(
    Bone('upper_arm1', 30, 602.934463049926, Point2(-17.00, -96.00))    .add(
        Bone('lower_arm1', 30, -38.94698145403902, Point2(1.00, -58.00))
)
).add(
    Bone('upper_arm2', 30, 473.13502769954044, Point2(10.00, -101.00))    .add(
        Bone('lower_arm2', 30, 43.30670750905642, Point2(-2.00, -63.00))
)
).add(
    Bone('head', 30, -5.5061017168338, Point2(-1.00, -127.00))
).add(
    Bone('upper_leg1', 30, 566.7716441184315, Point2(-1.00, -5.00))    .add(
        Bone('lower_leg1', 30, 350.4278321189955, Point2(-2.00, -63.00))
)
).add(
    Bone('upper_leg2', 30, 523.3509496623373, Point2(7.00, -5.00))    .add(
        Bone('lower_leg2', 30, 12.15702951581773, Point2(-2.00, -63.00))
)
)


skeleton = Skeleton( root_bone )