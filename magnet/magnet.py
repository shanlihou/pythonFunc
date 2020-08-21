# coding= utf-8
import requests
from bs4 import BeautifulSoup
import urllib
import re
import sys
import gzip
URIBASE = 'btsow.casa'
HEADERS = {'Host': URIBASE, 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3053.3 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate, sdch, br', 'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'}


def save_file(data):
    with open('one.html', 'w', encoding='utf-8') as fw:
        fw.write(data)


def get_save(fn=None):
    if not fn:
        fn = 'test.html'
    with open(fn, 'r', encoding='utf-8') as fr:
        return fr.read()


def get_content(urlPath, is_save=False):
    ret = requests.get(urlPath, headers=HEADERS)
    html = ret.text
    if is_save:
        save_file(html)
    return html


class BtOne(object):
    def __init__(self, url, size):
        content = get_content(url, True)
#         content = get_save('one.html')
        self.mag = self.parse_mag(content)
        self.size = size

    def __str__(self):
        return '{},{}'.format(self.mag, self.size)

    def parse_mag(self, content):
        pat = re.compile(r'(magnet:\?xt=urn:btih:[^"><]+)["<>]')
        ret = pat.findall(content)
        return ret[0]


def parse_content(content):
    pat = re.compile('(https://.+magnet[^"]+)"')
    ret = pat.findall(content)
    soup = BeautifulSoup(content, "html.parser")
    div = soup.select('div[class="data-list"]')
    for _div in div:
        for ret in _div.select('div[class="row"]'):
            a = ret.select('a')[0]
            n_div = a.find_next_siblings('div')[0]
            yield BtOne(a['href'], n_div.string)
#     for url in ret:
#         #bo = BtOne(url)


def getAllMagnet(code):
    # code=urllib.quote_plus(code)
    print(code)
    code = urllib.parse.quote(code)
    url = 'https://{}/search/{}'.format(URIBASE, code)
    content = get_content(url, True)
    for bo in parse_content(content):
        print(bo)


if __name__ == '__main__':
    #     parse_content(get_save())
    #     bo = BtOne(1)
    getAllMagnet('复仇者')
#     if (len(sys.argv) == 2):
#         getAllMagnet(sys.argv[1])
