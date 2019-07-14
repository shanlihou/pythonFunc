import requests

if __name__ == '__main__':
    ret = requests.get('http://big-chat.com/olivia_innocent/')
    online = 'Room is currently offline' not in ret.text