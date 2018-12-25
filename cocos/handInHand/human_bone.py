from cocos.skeleton import Bone, Skeleton

def Point2(*args): return args

root_bone = Bone('body', 70, -181.4769894842871, Point2(80.00, -48.00)).add(
    Bone('upper_arm1', 30, 603.071609599222, Point2(-31.00, -116.00))    .add(
        Bone('lower_arm1', 30, -37.73392048348615, Point2(-2.00, -53.00))
)
).add(
    Bone('upper_arm2', 30, 507.1061826659556, Point2(25.00, -112.00))    .add(
        Bone('lower_arm2', 30, -15.428819153105243, Point2(2.00, -57.00))        .add(
            Bone('f_body', 70, 229.22448312255662, Point2(-38.00, -150.00))            .add(
                Bone('f_upper_arm1', 30, 584.1112271775867, Point2(-31.00, -116.00))                .add(
                    Bone('f_lower_arm1', 30, -0.2193917324523949, Point2(-2.00, -53.00))
)
)            .add(
                Bone('f_upper_arm2', 30, 473.13502769954044, Point2(25.00, -112.00))                .add(
                    Bone('f_lower_arm2', 30, 267.4462614921407, Point2(2.00, -57.00))
)
)            .add(
                Bone('f_head', 30, -0.905045775160882, Point2(0.00, -122.00))
)            .add(
                Bone('f_upper_leg1', 30, 566.7716441184316, Point2(-18.00, -3.00))                .add(
                    Bone('f_lower_leg1', 30, 364.9171422299325, Point2(-2.00, -50.00))
)
)            .add(
                Bone('f_upper_leg2', 30, 523.3509496623373, Point2(18.00, 0.00))                .add(
                    Bone('f_lower_leg2', 30, 22.80787630729788, Point2(-1.00, -53.00))
)
)
)
)
).add(
    Bone('head', 30, -14.55756347235696, Point2(-5.00, -125.00))
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