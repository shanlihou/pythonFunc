import re


def rep_func(m):
    target = m.group(1)
    pat = re.compile('_(\w)')
    pat.search(target)
    new = pat.sub(lambda x: x.group(1).upper(), target)
    ret = """def build{}(self, eventId):
        e = self.build_element(flowController.FlowEvent, element_id=eventId,
                               event_handler=tmp,
                               name=gameconst.DungeonFlowEventName.{})

        return e\n\n""".format(new, target)
    return ret


def repl(pat_str, fn, func):
    pat = re.compile(pat_str)
    fw = open(fn + '.new', 'w', encoding='utf-8')
    with open(fn, encoding='utf-8') as fr:
        for line in fr:
            find = pat.search(line)
            if find:
                print(find.groups())
                fw.write(pat.sub(func, line))
            else:
                fw.write(line)


if __name__ == '__main__':
    # repl(r"(SMB_\w+) = '.+'", fn, rep_func)
    pass
