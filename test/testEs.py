import requests

URI_BASE = 'http://{}:{}'.format('192.168.16.223', 9200)


class EsTest(object):
    def __init__(self):
        pass

    def getPluginInfo(self):
        url = '{}/{}/{}'.format(URI_BASE, '_cat', 'plugins')
        ret = requests.get(url)
        print(ret.text)


def main():
    et = EsTest()
    et.getPluginInfo()


if __name__ == '__main__':
    main()
