#!/usr/bin/env python
# --coding:utf-8 --

from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib.parse import urlparse
<<<<<<< HEAD
import sqlite3
=======
import json
>>>>>>> 14be24449c420070e505c3c80ccec8393f7e7650

DB_PATH = '~/shgithub/python/ios_spider/crawler.sqlite3.db'
curdir = path.dirname(path.realpath(__file__))
sep = '/'

# MIME-TYPE
mimedic = [
    ('.html', 'text/html'),
    ('.htm', 'text/html'),
    ('.js', 'application/javascript'),
    ('.css', 'text/css'),
    ('.json', 'application/json'),
    ('.png', 'image/png'),
    ('.jpg', 'image/jpeg'),
    ('.gif', 'image/gif'),
    ('.txt', 'text/plain'),
    ('.avi', 'video/x-msvideo'),
]

def get_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    c = cursor.execute('select * from JAVBUS_DATA')
    for row in c:
        print(row)
        break
    cursor.close()
    conn.close()

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        querypath = urlparse(self.path)
        filepath, _ = querypath.path, querypath.query
        print(filepath, _)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write('{"hello": 123}'.encode('utf-8'))

    def do_POST(self):
        print(self.headers)
        print(self.command)
        req_datas = self.rfile.read(
            int(self.headers['content-length']))  # 重点在此步!
        print(req_datas.decode())
        data = {
            'result_code': '2',
            'result_desc': 'Success',
            'timestamp': '',
            'data': {'message_id': '25d55ad283aa400af464c76d713c07ad'}
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def _do_GET_(self):
        sendReply = False
        querypath = urlparse(self.path)
        filepath, _ = querypath.path, querypath.query

        if filepath.endswith('/'):
            filepath += 'index.html'
        _, fileext = path.splitext(filepath)
        for e in mimedic:
            if e[0] == fileext:
                mimetype = e[1]
                sendReply = True

        if sendReply:
            try:
                with open(path.realpath(curdir + sep + filepath), 'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(content)
            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)


def run():
    get_data()
    port = 8000
    print('starting server, port', port)

    # Server settings
    server_address = ('', port)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
