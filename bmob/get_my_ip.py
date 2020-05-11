#!/usr/bin/python3
#-*-coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json
from bmob import BMOB
import logging


class GetMyIp(object):
    def __init__(self, *args, **kwargs):
        pass

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        ret = soup.find_all('span', class_='cf-footer-item')
        for span in ret:
            if 'Your IP:' in span.text:
                return self.get_ip(span.text)

    def get_ip(self):
        ret = requests.get('http://jsonip.com')
        json_obj = json.loads(ret.content.decode('ascii'))
        return json_obj['ip']

    def save_html(self, html):
        with open('tmp.html', 'wb') as fw:
            fw.write(html)

    def get_html(self):
        with open('tmp.html', 'rb') as fr:
            return fr.read()

    def send_ip_to_bmob(self):
        logging.info('start get')
        ip = self.get_ip()
        logging.info('get ip:{}'.format(ip))
        data = json.dumps({'ip': BMOB().encrypt(ip)})
        BMOB().putData('019785abb1', 'rasp_ip', data)
        # self.save_html(ret.content)
        #ret = self.get_html()
        #ip = self.parse_html(ret)
        # print(ip)

    def test(self):
        ret = BMOB().get('rasp_ip')
        ret = json.loads(ret)
        for data in ret['results']:
            print(BMOB().decrypt(data['ip']))


if __name__ == '__main__':
    gmi = GetMyIp()
    gmi.test()
