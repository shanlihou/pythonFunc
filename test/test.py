import gzip
if __name__ == '__main__':
    a = b'\x1f\x8b\x08\x00\xdd,P`\x02\xffc` \x03\x00\x00\x0ew\xaf\x195\x00\x00\x00'
    a = gzip.decompress(a)
    print(a)