import time
filepath = r'E:\shLog\merge\merge.log'


def main():
    _dic = {}

    with open(filepath) as fr:
        for line in fr:
            if 'start merge' in line:
                sps = line.split(' ')
                _key = sps[-1]
                _dic.setdefault(_key, {})

                time_str = '{} {}'.format(sps[1], sps[2].split(',')[0])
                _timestamp = time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S'))

                _dic[_key]['start_str'] = line
                _dic[_key]['start_ts'] = _timestamp

            elif 'finish mergeing' in line:
                sps = line.split(' ')
                _key = sps[-1]
                _dic.setdefault(_key, {})

                time_str = '{} {}'.format(sps[1], sps[2].split(',')[0])
                _timestamp = time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S'))

                _dic[_key]['end_str'] = line
                _dic[_key]['end_ts'] = _timestamp

    _sort_list = []
    for k, v in _dic.items():
        try:
            v['name'] = k
            v['sort'] = v['end_ts'] - v['start_ts']
            _sort_list.append(v)
        except Exception as e:
            print(e, v)

    _sort_list = sorted(_sort_list, key=lambda x: -x['sort'])
    _whole_time = 0
    for i, v in enumerate(_sort_list):
        if v['name'].startswith('tbl_Avatar_'):
            _whole_time += v['sort']

    print(_whole_time)

if __name__ == '__main__':
    main()

