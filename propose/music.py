#coding=utf-8
import winsound

class Music(object):
    def __init__(self):
        '''
        self.HZ = {'c': 523, 'c#': 554, 'd': 587, 'd#': 622, 'e': 659, 'f': 698, 
                   'f#': 740, 'g': 784, 'g#': 831, 'a': 880, 'a#': 932, 'b': 988}'''
        self.HZ = {'1': 523, '1#': 554, '2': 587, '2#': 622, '3': 659, '4': 698, 
                   '4#': 740, '5': 784, '5#': 831, '6': 880, '6#': 932, '7': 988}
        self.high = {'h': 2, 'm': 1, 'l': 0.5}
    
    
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
            
    def playPitch(self, pitch):
        pIter = iter(pitch)
        p = next(pIter)
        tmp = next(pIter)
        if tmp == '#':
            p += tmp
            tmp = next(pIter)
            
        high = tmp
        duration = float(''.join(list(pIter)))
        hz = self.HZ[p] * self.high[high]
        duration = int(duration * 170)
        print(p, high, duration, hz)
        winsound.Beep(hz, duration)
    
    def playSec(self, sec):
        pitchs = sec.split(',')
        for pitch in pitchs:
            self.playPitch(pitch)
    
    
    def playFile(self, fileName):
        with open(fileName) as fr:
            musicData = fr.read()
            secs = musicData.split('\n')
            for sec in secs:
                if sec.startswith('n'):
                    continue
                
                self.playSec(sec)
            
    def test(self):
        self.playFile('canon.txt')

def test():
    music = Music()
    music.test()
    
if __name__ == '__main__':
    test()