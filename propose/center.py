class Center(object):
    clsDict = {}

    def __init__(self):
        print('center init')

    def register(self, name, cls):
        self.clsDict[name] = cls

    def getInstance(self, name):
        return self.clsDict[name]


center = Center()
