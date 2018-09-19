import math

from jpg import display
from jpg.display import displayInstance


class MapDisplay(object):
    def __init__(self, cards, mons, crystals):
        self.width = 2
        self.cards = cards
        self.mons = mons
        self.crystals = crystals

    def drawPoint(self, x, y, color):
        y = 150 - y
        x = x + 200
        display.display().drawPoint(x * self.width, y * self.width, color, self.width)

    def drawCards(self, x, y, card):
        if not card:
            return

        for xx, line in enumerate(card):
            for yy, mark in enumerate(line):
                if mark == '1':
                    color = 0x889914
                elif mark == '0':
                    color = 0x123456
                elif mark == '2':
                    #color = 0x149988
                    color = 0x123456

                self.drawPoint(x + xx, y + yy, color)

    def drawMons(self, x, y, area):
        w, z, h = eval(area)
        w = math.ceil(w)
        h = math.ceil(h)
        for xx in range(w):
            for yy in range(h):
                self.drawPoint(x + xx, y - yy, 0x149988)

    def displayMap(self):
        for info in self.cards:
            x, y = info['pos']
            self.drawCards(x, y, info['card'].turnMap)

        for info in self.mons:
            x, y = info['pos']
            print(x, y, info['name'])
            self.drawMons(x, y, info['area'])

        for crystal in self.crystals:
            x, y = crystal.pos
            y
            print('crystal:', x, y, crystal.oriPos)
            self.drawPoint(x, y, 0xff8302)

    @staticmethod
    def getMapXY(x, y):
        x /= 2
        y /= 2
        x -= 200
        y = 150 - y
        return x, y

    @staticmethod
    @displayInstance.callBack
    def mouseMotion(x, y):
        x, y = MapDisplay.getMapXY(x, y)
        display.display().displayText('%d, %d' % (x, y), 0, 0)

    def test(self):
        display.display()
        self.displayMap()
        display.display().display()
        display.display().test()
