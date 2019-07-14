#coding:utf-8
from poster import Poster
import sys
sys.path.append('..')
import const
import time
import os
import random


class CMD(object):
    text = '我爱你应彬小宝宝嫁给我吧'
    def __init__(self, url1, url2):
        self.lPoster = Poster(url1)
        self.rPoster = Poster(url2)
        self.poster = Poster(url1)
        self.turnIter = self.getCurTurn()
        
    def getCurTurn(self):
        textIter = iter(self.text)
        cur = 0
        text = ''
        dir = 0
        while 1:
            if cur == 0:
                text = next(textIter)
                dir = random.randint(0, 3)
            yield text, dir
            cur = (cur + 1) % 2

    @staticmethod
    def getMusicData(pitch):
        return {'cmd': 'music', 'type': 0, 'data': pitch}

    @staticmethod
    def getMoveData(data, duration, dir):
        return {'cmd': 'coco', 'act': 0, 'data': data, 'duration': duration, 'dir': dir}

    @staticmethod
    def getAnimData(x, y, duration):
        return {'cmd': 'coco', 'type': 1, 'name': 'baobao_recv'}

    @staticmethod
    def getZooData(duration):
        return {'cmd': 'coco', 'type': 2, 'duration': duration}

    @staticmethod
    def getThrowData(duration):
        return {'cmd': 'coco', 'type': 3, 'duration': duration}

    @staticmethod
    def getCodehData(code, duration):
        return {'cmd': 'coco', 'type': 4, 'code': code, 'duration': duration}

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
                text, dir = next(self.turnIter)
                datas.append(self.getMoveData(text, pitchDur / 1000, dir))
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
        opt = 5
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
        elif opt == 3:
            self.poster.post(self.getZooData(5))
        elif opt == 4:
            self.poster.post(self.getThrowData(5))
        elif opt == 5:
            self.poster.post(self.getCodehData('addCatch', 5))
            time.sleep(5)
            self.poster.post(self.getCodehData('addCatch2', 5))


if __name__ == '__main__':
    cmd = CMD('http://127.0.0.1:8000/cmd/', 'http://127.0.0.1:8000/cmd/')
    cmd.test()
