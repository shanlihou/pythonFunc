from poster import Poster

class CMD(object):
    def __init__(self, url):
        self.poster = Poster(url)
        
    def getMusicData(self, pitch):
        return {'cmd': 'music', 'type': 0, 'data': pitch}

    def getMoveData(self, data, duration, dir):
        return {'cmd': 'coco', 'act': 0, 'data': data, 'duration': duration, 'dir': dir}

    def test(self):
        pass