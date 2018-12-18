import xml.sax
from lxml import etree
import os


class defHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.tree = []
        self.otherCount = 0
        self.interFaces = []

    def startElement(self, tag, attributes):
        self.tree.append(tag)

    def endElement(self, tag):
        del self.tree[-1]

    def getPropName(self):
        if 'Properties' not in self.tree:
            return ''

        return self.tree[2]

    def characters(self, content):
        if 'Flags' in self.tree:
            if 'OTHER_CLIENTS' in content or 'ALL_CLIENTS' in content:
                print(self.getPropName())
                print(content)
                self.otherCount += 1
        elif 'Interface' in self.tree:
            self.interFaces.append(content.strip())


class defParser(object):
    syncTup = ('OTHER_CLIENTS', 'ALL_CLIENTS')

    def __init__(self, name):
        self.html = etree.parse(name, etree.HTMLParser())
        self.interfaces = []
        self.others = []
        self.otherCount = 0

    def parseInterfaces(self):
        ret = self.html.xpath('//interface')
        for i in ret:
            text = i.xpath('child::text()')
            text = str(text[0])
            self.interfaces.append(text.strip())

    def parseOther(self):
        ret = self.html.xpath('//properties/*')
        for i in ret:
            flags = i.xpath('child::flags')[0]
            text = flags.xpath('child::text()')[0]
            text = text.strip()
            if text in self.syncTup:
                print(i.tag)
                self.otherCount += 1

    def parse(self):
        self.parseInterfaces()
        self.parseOther()


class EntityCost(object):
    def __init__(self, path, fileName):
        self.path = path
        self.name = fileName

    def openfile(self, fileName):
        fn = os.path.join(self.path, fileName)
        return open(fn)

    def findFile(self, path, fileName):
        for i in os.listdir(path):
            fullName = os.path.join(path, i)
            if os.path.isdir(fullName):
                ret = self.findFile(fullName, fileName)
                if ret:
                    return ret

            if i == fileName:
                return fullName

        return ''

    def getName(self, name):
        return self.findFile(self.path, name)

    def parse(self, name):
        dp = defParser(self.getName(name))
        dp.parse()
        count = dp.otherCount
        print(count)
        for i in dp.interfaces:
            count += self.parse(i + '.def')

        return count

    def test(self):
        # self.parse(self.name)
        if 0:
            dp = defParser(self.getName('Monster.def'))
            dp.parse()
            print(dp.interfaces)
            print(dp.otherCount)
        else:
            count = self.parse(self.name)
            print(count)


if __name__ == '__main__':
    ec = EntityCost(
        r'E:\svn\Dev\Server\kbeWin\kbengine\assets\scripts\entity_defs', r'Monster.def')
    ec.test()
