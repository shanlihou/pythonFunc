import sys


fw = open('not_use.txt', 'w')
console = sys.stdout
sys.stdout = fw


def sh_print(*args):
    if len(args) == 1:
        console.write(str(args[0]) + '\n')
    else:
        console.write(str(args) + '\n')
