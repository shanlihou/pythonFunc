# coding=utf-8
import tornado.ioloop
import time
import tornado.gen
import sched
import json
# from tornado import gen
from tornado.httpclient import AsyncHTTPClient
import threading


@tornado.gen.coroutine
def elasticRequest(uri, callback, method='GET', data=None, headers=None):
    http_client = tornado.httpclient.AsyncHTTPClient()
    req = tornado.httpclient.HTTPRequest(
        url=uri,
        method=method,
        body=data,
        headers=headers
    )
    response = yield tornado.gen.Task(http_client.fetch, req)
    if response.error:
        data = response.body.decode('utf-8')
        jsonData = json.loads(data)
        root_cause = jsonData.get('error', {}).get('root_cause', [])
        for cause in root_cause:
            if cause['type'] == 'resource_already_exists_exception':
                return
        print('ckz: elasticRequest error:', response.error, uri)
        print(response.body)

    else:
        callback(response)


class FriendSearchMixin(object):
    headers = {'Content-Type': 'application/json'}

    def __init__(self):
        self.ip = '192.168.16.252'
        self.port = 9200
        self.uriBase = 'http://' + self.ip + ':' + str(self.port)
        self.indexName = str(10272) + '_friend'
        self.typeName = 'Avatar'

    def cat(self):
        url = self.join(self.uriBase, '_cat/indices?v')

        def func(resp):
            print(resp.body.decode('utf-8'))
        elasticRequest(url, func)

    def setting(self):
        data = '{"index.blocks.read_only_allow_delete": null}'
        uri = self.join(self.uriBase, self.indexName, '_settings')

        def func(resp):
            print(resp.body)
        print(uri)
        elasticRequest(uri, func, 'PUT', data, self.headers)

    def delete(self, dbId):
        uri = self.join(self.uriBase, self.indexName, self.typeName, str(dbId))

        def func(resp):
            print('delete------------------------------------')
            print(resp.body)
        print(uri)
        elasticRequest(uri, func, 'DELETE')

    def addAvatarInfo(self, name, gbId, id):
        data = {'name': name,
                'gbId': gbId}

        data = json.dumps(data)
        uri = self.join(self.uriBase, self.indexName, self.typeName, str(id))

        def func(response):
            print('add:', response.body)
        elasticRequest(uri, func, 'PUT', data, self.headers)

    def initElastic(self):
        data = '''{
  "mappings": {
    "%s": {
      "properties": {
        "name": {
          "type": "text",
          "analyzer": "smartcn",
          "search_analyzer": "smartcn"
        },
        "gbId": {
          "type": "long"
        }
      }
    }
  }
}''' % self.typeName

        def func(*args):
            print(args)

        uri = self.join(self.uriBase, self.indexName)
        print(uri)
        elasticRequest(uri, func, 'PUT', data, self.headers)

    def indexObId(self, obId):
        uri = self.join(self.uriBase, self.indexName,
                        self.typeName, str(obId)) + '?pretty=true'

        def _func(resp):
            data = resp.body.decode('utf-8')
            jsonData = json.loads(data)
            print(jsonData)
            print(jsonData['_source'])
        elasticRequest(uri, _func)
        
    def getAll(self):
        uri = self.join(self.uriBase, self.indexName, self.typeName, '_search')

        def func(resp):
            print('-' * 60)
            body = resp.body.decode('utf-8')
            body = json.loads(body)
            for data in body['hits']['hits']:
                print(data)
        print(uri)
        elasticRequest(uri, func, 'GET')

    def searchAvatarName(self, name):
        for i in name:
            print(ord(i))
        data = {'query': {'match': {'name': name}},
                'size': 100
                }
        data = json.dumps(data)
        uri = self.join(self.uriBase, self.indexName, self.typeName, '_search')

        def func(resp):
            body = resp.body.decode('utf-8')
            jsonData = json.loads(body)
            hits = jsonData['hits']['hits']
            print(hits)
            for data in hits:
                print(data)
                source = data['_source']
                print(source, data['_id'])

        elasticRequest(uri, func, 'POST', data, self.headers)

    def join(self, *args):
        return '/'.join(args)

    def test(self):
        self.initElastic()
        # self.setting()
        # self.cat()
        # self.addAvatarInfo('包青一天大旧人', 2299822224)
        self.searchAvatarName('血色')
        self.indexObId(8423432)
        self.delete(557056)
        self.getAll()


if __name__ == "__main__":
    # test_run()
    fs = FriendSearchMixin()
    fs.test()
    tornado.ioloop.IOLoop.current().start()
