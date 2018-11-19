import json
import requests


class Poster(object):
    def __init__(self, url):
        self.url = url

    def post(self, data):
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(data)
        requests.post(self.url, headers=headers, data=data)
