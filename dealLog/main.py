import os


class DealLog(object):
    def __init__(self, src):
        self.src = src
        self.filters = ['onWeatherChanged:',
                        'guild battle start',
                        'changeWeather']

    def isok(self, strin):
        for filterstr in self.filters:
            if filterstr in strin:
                return True
        else:
            return False

    def test(self):
        lines = []
        lineNum = 0
        with open(self.src, encoding='UTF-8') as fr:
            while 1:
                lineNum += 1
                try:
                    line = fr.readline()
                    if not line:
                        break
                    if self.isok(line):
                        print(lineNum, line)
                        lines.append(line)
                except UnicodeDecodeError as e:
                    print(lineNum)

        with open(self.src + '.1', 'w') as fw:
            for line in lines:
                fw.write(line)


def main():
    dl = DealLog(r'C:\Users\Administrator\Documents\WXWork\1688851680425036\Cache\File\2020-06\logger_cellapp(6).log')
    dl.test()


if __name__ == '__main__':
    main()
