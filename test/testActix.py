import requests


class TestActix(object):
    def test(self):
        ret = requests.get('http://192.168.16.223:8080')
        print(ret.content)


def main():
    ta = TestActix()
    ta.test()


if __name__ == '__main__':
    main()
