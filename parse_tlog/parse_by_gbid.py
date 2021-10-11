import const
import utils


G_AVATAR_GBID = '8726875801857469109'
FLOW_NAME = 'LingxuRewardFlow'
WRITE_FILE_NAME = r'E:\shtlog\out\avatar.LingxuRewardFlow.log'


def main():
    with open(WRITE_FILE_NAME, 'w') as fw:
        for line in utils.get_origin_line_stream():
            if FLOW_NAME in line:
                fw.write(line)



if __name__ == '__main__':
    main()