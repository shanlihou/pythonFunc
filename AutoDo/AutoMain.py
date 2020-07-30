import os
import time
import heapq

g_task_list = [
    ('2020-07-30 12:59:00', r'D:\soft\baidu\BaiduNetdisk\baidunetdisk.exe')
]


class TaskVal(object):
    def __init__(self, timestamp, cmd_str):
        self.timestamp = timestamp
        self.cmd_str = cmd_str

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def do(self):
        os.system(self.cmd_str)


class TimeTask(object):
    def __init__(self):
        self.task = []
        for time_str, cmd_str in g_task_list:
            timestamp = self.get_timestamp(time_str)
            delay = self.get_delay(timestamp)
            if delay > 0:
                heapq.heappush(self.task, TaskVal(timestamp, cmd_str))

    def get_delay(self, timestamp):
        now = int(time.mktime(time.localtime()))
        return timestamp - now

    def get_timestamp(self, time_str):
        return time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S'))

    def do_task(self):
        task_now = TaskVal(int(time.mktime(time.localtime())), '')
        heapq.heappush(self.task, task_now)
        while self.task:
            pop_obj = heapq.heappop(self.task)
            if pop_obj is task_now:
                break

            print('do')
            pop_obj.do()


def main():
    tt = TimeTask()
    while 1:
        tt.do_task()
        time.sleep(1)


if __name__ == '__main__':
    main()
