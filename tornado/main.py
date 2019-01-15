# coding=utf-8
import tornado.ioloop
import time
import tornado.gen
import sched
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
        print('ckz: elasticRequest error:', response.error)
        print(response.body)
    else:
        callback(response)


class FriendSearchMixin(object):
    headers = {'Content-Type': 'application/json'}

    def __init__(self):
        self.ip = '192.168.16.67'
        self.port = 9200
        self.uriBase = 'http://' + self.ip + ':' + str(self.port)
        self.indexName = str(999) + '_friend'

    def initElastic(self):
        data = '''{
  "mappings": {
    "Avatar": {
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
}'''

        def func(*args):
            print(args)

        url = self.join(self.uriBase, self.indexName)
        print(url)
        elasticRequest(url, func, 'PUT', data, self.headers)
        
    def join(self, *args):
        return '/'.join(args)


if __name__ == "__main__":
    # test_run()
    fs = FriendSearchMixin()
    fs.initElastic()
    tornado.ioloop.IOLoop.current().start()
