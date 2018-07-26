#!/usr/bin/python
# coding:utf-8
import threading

import pygame
from pygame.locals import *
Lock = threading.Lock()
pygame.init()
num = 0


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class display(object):
    def __init__(self):
        global num
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480), 0, 32)
        print('init:', num)
        self.num = num
        num += 1
        self.drawBack((255, 255, 255))

    def drawBack(self, backColor):
        self.screen.fill(backColor)
        print('draw back:', self.num)

    def drawPoint(self, x, y, color, width=2):
        pygame.draw.rect(self.screen, color, Rect((x, y), (width, width)))

    def display(self):

        pygame.display.update()
        print('display:', self.num)

    def getColor(self, num):
        add = 1 << 31 - 1
        num = int(add + num)
        blue = num % 256
        num /= 256
        green = num % 256
        num /= 256
        red = num % 256
        return (green, blue, red)

    def displayData(self, data, offsetY, type=0):
        # print 'data len:', len(data)
        self.max = -256
        self.min = 256
        offset = 0
        step = 3
        offsetY = (step * 8 + 1) * offsetY
        for mcu in data:
            # print '\t', len(mcu)
            for YCrCb in mcu:
                # print '\t' * 2, len(YCrCb)
                for k in YCrCb:
                    # print '\t' * 3, len(k)
                    if len(k) == 0:
                        continue
                    if type == 0:
                        self.displayUnit(offset, offsetY, k, step)
                    else:
                        self.displayVert(offset, offsetY, k, step)
                    offset += 8 * step + 1
        print('max:', self.max, 'min:', self.min)

    def displayVert(self, offsetX, offsetY, unit, step=1):
        for x in range(8):
            for y in range(8):
                red = unit[x * 8 + y]
                if red > self.max:
                    self.max = red
                if red < self.min:
                    self.min = red

                red = self.getColor(red)
                # print red
                display().drawPoint(offsetX + x * step, offsetY + y * step, red, step)

    def displayUnit(self, offsetX, offsetY, unit, step=1):
        for x in range(8):
            for y in range(8):
                red = unit[x][y]
                if red > self.max:
                    self.max = red
                if red < self.min:
                    self.min = red

                red = self.getColor(red)
                # print red
                display().drawPoint(offsetX + x * step, offsetY + y * step, red, step)

    def test(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()


if __name__ == '__main__':
    tester = display()
    tester.drawPoint(15,  15, 0x889914, 9)
    tester.display()
    tester.test()
'''
while True:
    for event in pygame.event.get():
        '''
