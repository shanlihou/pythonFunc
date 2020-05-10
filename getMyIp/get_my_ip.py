#-*-coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json

class GetMyIp(object):
    def __init__(self, *args, **kwargs):
        pass
    
    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        ret = soup.find_all('span', class_='cf-footer-item')
        for span in ret:
            if 'Your IP:' in span.text:
                return self.get_ip(span.text)
    
    def get_ip(self, data):
        ret = requests.get('http://jsonip.com')
        json_obj = json.loads(ret.content.decode('ascii'))
        return json_obj['ip']
    
    def save_html(self, html):
        with open('tmp.html', 'wb') as fw:
            fw.write(html)
            
    def get_html(self):
        with open('tmp.html', 'rb') as fr:
            return fr.read()
        
    def test(self):
        ret = requests.get('http://jsonip.com')
        json_obj = json.loads(ret.content.decode('ascii'))
        return json_obj['ip']
        #self.save_html(ret.content)
        #ret = self.get_html()
        #ip = self.parse_html(ret)
        #print(ip)
        

if __name__ == '__main__':
    gmi = GetMyIp()
    gmi.test()
    