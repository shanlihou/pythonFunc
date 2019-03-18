# coding:utf-8
import requests
import json
import tornado
import tornado.httpclient
import tornado.gen


@tornado.gen.coroutine
def elasticRequest(uri, callback, method='GET', data=None):
    http_client = tornado.httpclient.AsyncHTTPClient()
    req = tornado.httpclient.HTTPRequest(
        url=uri,
        method=method,
        body=data,

    )
    response = yield tornado.gen.Task(http_client.fetch, req)
    if response.error:
        print('ckz: elasticRequest error:', response.error)
    else:
        callback(response)


class Elastic(object):
    def init(self):
        headers = {}
        headers['Content-Type'] = 'application/json'
        data = '''{
  "mappings": {
    "person": {
      "properties": {
        "user": {
          "type": "text",
          "analyzer": "smartcn",
          "search_analyzer": "smartcn"
        },
        "title": {
          "type": "text",
          "analyzer": "smartcn",
          "search_analyzer": "smartcn"
        },
        "desc": {
          "type": "text",
          "analyzer": "smartcn",
          "search_analyzer": "smartcn"
        }
      }
    }
  }
}'''
        ret = requests.put(url='http://localhost:9200/accounts',
                           data=data, headers=headers)
        print(ret.text)

    def addDoc(self):
        data = {'user': '李四',
                'title': '工程师',
                'desc': '系统管理'}
        data = json.dumps(data)
        headers = {}
        headers['Content-Type'] = 'application/json'
        ret = requests.post(
            url='http://localhost:9200/accounts/person', data=data, headers=headers)
        print(ret.text)

    def getDoc(self):
        ret = requests.get(
            'http://localhost:9200/accounts/person/1?pretty=true')
        print(ret.text)

    def getAll(self):
        ret = requests.get(
            'http://localhost:9200/accounts/person/_search')
        print(ret.text)

    def search(self):
        data = {'query': {'match': {'desc': '系统'}},
                'size': 1
                }
        headers = {'Content-Type': 'application/json'}
        ret = requests.post(
            'http://localhost:9200/accounts/person/_search', headers=headers, data=data)
        print(ret.text)

    def setting(self):
        data = '{"index.blocks.read_only_allow_delete": null}'
        headers = {'Content-Type': 'application/json'}

        ret = requests.put(
            'http://127.0.0.1:9200/accounts/_settings', data=data, headers=headers)
        print(ret.text)

    def test(self):
        ret = requests.get('http://localhost:9200/_cat/indices?v')
        print(ret.text)

        ret = requests.put('http://localhost:9200/weather')
        print(ret.text)

        ret = requests.delete('http://localhost:9200/weather')
        print(ret.text)
        self.getAll()
        # self.init()
        # self.setting()
        # self.addDoc()


if __name__ == '__main__':
    ela = Elastic()
    ela.test()
