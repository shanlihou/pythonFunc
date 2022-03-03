import pickle

HEX = '8003635F7570660A466978656441727261790A71004D29035D7101284E4E4E4E4E658671025271032E'


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