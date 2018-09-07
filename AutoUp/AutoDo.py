from bmob import BMOB
import json
import threading
import time
from builtins import classmethod


class AutoDo(object):
    table = 'script'
    objId = 'ce8e21ea1d'

    def __init__(self):
        pass

    def update(self, fileName):
        data = self.makeData(fileName)
        BMOB().putData(self.objId, self.table, data)

    def add(self, fileName):
        data = self.makeData(fileName)
        BMOB().addData(self.table, data)

    def makeData(self, fileName):
        with open(fileName) as fr:
            data = fr.read()
            data = {'name': fileName,
                    'data': data,
                    'state': 0}
            return json.dumps(data)

    def get(self):
        data = BMOB().get(self.table)
        dataDict = json.loads(data)['results']
        for i in dataDict:
            fileName = i['name']
            content = i['data']
            with open(fileName, 'w') as fw:
                fw.write(content)

    @classmethod
    def getMainTime(cls):
        data = BMOB().get(cls.table + '/' + cls.objId)
        data = json.loads(data)['updatedAt']
        updateTime = time.strptime(data, '%Y-%m-%d %H:%M:%S')
        updateTime = time.mktime(updateTime)
        return updateTime

    def run(self):
        import AutoMain
        auto = AutoMain.AutoMain()
        self.auto = auto
        auto.run()

    def stop(self):
        self.auto.stop()

    def test(self):
        # self.send(r'..\bmob\MyPwd.py')
        # self.get()
        self.update('AutoMain.py')


def run(args):
    auto = args
    auto.get()
    auto.run()


class MainDo(object):
    def __init__(self):
        pass

    def judgeUpdate(self):
        upTime = AutoDo.getMainTime()
        return upTime > self.upTime + 5

    def start(self):
        self.upTime = AutoDo.getMainTime()
        self.auto = AutoDo()
        self.t = threading.Thread(target=run, args=(self.auto, ))
        self.t.start()

    def run(self):
        while 1:
            time.sleep(2)
            if not self.judgeUpdate():
                continue
            isAlive = self.t.is_alive()

            if isAlive:
                self.auto.stop()
            else:
                self.start()


if __name__ == '__main__':
    auto = AutoDo()
    auto.test()
