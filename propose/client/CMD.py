from poster import Poster
import sys
sys.path.append('..')
import const
import time
import os


class CMD(object):
    def __init__(self, url):
        self.poster = Poster(url)

    @staticmethod
    def getMusicData(pitch):
        return {'cmd': 'music', 'type': 0, 'data': pitch}

    @staticmethod
    def getMoveData(data, duration, dir):
        return {'cmd': 'coco', 'act': 0, 'data': data, 'duration': duration, 'dir': dir}

    @staticmethod
    def getAnimData(x, y, duration):
        return {'cmd': 'coco', 'type': 1, 'name': 'baobao_recv'}

    def getPitchDur(self, pitch):
        if pitch[1] == '#':
            return int(pitch[3:]) * const.MUSIC_DURATION
        else:
            return int(pitch[2:]) * const.MUSIC_DURATION

    def playSec(self, sec, pType=const.PlayType.prelude):
        if pType == const.PlayType.prelude:
            pitches = sec.split(',')
            for pitch in pitches:
                data = self.getMusicData(pitch)
                pitchDur = self.getPitchDur(pitch)
                datas = [data]
                datas.append(self.getMoveData('123', pitchDur / 1000, 0))
                self.poster.post(datas)
                time.sleep(pitchDur / 1000)

    def notation(self, fileName):
        with open(fileName) as fr:
            musicData = fr.read()
            secs = musicData.split('\n')
            for sec in secs:
                if sec.startswith('n'):
                    continue

                self.playSec(sec)

    def test(self):
        print(os.getcwd())
        opt = 2
        if opt == 0:
            self.notation('..\canon.txt')
        elif opt == 1:
            pitch = '3h8'
            data = self.getMusicData(pitch)
            pitchDur = self.getPitchDur(pitch)
            datas = [data]
            datas.append(self.getMoveData('123', pitchDur / 1000, 1))
            self.poster.post(datas)
        elif opt == 2:
            self.poster.post(self.getAnimData(150, 150, 5))


if __name__ == '__main__':
    cmd = CMD('http://127.0.0.1:8000/cmd/')
    cmd.test()
