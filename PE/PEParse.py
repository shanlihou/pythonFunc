# coding=utf-8
class PEParse(object):
    def __init__(self, path):
        self.path = path
        self.reader = open(self.path, 'rb')

    def readNum(self, length):
        num = self.reader.read(length)
        num = int.from_bytes(num, byteorder='little')
        return num

    def parse(self):
        self.magic = self.reader.read(2)
        self.reader.read(18)
        self.e_ip = self.reader.read(2)
        self.e_cs = self.reader.read(2)
        print(self.magic)
        print(self.e_ip)
        print(self.e_cs)
        self.reader.read(36)
        # read pe
        self.e_lfanew = self.readNum(4)
        print('%x' % self.e_lfanew)
        print(self.reader.tell())
        self.reader.seek(self.e_lfanew)
        PE = self.reader.read(4)
        print(PE)

    def test(self):
        self.parse()


if __name__ == '__main__':
    pe = PEParse(r'D:\game\Warcraft III\war3.exe')
    pe.test()
