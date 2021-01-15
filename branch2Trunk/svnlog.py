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
    for i in range(500):
        val = next(it, None)
        print(val)


if __name__ == '__main__':
    root_name = r'E:\svn\Dev\Server'
    main(root_name)