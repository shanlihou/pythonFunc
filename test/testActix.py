import requests
import json

class TestActix(object):
    def test(self):
        dic = {
            'jsonrpc': '2.0',
            'method': 'search',
            'params': [],
            'id': 1
            }
        json_str = json.dumps(dic)
        ret = requests.post('http://192.168.16.223:8080', data=json_str)
        print(ret.content)


def main():
    ta = TestActix()
    ta.test()


if __name__ == '__main__':
    main()
