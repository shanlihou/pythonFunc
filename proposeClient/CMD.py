from poster import Poster
import const

class CMD(object):
    def __init__(self, url):
        self.poster = Poster(url)
        
    def getMusicData(self, pitch):
        return {'cmd': 'music', 'type': 0, 'data': pitch}

    def getMoveData(self, data, duration, dir):
        return {'cmd': 'coco', 'act': 0, 'data': data, 'duration': duration, 'dir': dir}

    def playSec(self, sec, pType=const.PlayType.prelude):
        if pType == const.PlayType.prelude:
            pitches = sec.split(',')
            for pitch in pitches:
                data = self.getMusicData(pitch)
                self.poster.post(data)


    def notation(self, fileName):
        with open(fileName) as fr:
            musicData = fr.read()
            secs = musicData.split('\n')
            for sec in secs:
                if sec.startswith('n'):
                    continue

                self.playSec(sec)

    def test(self):
        pass