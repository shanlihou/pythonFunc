import math

from jpg import display


class MapDisplay(object):
    def __init__(self, cards, mons):
        self.width = 2
        self.cards = cards
        self.mons = mons

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
                elif mark == '9':
                    color = 0x123456
                elif mark == '2':
                    #color = 0x149988
                    color = 0x123456

                self.drawPoint(x + xx, y + yy, color)

    def drawMons(self, x, y, area):
        y += 32
        w, h, z = eval(area)
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

    def test(self):
        display.display()
        self.displayMap()
        display.display().display()
        display.display().test()
