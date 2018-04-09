import sys
import urllib2
import re
import time
import os
from ListPath import ListPath
import threading
from myUpdate import myUpdate
import sixteen
import string
import platform
import datetime
sysstr = platform.system()
if sysstr == 'Windows':
    import winsound
def BEEP():
    now = datetime.datetime.now()
    print now.strftime('%H:%M:%S')
    if sysstr == 'Windows':
        winsound.Beep(2300, 2000)
class CgiUtil(object):
    def __init__(self, name, pwd, url=None, path=None):
        self.name = name
        self.pwd = pwd
        self.url = url
        self.path = path
        #self.filename = self.findBin()
    
    def GET(self, url):
        p = urllib2.HTTPPasswordMgrWithDefaultRealm()
        p.add_password(None, url, self.name, self.pwd)
        handler = urllib2.HTTPDigestAuthHandler(p)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        resp = urllib2.urlopen(url, timeout = 120).read()
        return resp
    def findBin(self):
        listPath = ListPath(self.path)
        l = listPath.getAllFile()
        binList = filter(lambda x:x.endswith('.bin'), l)
        return filter(lambda x:os.path.basename(x).find('EngItl') != -1, binList)[0]
    def getState(self, data):
        pat = re.compile('State=(\w+)')
        find = pat.search(data)
        state = ''
        if find:
            state = find.group(1)
        ProgressStr = 'Progress='
        start = data.find(ProgressStr)
        end = start + len(ProgressStr) + 1
        print start
        if start != -1:
            return state, ord(data[start + len(ProgressStr)])
        else:
            return state, None
    def testUpdate(self):
        self.filename = self.findBin()
        p = urllib2.HTTPPasswordMgrWithDefaultRealm()
        p.add_password(None, self.url, self.name, self.pwd)
        handler = urllib2.HTTPDigestAuthHandler(p)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
                
        boundary = '----------%d' % int(time.time() * 1000)
        data = []
        data.append('--%s' % boundary)
        
        with open(self.filename, 'rb') as fr:
            data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('upgrade', 'update.bin'))
            data.append('Content-Type: application/octet-stream\r\n')
            data.append(fr.read())
            data.append('--%s--\r\n' % boundary)
        http_body='\r\n'.join(data)
        try:
            #buld http request
            req = urllib2.Request(self.url, data=http_body)
            #header
            req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
            req.add_header('User-Agent','Mozilla/5.0')
            #post data to server
            resp = urllib2.urlopen(req, timeout=60)
            #get response
            ret = resp.read()
            print ret
        except Exception,e:
            print 'http error'
            print e
    def saveResult(self, name, data):
        fw = open(name, 'w')
        fw.write(data)
    def printNow(self):
        now = datetime.datetime.now()
        print now.strftime('%H:%M:%S')
    def savePhoto(self, data):
        strJpeg = 'Content-Type: image/jpeg'
        strEnd = '\r\n\r\n'
        patternLen = re.compile(r'Content-Length:\s*(\d+)')
        index = 0
        id = 0
        while(1):
            index = data.find(strJpeg, index)
            if index == -1:
                break
            
            #sixteen.printDataIn16(data[index:index + len(strJpeg) + 2])
            find = patternLen.search(data[index:index + 200])
            length = 0
            if find:
                length = string.atoi(find.group(1))
            start = data.find(strEnd, index) + len(strEnd)
            jpgData = data[start:start + length]
            with open('d:\\snap%d.jpg' % id, 'wb') as fw:
                fw.write(jpgData)
                id += 1
            index += len(strJpeg)
            print 'len:', len(jpgData), length
            if len(jpgData) != length:
                self.printNow()
                BEEP()
                1 / 0
        if id < 2:
            self.printNow()
            print 'id not enough'
            BEEP()
            1 / 0
            

def alwaysGetState(args):
    cgiTest = CgiUtil('admin', 'admin123', 'http://' + alwaysGetState.url + '/cgi-bin/upgrader.cgi?action=uploadFirmware',
                       r'Y:\lj\IP3519\Dist')
    
    while(1):
        try:
            result = cgiTest.GET('http://' + alwaysGetState.url + '/cgi-bin/upgrader.cgi?action=getState')
            ret = cgiTest.getState(result)
            print ret
            if ret[1] == 100:
                pass
        except Exception, e:
            print 'failed'
            print e
        finally:
            time.sleep(1)
if __name__ == '__main__':
    innerHost = '172.29.4.134'
    if sys.argv[1] == '0':
        host = sys.argv[3]
        '''
        cgiTest = CgiUtil('admin', 'admin123', 'http://172.29.4.134/cgi-bin/upgrader.cgi?action=uploadFirmware', r'Y:\lj\IP3519\Dist')
        cgiTest.testUpdate()
        print cgiTest.findBin()
        print cgiTest.GET('http://172.29.4.134/cgi-bin/upgrader.cgi?action=getState')
        '''
        if len(sys.argv) == 4:
            up = myUpdate(path=sys.argv[2], host=host)
        else:
            up = myUpdate(path=sys.argv[2], host=host, name=sys.argv[4], pwd=sys.argv[5])
            
        up.test()
    elif sys.argv[1] == '1':
        host = sys.argv[3]
        alwaysGetState.url = host
        t = threading.Thread(target=alwaysGetState, args=None)
        t.start()
        while(1):
            try:
                up = myUpdate(filename=sys.argv[2], host=host)
                up.test()
            except Exception, e:
                print e
            finally:
                print time.localtime()  
                time.sleep(120)  
                print time.localtime()
    #rain brush  
    elif sys.argv[1] == '2':
        innerHost = sys.argv[2]
        url = '/cgi-bin/rainBrush.cgi?action=moveOnce&channel=1'
        cgiTest = CgiUtil('admin', 'admin123')
        count = 0
        errCnt = 0
        while(1):
            try:
                result = cgiTest.GET('http://' + innerHost + url)
                if result.startswith('OK'):
                    print 'success:', result
                else:
                    print 'failed:', result
                count += 1
                cgiTest.printNow()
            except Exception, e:
                print e
                errCnt += 1
                BEEP()
                #break
            finally:
                print count, errCnt
                time.sleep(5)
    elif sys.argv[1] == '3':
        cgiTest = CgiUtil('admin', 'admin123', 'http://' + '172.29.4.134' + '/cgi-bin/upgrader.cgi?action=uploadFirmware',
                           r'Y:\IPCHisilicon\Dist')
        cgiTest.testUpdate()
    elif sys.argv[1] == '4':
        cgiTest = CgiUtil('admin', 'admin123')
        #fr = open('d:\\response.txt', 'rb')
        #cgiTest.savePhoto(fr.read())
        
        url = '/cgi-bin/snapManager.cgi?action=attachFileProc&Flags[0]=Event&Events=[All]&heartbeat=5'
        result = cgiTest.GET('http://' + innerHost + url)
        cgiTest.savePhoto(result)
        index = 0
        while 1:
            try:
                result = cgiTest.GET('http://' + innerHost + url)
            except Exception, e:
                BEEP()
                break
            cgiTest.savePhoto(result)
            index += 1
            print 'index:', index
        #save the response for the test
        #fw = open('d:\\response.txt', 'wb')
        #fw.write(result)
        
        