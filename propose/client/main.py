# coding:utf-8
import requests
import json
if __name__ == '__main__':
    url = 'http://127.0.0.1:8000/cmd/'
    headers = {'Content-Type': 'application/json'}
    data = {"cmd": "coco", "act": 0, "data": "你好", "duration": 5, "dir": 3}
    data = json.dumps(data)
    print(data)
    requests.post(url, headers=headers, data=data)
