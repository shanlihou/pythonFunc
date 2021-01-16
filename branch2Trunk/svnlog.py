import os


def log_iter(root):
    os.chdir(root)
    cur = []
    with os.popen('svn log') as fr:
        for line in fr:
            line = line.strip()
            if line != '------------------------------------------------------------------------':
                cur.append(line)
            else:
                if not cur:
                    continue

                if cur[0].split('|')[1].strip() == 'chenkezheng':
                    yield cur
                cur = []


def main(root):
    it = log_iter(root)
    with open('out.txt', 'w') as fw:
        for i in range(600):
            val = next(it, None)
            fw.write('\n'.join(val) + '\n')


if __name__ == '__main__':
    root_name = r'E:\svn\Dev\Server'
    main(root_name)