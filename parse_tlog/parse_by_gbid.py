import const
import utils
import time


G_AVATAR_GBID = '8726031376526920939'
G_GUILD_UUID = '88113899812159490'
FLOW_NAME = 'GuildBanditFlow'
WRITE_FILE_NAME = r'E:\shtlog\out\avatar.GuildBanditFlow.log'
RECORD_FILE = r'E:\shLog\tmp\records.txt'
READ_FILE = r'F:\shdownload\log\11.152.254.179_data_home_user00_log_logger_baseapp.log'


def filter_read():
    fw = open(READ_FILE + '.new', 'w', encoding='utf-8')
    with open(READ_FILE) as fr:
        for line in fr:
            if 'Channel::handshake: kcp' in line:
                continue

            fw.write(line)



def print_records():
    with open(RECORD_FILE) as fr:
        for line in fr:
            tups = line.split(' ')
            tups = [i.strip() for i in tups if i.strip()]
            _time = tups[-1]
            _time = time.localtime(int(_time))
            _time = time.strftime("%Y-%m-%d %H:%M:%S", _time)
            tups[-1] = _time
            print(tups)

def main():
    with open(WRITE_FILE_NAME, 'w', encoding='utf-8') as fw:
        for line in utils.get_origin_line_stream():
            if FLOW_NAME in line:
                fw.write(line)



if __name__ == '__main__':
    #main()
    # print_records()
    #main()
    filter_read()