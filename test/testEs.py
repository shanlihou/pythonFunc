import requests
import base64

URI_BASE = 'http://{}:{}'.format('192.168.16.252', 9200)
ori = 'elastic:123456'
authB64 = base64.b64encode(bytes(ori, 'ascii'))
INDEX = '20217_friend_ik'


class EsTest(object):
    headers = {
        'Authorization': 'Basic %s' % authB64.decode('ascii')
    }

    def __init__(self):
        pass

    def getPluginInfo(self):
        url = '{}/{}/{}'.format(URI_BASE, '_cat', 'plugins')
        ret = requests.get(url, headers=self.headers)
        print(ret.text)

    def del_index(self):
        url = '{}/{}'.format(URI_BASE, INDEX)
        ret = requests.delete(url, headers=self.headers)
        print(ret.text)


def main():
    et = EsTest()
    et.del_index()


if __name__ == '__main__':
    main()
