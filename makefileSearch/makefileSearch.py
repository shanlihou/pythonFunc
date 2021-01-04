import os
ROOT = r'D:\shKbeWin\kbe\src'

def search_in_file(filename, content):
    with open(filename) as fr:
        for line in fr:
            if content in line:
                print(filename)
                print(line)


def rec_search(filename):
    for i in os.listdir(filename):
        new = os.path.join(filename, i)
        if os.path.isdir(new):
            rec_search(new)
            continue

        if new.endswith('.mak') or new.lower().endswith('makefile'):
            search_in_file(new, 'MYSQL_CONFIG_PATH')


def main():
    rec_search(ROOT)


if __name__ == '__main__':
    main()