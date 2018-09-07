# coding=utf-8
import re
import structStr


class BaseParse(object):
    def __init__(self, reader=None, offset=None, cStruct=None):
        self.printSet = []
        self.typeLen = {'WORD': 2,
                        'DWORD': 4,
                        'BYTE': 1}
        if reader:
            self.reader = reader
            if offset:
                self.reader.seek(offset)
                
        if cStruct:
            self.cStruct = cStruct

    def readNum(self, length):
        num = self.reader.read(length)
        num = int.from_bytes(num, byteorder='little')
        return num

    def parseAttr(self, name, length):
        __ = self.readNum(length)
        setattr(self, name, __)
        self.printSet.append(name)

    def parseStruct(self):
        pat = re.compile('(\w+)\s+(\w+);')
        find = pat.findall(self.cStruct)
        for typeName, name in find:
            length = self.typeLen[typeName]
            self.parseAttr(name, length)

    def __str__(self):
        strRet = ''
        for i in self.printSet:
            strRet += i + ':' + '%x' % getattr(self, i) + '\n'
        return strRet


class ImageFileHeader(BaseParse):
    def __init__(self, reader):
        super(ImageFileHeader, self).__init__()
        self.reader = reader
        self.cStruct = structStr.ImageFileHeaderStructStr

    def parse(self):
        self.parseStruct()


class ImageDataDirectory(BaseParse):
    def __init__(self, reader):
        super(ImageDataDirectory, self).__init__()
        self.reader = reader
        self.cStruct = structStr.ImageDataDirectoryStructStr


class ImageOptionalHeader(BaseParse):
    def __init__(self, reader):
        super(ImageOptionalHeader, self).__init__()
        self.reader = reader
        self.cStruct = structStr.ImageOptionalHeaderStructStr

    def parse(self):
        self.parseStruct()
        self.dataDirectory = []
        for i in range(self.NumberOfRvaAndSizes):
            dataDir = ImageDataDirectory(self.reader)
            dataDir.parseStruct()
            self.dataDirectory.append(dataDir)

    def __str__(self):
        ret = super(ImageOptionalHeader, self).__str__()
        for i in range(self.NumberOfRvaAndSizes):
            ret += '-' * 60 + '\n'
            ret += self.dataDirectory[i].__str__()
        return ret


class ImageSectionHeader(BaseParse):
    def __init__(self, reader):
        super(ImageSectionHeader, self).__init__()
        self.reader = reader
        self.cStruct = structStr.ImageSectionHeaderStructStr

    def parse(self):
        self.name = self.reader.read(8)
        self.parseStruct()

    def __str__(self):
        ret = self.name.decode('utf8')
        ret += '\n' + super(ImageSectionHeader, self).__str__()
        return ret


class ImageImportDescriptor(BaseParse):
    def __init__(self, reader, fileOffset):
        super(ImageImportDescriptor, self).__init__(reader)
        self.reader.seek(fileOffset)
        self.cStruct = structStr.ImageImportDescriptor

    def parse(self):
        self.parseStruct()


class PEParse(BaseParse):
    def __init__(self, path):
        self.path = path
        self.reader = open(self.path, 'rb')

    def getFileOffset(self, rva):
        ishIn = None
        for ish in self.ish:
            print(rva, ish.VirtualAddress)
            if rva < ish.VirtualAddress:
                break

            ishIn = ish

        return ishIn and rva - ishIn.VirtualAddress + ishIn.PointerToRawData

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
        self.PE = self.reader.read(4)
        # read image_file_header
        ifh = ImageFileHeader(self.reader)
        ifh.parse()
        self.ifh = ifh
        print(ifh)
        # read image_optional_header
        print('-' * 60)
        ioh = ImageOptionalHeader(self.reader)
        ioh.parse()
        print(ioh)
        self.ioh = ioh
        # read image section header
        self.ish = []
        for i in range(self.ifh.NumberOfSections):
            print('-' * 60)
            ish = ImageSectionHeader(self.reader)
            ish.parse()
            self.ish.append(ish)
            print(ish)
        # parse table
        self.InputTable = []
        for dd in self.ioh.dataDirectory:
            if not dd.VirtualAddress:
                continue

            offset = self.getFileOffset(dd.VirtualAddress)
            iid = ImageImportDescriptor(self.reader, offset)
            iid.parse()
            self.InputTable.append(iid)
            print(iid)
            nameRva = iid.Name
            nameOffset = self.getFileOffset(nameRva)
            if not nameOffset:
                continue

            self.reader.seek(nameOffset)
            print(self.reader.read(20))

    def test(self):
        self.parse()


if __name__ == '__main__':
    pe = PEParse(r'D:\game\Warcraft III\war3.exe')
    pe.test()
