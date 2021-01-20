import re

def main():
    root = r'E:\trunk_server\kbengine\assets\scripts\data\fightProp_define.py'
    pat = re.compile(r'\s"(\w+)": _tools\.RODict\({')
    patSub = re.compile(r'[^\w]e\.(\w+)[^\w]')
    adj = {}
    degree = {}
    with open(root, encoding='utf-8') as fr:
        cur = ''
        for line in fr:
            find = pat.search(line)
            if find:
                print(find.groups())
                cur = find.groups()[0]
                adj.setdefault(cur, [])

            if '"formula' in line:
                ret = patSub.findall(line)
                print(ret)
                for sub in ret:
                    adj.setdefault(sub, [])
                    adj[sub].append(cur)
                    degree[cur] = degree.get(cur, 0) + 1

    print(adj)
    print(degree)
    q = []
    for k in adj:
        if k not in degree:
            q.append(k)

    ret = []
    while q:
        cur = q.pop(0)
        ret.append(cur)
        for i in adj[cur]:
            degree[i] -= 1
            if not degree[i]:
                q.append(i)
    print(ret)

if __name__ == '__main__':
    main()