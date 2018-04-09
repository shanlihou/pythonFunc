import sys
import urllib2
import re
def storage(url):
    user = 'admin'
    passwd = 'admin'
    p = urllib2.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, url, user, passwd)
    handler = urllib2.HTTPDigestAuthHandler(p)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    resp = urllib2.urlopen(url).read()
    return resp
def test():
    urlBase = 'http://172.29.4.132'
    url = urlBase + '/cgi-bin/mediaFileFind.cgi?action=factory.create'
    pat = re.compile(r'=(\d+)')
    resp = storage(url)
    ret = pat.search(resp)
    if (ret):
        num = ret.group(1)
        print (num)
        url2 = urlBase + '/cgi-bin/mediaFileFind.cgi?action=findFile&object=' + num + '&condition.Channel=0&condition.StartTime=2016-12-11%2000:00:00&condition.EndTime=2016-12-11%2023:59:00&condition.Dirs[0]=/mnt/sd&condition.Types[0]=jpg&condition.Flag[0]=Timing'
        url3 = urlBase + '/cgi-bin/mediaFileFind.cgi?action=findNextFile&object=' + num + '&count=10000'
        url4 = urlBase + '/cgi-bin/mediaFileFind.cgi?action=close&object=' + num
        resp = storage(url2)
        print resp
        resp = storage(url3)
        print resp
        resp = storage(url4)
        print resp
print len(sys.argv)
if len(sys.argv) == 1:
    test()
elif len(sys.argv) == 2:
    while True:
        test()
        
for i in sys.argv:
    print i