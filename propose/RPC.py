from singleton import singleton
from center import center
from music import Music


@singleton
class RPC(object):
    def __init__(self):
        pass

    def parseCmd(self, jsonData):
        if isinstance(jsonData, list):
            for data in jsonData:
                self.parse(data)
        else:
            self.parse(jsonData)

    def parse(self, jsonData):
        cmd = jsonData['cmd']
        if hasattr(self, cmd):
            getattr(self, cmd)(jsonData)

    def test(self, jsonData):
        print(jsonData)

    @staticmethod
    def coco(jsonData):
        center.getInstance('coco').addTask(jsonData)

    @staticmethod
    def music(jsonData):
        Music.playCmd(jsonData)
