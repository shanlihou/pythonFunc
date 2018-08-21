import requests
import ssl
class videoQuery(object):
    def __init__(self):
        print(ssl.OPENSSL_VERSION)
        
        ret = requests.get('https://www.souka.ml/q/no=ISKF-006')
        print(ret.text)
        '''
        send_headers = {'Host':'btso.pw','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3053.3 Safari/537.36','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Connection':'keep-alive', 'Accept-Encoding':'gzip, deflate, sdch, br', 'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6'}
        req = urllib2.Request('https://www.souka.ml/q/no=ISKF-006', headers=send_headers)
        resp = urllib2.urlopen(req)
        html = resp.read()
        if resp.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(html)
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
            print(data)'''
        
if __name__ == '__main__':
    vq = videoQuery()