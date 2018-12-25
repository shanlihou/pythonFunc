import png
import os

parseDict = {
    'rgba': [3, 4, 'RGBA'],
    'grey': [1, 2, 'LA']}


def dealPng(name):
    fileName = os.path.join('resources', name)
    pr = png.Reader(filename=fileName)
    rgb = pr.asDirect()
    width, height, pixels, meta = rgb

    if meta['greyscale']:
        start, step, code = parseDict['grey']
    else:
        start, step, code = parseDict['rgba']

    print(width, height, meta)
    pList = []
    for i in pixels:
        pList.append(i)
    for data in pList:
        for index in range(start, len(data), step):
            al = data[index]
            data[index] = 20 if al else 0

    png.from_array(pList, code).save(name)


def dealPath(path):
    for i in os.listdir(path):
        dealPng(i)


class PngDeal(object):
    def __init__(self, name):
        self.name = name
        self.pr = png.Reader(filename=name)
        import imp
        self.disp = imp.load_source(
            'disp', r'E:\shgithub\python\pythonFunc\Lib\display.py').displayInstance

    def test(self):
        width, height, pixels, meta = self.pr.asDirect()
        for x, data in enumerate(pixels):
            for y in range((len(data) // 4)):
                pixel = data[y * 4]
                pixel = 0x050505 if pixel > 128 else 0
                self.disp.drawPoint(x, y, pixel, 1)
        self.disp.display()
        self.disp.test()


if __name__ == '__main__':
    opt = 0
    if opt:
        dealPng('message.png')
    else:
        dealPath('resources')
