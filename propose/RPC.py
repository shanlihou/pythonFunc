from singleton import singleton


@singleton
class RPC(object):
    def __init__(self):
        pass

    def parseCmd(self, jsonData):
        cmd = jsonData['cmd']
        if hasattr(self, cmd):
            getattr(self, cmd)(jsonData)

    def test(self, jsonData):
        print(jsonData)