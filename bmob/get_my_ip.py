#!/usr/bin/python3
#-*-coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json
from bmob import BMOB
import logging
import pickle
import time


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

    def get_bmob_ip(self):
        try:
            ret = BMOB().get('rasp_ip')
        except Exception as e:
            return ''

        ret = json.loads(ret)
        for data in ret['results']:
            return BMOB().decrypt(data['ip'])

        return ''

    def get_local_ip(self):
        return pickle.load(open('myconfig', 'rb'))

    def save_local_ip(self, ip):
        pickle.dump(ip, open('myconfig', 'wb'))

    def test(self):
        ip = self.get_bmob_ip()
        if ip:
            self.save_local_ip(ip)
            print(ip)
        else:
            print(self.get_local_ip())

    def run(self):
        while 1:
            self.send_ip_to_bmob()
            time.sleep(120)

if __name__ == '__main__':
    gmi = GetMyIp()
    gmi.run()
