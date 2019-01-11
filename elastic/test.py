# coding:utf-8
import requests
import json


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
        self.getDoc()
        # self.init()
        # self.setting()
        # self.addDoc()


if __name__ == '__main__':
    ela = Elastic()
    ela.test()
