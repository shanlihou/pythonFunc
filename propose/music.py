# coding=utf-8
import winsound
import time


class Music(object):
    HZ = {'1': 523, '1#': 554, '2': 587, '2#': 622, '3': 659, '4': 698,
          '4#': 740, '5': 784, '5#': 831, '6': 880, '6#': 932, '7': 988}
    high = {'b': 4, 'h': 2, 'm': 1, 'l': 0.5}

    def test1(self):
        step = 523 // 12
        pitchIter = iter(self.pitchs)
        for i in range(523, 2 * 523, step):
            ch = next(pitchIter)
            if not ch.endswith('#'):
                print(i, ch)
                winsound.Beep(i, 500)

    def test2(self):
        last = 0
        for i in self.HZ:
            print(i, i - last)
            last = i
            winsound.Beep(i, 500)

    @classmethod
    def playPitch(cls, pitch):
        pIter = iter(pitch)
        p = next(pIter)
        tmp = next(pIter)
        if tmp == '#':
            p += tmp
            tmp = next(pIter)

        high = tmp
        duration = float(''.join(list(pIter)))
        duration = int(duration * 250)
        if p == '0':
            time.sleep(duration / 1000)
            return

        hz = cls.HZ[p] * cls.high[high]
        print(p, high, duration, hz)
        winsound.Beep(hz, duration)

    @classmethod
    def playSec(cls, sec):
        pitchs = sec.split(',')
        for pitch in pitchs:
            cls.playPitch(pitch)

    def playFile(self, fileName):
        start = 34
        with open(fileName) as fr:
            musicData = fr.read()
            secs = musicData.split('\n')
            for sec in secs:
                if sec.startswith('n'):
                    continue
                start -= 1
                if start < 0:
                    self.playSec(sec)

    def test(self):
        self.playFile('canon.txt')


def test():
    music = Music()
    music.test()


if __name__ == '__main__':
    test()
