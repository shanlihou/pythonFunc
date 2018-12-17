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
            if 'OTHER_CLIENTS' in content:
                print(self.getPropName())
                print(content)
                self.otherCount += 1
        elif 'Interface' in self.tree:
            self.interFaces.append(content.strip())


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
        print(self.getName(name))
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        Handler = defHandler()
        parser.setContentHandler(Handler)

        parser.parse(self.getName(name))
        print(Handler.otherCount)
        print(Handler.interFaces)
        for ifName in Handler.interFaces:
            self.parse(ifName + '.def')

    def test(self):
        # self.parse(self.name)
        if 1:
            html = etree.parse(self.getName('iBaseWithCell.def'), etree.HTMLParser())
            print(html.xpath('//root'))
            for i in html.xpath('//*'):
                print(i.tag)


if __name__ == '__main__':
    ec = EntityCost(
        r'E:\svn\Dev\Server\kbeWin\kbengine\assets\scripts\entity_defs', r'Monster.def')
    ec.test()
