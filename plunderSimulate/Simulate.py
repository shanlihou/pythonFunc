from Avatar import AvatarPool
import config


if __name__ == '__main__':
    AvatarPool().initAvatars(config.avatar_num)
    AvatarPool().go(config.days)