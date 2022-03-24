import pickle

HEX = '80034A2B050F625D7100288A080F11116FE219E22E8A08BCBBBB85E219E22E8A0810EFEEDEE219E22E8A08D1888812E319E22E8A08AC66660EE319E22E658671012E'

# def escape_string(value, mapping=None):
#     """escapes *value* without adding quote.

#     Value should be unicode
#     """
#     if value is None:
#         return 'NULL'
#     if type(value) in (bytes, bytearray):
#         return '0x%s'%value.hex()
#     if type(value) is not str:
#         return str(value)
#     return "'%s'" % value.translate(_escape_table)

# def test():
#     data = {
#         5690608648741453826:{86040017}
#     }

#     print(escape_string(pickle.dumps(data)))

def main():
    _it = iter(HEX)
    hex_list = []
    while 1:
        ch1 = next(_it, None)
        if ch1 == None:
            break

        ch2 = next(_it)
        ch = int(f'{ch1}{ch2}', 16)
        hex_list.append(ch)

    print(hex_list)
    ret = pickle.loads(bytes(hex_list))
    print(ret)


if __name__ == '__main__':
    main()