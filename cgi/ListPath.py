import os
class ListPath(object):
    def __init__(self, path):
        self.path = path
    def getAllFile(self):
        return [i for i in self.recPath(self.path)]
    def recPath(self, path):
        for i in os.listdir(path):
            new = os.path.join(path, i)
            if os.path.isdir(new):
                for j in self.recPath(new):
                    yield j
                continue
            yield new