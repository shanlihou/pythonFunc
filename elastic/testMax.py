import requests
import time


def main():
    url = 'http://192.168.16.252:9200/20004_friend/Avatar/559108?pretty=true'
    ret = requests.get(url)
    print(ret.content)
    while(1):
        time.sleep(5)


if __name__ == '__main__':
    main()
