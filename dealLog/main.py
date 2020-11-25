# coding=utf-8
import os
import re
import time
import heapq


g_iter = iter(range(1000000000))


class DealLog(object):
    def __init__(self, src):
        self.src = src
        self.filters = [
            '[WorldLineStub(6024)]:enterLine',
        ]

    def isok(self, strin):
        for filterstr in self.filters:
            if filterstr in strin:
                return True
        else:
            return False

    def test(self):
        lines = []
        lineNum = 0
        with open(self.src, encoding='UTF-8') as fr:
            while 1:
                lineNum += 1
                try:
                    line = fr.readline()
                    if not line:
                        break
                    if self.isok(line):
                        print(lineNum, line)
                        lines.append(line)
                except UnicodeDecodeError as e:
                    print(lineNum)

        with open(self.src + '.1', 'w') as fw:
            for line in lines:
                fw.write(line)

    def filter(self):
        with open(self.src, encoding='UTF-8') as fr:
            fw = open(self.src + '.new', 'w')
            for line in fr:
                if self.isok(line):
                    fw.write(line)


class LogLine(object):
    def __init__(self, timestamp, line):
        self.timestamp = timestamp
        self.index = next(g_iter)
        self.line = line

    def __lt__(self, other):
        if self.timestamp == other.timestamp:
            return self.index < other.index

        return self.timestamp < other.timestamp

    def write_line(self, fp):
        fp.write(self.line)


class LogStream(object):
    def __init__(self, filename):
        self.stream = self.read_file(filename)
        self.last_timestamp = 0

    def read_file(self, filename):
        pat = re.compile(r'\[(\d+)\-(\d+)\-(\d+) (\d+)\:(\d+)\:(\d+) (\d+)\]')
        with open(filename, encoding='utf-8') as fr:
            for line in fr:
                find = pat.search(line)
                if find:
                    timestamp = self.get_timestamp(find.groups())
                    yield LogLine(timestamp, line)

    def read_one(self, timestamp):
        if self.last_timestamp <= timestamp:
            ret = next(self.stream, None)
            if ret is None:
                return ret

            self.last_timestamp = ret.timestamp
            return ret
        else:
            return None

    def get_timestamp(self, groups):
        a = time.strptime(' '.join(groups[:-1]), '%Y %m %d %H %M %S')
        timestamp = time.mktime(a)
        return timestamp * 1000 + int(groups[-1])


class MergeLog(object):
    def __init__(self, file_list):
        self.filters = [
            'Avatar(9461)',
            'WorldLineStub'
        ]
        self.file_list = file_list
        self.cache = []
        self.max_num = 50000
        self.fw = open(r'e:\shlog\merge.log', 'w', encoding='utf-8')

    def isok(self, strin):
        return True

    def push_if_pop(self, val):
        if not self.isok(val.line):
            return

        heapq.heappush(self.cache, val)
        if len(self.cache) > self.max_num:
            one = heapq.heappop(self.cache)
            one.write_line(self.fw)

    def test(self):
        streams = []
        for fn in self.file_list:
            streams.append(LogStream(fn))

        timestamp = 0
        while 1:
            ret = None
            isRead = False
            for stream in streams:
                _timestamp = timestamp
                while 1:
                    ret = stream.read_one(timestamp)
                    if ret is None:
                        break
                    else:
                        self.push_if_pop(ret)
                        isRead = True

                        if _timestamp < ret.timestamp:
                            _timestamp = ret.timestamp

                timestamp = _timestamp

            if not isRead:
                break

        while self.cache:
            one = heapq.heappop(self.cache)
            one.write_line(self.fw)


def main():
    ml = MergeLog([
        r'E:\trunk_server\kbengine\assets\logs\logger_baseapp.log',
        r'E:\trunk_server\kbengine\assets\logs\logger_cellapp.log',
    ])
    ml.test()


if __name__ == '__main__':
    main()
