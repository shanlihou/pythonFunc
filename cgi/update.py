import hashlib
import socket
import re
import time
import os
class auth:
    def __init__(self, name, realm, pwd, method, nonce, nc, cnonce, qop, uri):
        self.name = name
        self.realm = realm
        self.pwd = pwd
        self.method = method
        self.nonce = nonce
        self.nc = nc
        self.cnonce = cnonce
        self.qop = qop
        self.uri = uri
    def getA1(self):
        a1 = hashlib.md5()
        a1.update(self.name + ':')
        a1.update(self.realm + ':')
        a1.update(self.pwd)
        return a1.hexdigest()
    def getA2(self):
        a2 = hashlib.md5()
        a2.update(self.method + ":")
        a2.update(self.uri)
        return a2.hexdigest()
    def getResult(self):
        a1 = self.getA1()
        a2 = self.getA2()
        result = hashlib.md5()
        result.update(a1 + ':')
        result.update(self.nonce + ':')
        result.update(self.nc + ':')
        result.update(self.cnonce + ':')
        result.update(self.qop + ':')
        result.update(a2)
        return result.hexdigest()
    
class myUpdate(object):
    def __init__(self, path, host='172.29.4.133', port=80, name='admin', pwd='admin123'):
        self.host = host
        self.port = port
        self.name = name
        self.pwd = pwd
        self.method = 'POST'
        self.nc = '00000001'
        self.cnonce = '1a86a38e3de985c8'
        self.uri = '/cgi-bin/upgrader.cgi?action=uploadFirmware'
        self.filename = path
    '''
    def findBin(self):
        listPath = ListPath(self.path)
        l = listPath.getAllFile()
        binList = filter(lambda x:x.endswith('.bin'), l)
        return filter(lambda x:os.path.basename(x).find('Chn_PN') != -1, binList)[0]
    '''
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
    def getInfo(self, data):
        pat = re.compile(r'(\w+)="([^"]+)"')
        ret = pat.findall(data)
        info = {}
        for i in ret:
            info[i[0]] = i[1]
        return info
    def getBody(self):
        self.timeStamp = int(time.time() * 1000)
        self.boundary = '----------%d' % self.timeStamp
        data = []
        data.append('--%s' % self.boundary)
        
        fr=open(self.filename,'rb')
        data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('upgrade', 'update.bin'))
        data.append('Content-Type: application/octet-stream\r\n')
        data.append(fr.read())
        fr.close()
        data.append('--%s--\r\n' % self.boundary)
        http_body='\r\n'.join(data)
        return http_body
    def getEnc(self):
        enc = auth(self.name, self.info['realm'], self.pwd, self.method, self.info['nonce'], self.nc, self.cnonce, self.info['qop'], self.uri)
        #print enc.getResult()
        return enc.getResult()
    def post(self):
        self.msg = ['POST /cgi-bin/upgrader.cgi?action=uploadFirmware HTTP/1.1',
                    'Accept-Encoding: identity',
                    'Content-Length: 5',
                    'Host: 172.29.4.133',
                    'Content-Type: multipart/form-data; boundary=----------1512527708035',
                    'Connection: close',
                    'User-Agent: Mozilla/5.0\r\n\r\n']
        sendMsg = '\r\n'.join(self.msg)
        sendMsg += 'a' * 5
        self.sock.sendall(sendMsg)
        reply = self.sock.recv(4096)
        print reply
        self.info = self.getInfo(reply)
        self.sock.close()
    def sendSlow(self):
        length = len(self.sendMsg)
        hasSend = 0
        block = 1024 * 64
        while 1:
            if hasSend + block >= length:
                self.sock.sendall(self.sendMsg[hasSend:length])
                break
            else:
                print hasSend
                self.sock.sendall(self.sendMsg[hasSend:hasSend + block])
                hasSend += block
            time.sleep(1)
    def post2(self):
        result = self.getEnc()
        body = self.getBody()
        length = len(body)
        self.msg = ['POST /cgi-bin/upgrader.cgi?action=uploadFirmware HTTP/1.1',
                    'Accept-Encoding: identity',
                    'Content-Length: ' + str(length),
                    'Host: 172.29.4.133',
                    'Content-Type: multipart/form-data; boundary=----------%d' % self.timeStamp,
                    'Connection: close',
                    'User-Agent: Mozilla/5.0']
        self.msg.append('''Authorization: Digest username="%s", \
realm="%s", \
nonce="%s", \
uri="%s", \
response="%s", \
opaque="%s", \
algorithm="MD5", \
qop=auth, \
nc=%s, \
cnonce="%s"\r\n\r\n''' % (self.name, 
                          self.info['realm'], 
                          self.info['nonce'], 
                          self.uri, 
                          result, 
                          self.info['opaque'], 
                          self.nc,
                          self.cnonce))
        sendMsg = '\r\n'.join(self.msg)
        self.sock.sendall(sendMsg)
        self.sendMsg = body
        self.sendSlow()
    def test(self):
        self.connect()
        self.post()
        self.connect()
        self.post2()
if __name__ == '__main__':
    up = myUpdate(r'Y:\svn\s2lm_conditions\Dist\20171204\DH_IPC-HX5X2X-Themis_Chn_PN_Stream3_V2.620.0000001.0.R.171204\DH_IPC-HX5X2X-Themis_Chn_PN_Stream3_V2.620.0000001.0.R.171204.bin')
    up.test()