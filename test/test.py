import gzip
from collections import deque
class A(object):
    def __init__(self, b, c):
        self.b = b
        self.c = c

if __name__ == '__main__':
    a = b'\x1f\x8b\x08\x00\xdd,P`\x02\xffc` \x03\x00\x00\x0ew\xaf\x195\x00\x00\x00'
    a = gzip.decompress(a)
    print(a)
    q = deque()
    a = A(1, 2)
    q.append(a)
    q.append(A(3, 4))
    q.append(A(5, 6))
    q.remove(a)
    print(q)