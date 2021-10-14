import const
import utils
import time


G_AVATAR_GBID = '8726031376526920939'
FLOW_NAME = 'GuildFlow'
WRITE_FILE_NAME = r'E:\shtlog\out\avatar.GuildFlow.log'
RECORD_FILE = r'E:\shLog\tmp\records.txt'


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
    with open(WRITE_FILE_NAME, 'w') as fw:
        for line in utils.get_origin_line_stream():
            if FLOW_NAME in line:
                fw.write(line)



if __name__ == '__main__':
    #main()
    print_records()