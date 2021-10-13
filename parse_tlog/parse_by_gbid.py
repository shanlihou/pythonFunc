import const
import utils


G_AVATAR_GBID = '8726031376526920939'
FLOW_NAME = 'GuildFlow'
WRITE_FILE_NAME = r'E:\shtlog\out\avatar.GuildFlow.log'


def main():
    with open(WRITE_FILE_NAME, 'w') as fw:
        for line in utils.get_origin_line_stream():
            if FLOW_NAME in line:
                fw.write(line)



if __name__ == '__main__':
    main()