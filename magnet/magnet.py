import urllib2 
import urllib
import re
import sys
import gzip
from StringIO import StringIO
URIBASE = 'btsow.casa'
HEADERS = {'Host': URIBASE,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3053.3 Safari/537.36','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Connection':'keep-alive', 'Accept-Encoding':'gzip, deflate, sdch, br', 'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6'}


def getUrlList(urlPath):
    print(urlPath)
    req = urllib2.Request(urlPath, headers=HEADERS)
    resp = urllib2.urlopen(req)
    html = resp.read()
    print(resp.info())
    if resp.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(html)
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
        pattern = re.compile(r'https://{}/magnet/detail/hash/[A-F0-9]+'.format(URIBASE))
        patFind = pattern.search(data)
        if (patFind):
            matchList = pattern.findall(data)
            return matchList
    return None

def getMagnet(urlPath):
    req = urllib2.Request(urlPath, headers=HEADERS)
    resp = urllib2.urlopen(req)
    html = resp.read()
    if resp.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(html)
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
        pattern = re.compile(r'(magnet:\?xt=urn:btih:[^"\']+)" class=')
        patFind = pattern.search(data)
        if (patFind):
            return patFind.group(1)

def getAllMagnet(code):
    #code=urllib.quote_plus(code)
    print(code)
    code = urllib.quote(code.decode(sys.stdin.encoding).encode('utf8'))  
    List = getUrlList('https://{}/search/{}'.format(URIBASE, code))
    listFlag = []
    magList = []
    if (List != None):
        for url in List:
            sameFlag = 0
            for i in listFlag:
                if (url == i):
                    sameFlag = 1
                    break;
            if (sameFlag == 1):
                continue
            listFlag.append(url)
            magList.append(getMagnet(url))
    return magList

if (len(sys.argv) == 2):
    getAllMagnet(sys.argv[1])
