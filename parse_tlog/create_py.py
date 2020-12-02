#coding = utf-8
import xml.sax
filename = 'e:\\shtlog\\手游经分Tlog标准_V1.3.3.xml'


class JingFenHandler(xml.sax.ContentHandler):
    def __init__(self, name):
        self.name = name
        self.tag_stack = []
        self.is_in = False
        self.entries = []

    def startElement(self, tag, attributes):
        self.tag_stack.append(tag)
        if tag == 'struct' and attributes['name'] == self.name:
            self.is_in = True
        elif tag == 'entry':
            if self.is_in:
                self.entries.append(attributes['name'])

    def endElement(self, tag):
        if tag == self.tag_stack[-1]:
            self.tag_stack.pop()

        if tag == 'struct':
            self.is_in = False

    def get_val_name_str(self):
        def _func(name):
            ret = ''
            for i in name:
                if i.isupper():
                    yield ret
                    ret = ''

                ret += i

            yield ret

        return '_'.join(map(lambda x: x.upper(), filter(lambda x: x, _func(self.name))))

    def gen(self):
        print(self.get_val_name_str())
        ents = self.entries[3:]
        ents_str = ', '.join(ents)
        ret_str = 'def make{}({}):\n'.format(self.name, ents_str) + \
                '{}logData = [{}]\n'.format(' ' * 4, ents_str) + \
                '{}TLOG(gameconst.GameLog.LOG_{}, logData)\n'.format(' ' * 4, self.get_val_name_str())
        print(ret_str)



if __name__ == '__main__':
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    h = JingFenHandler('PlayerFriendsList')
    parser.setContentHandler(h)
    parser.parse(filename)
    h.gen()