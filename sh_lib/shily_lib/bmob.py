# coding:utf-8
import requests
import json
import rsa
import base64
import os
import logging
import sys

if sys.platform == 'win32':
    logname = 'bmob.log'
else:
    if os.path.exists(r'/home/pi'):
        logname = '/home/pi/shlog/bmob.log'
    else:
        logname = 'bmob.log'

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
    datefmt='%Y-%m-%d %A %H:%M:%S',
    filename=logname,
    filemode='a+')


def singleton(cls):
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class BMOB(object):
    def __init__(self, userInfo, priKey, pubKey):
        json_data = json.load(open(userInfo))
        self.appId = json_data['app_id']
        self.apiKey = json_data['api_key']
        self.base = 'https://api.bmob.cn/1/classes/'
        self.saveFile = 'testSave'
        if not priKey:
            priKey = 'pri_191be71fff.pem'
        
        if not pubKey:
            pubKey = 'pub_191be71fff.pem'
        self.loadPriKey(priKey)
        self.loadPubKey(pubKey)

    def getHeaders(self):
        return {'X-Bmob-Application-Id': self.appId,
                'X-Bmob-REST-API-Key': self.apiKey}

    def saveContent(self, data):
        with open(self.saveFile, 'w') as fw:
            fw.write(data)

    def get(self, table, isSave=False):
        headers = self.getHeaders()
        url = self.base + table
        ret = requests.get(url, headers=headers)
        if isSave:
            self.saveContent(ret.text)
        return ret.text

    def getSaveContent(self):
        with open(self.saveFile) as fr:
            return fr.read()

    def loadPriKey(self, keyFile):
        if not os.path.exists(keyFile):
            keyFile = os.path.join(
                sys.path[0], keyFile)
        with open(keyFile) as fr:
            pri_data = fr.read()
            self.priKey = rsa.PrivateKey._load_pkcs1_pem(pri_data)

    def loadPubKey(self, keyFile=''):
        if keyFile and os.path.exists(keyFile):
            with open(keyFile) as fr:
                pub_data = fr.read()
                self.pubKey = rsa.PublicKey.load_pkcs1_openssl_pem(pub_data)
                return

        ret = self.get('pubKey', True)
        retDict = json.loads(ret)
        pubKey = retDict['results'][0]['pubKey']
        self.pubKey = rsa.PublicKey.load_pkcs1_openssl_pem(pubKey)

    def big_enc(self, data):
        json_str = json.dumps(data)
        length = len(json_str)
        end = 0
        enc_list = []
        while end < length:
            _end = min(length, end + 117)
            enc_str = self.encrypt(json_str[end:_end])
            enc_list.append(enc_str)
            end = _end

        return '889914'.join(enc_list)

    def big_dec(self, data):
        datas = data.split('889914')
        datas = (self.decrypt(i) for i in datas)
        return ''.join(datas)

    def encrypt(self, data):
        data = data.encode('utf-8')
        enc_data = rsa.encrypt(data, self.pubKey)
        return base64.b64encode(enc_data).decode('utf-8')

    def decrypt(self, data):
        data = base64.b64decode(data.encode('utf-8'))
        ret = rsa.decrypt(data, self.priKey)
        ret = ret.decode('utf8')
        return ret

    def testRsa(self, data):
        with open('pri_191be71fff.pem') as fr:
            pri_data = fr.read()
            priKey = rsa.PrivateKey._load_pkcs1_pem(pri_data)
            data = base64.b64decode(data.encode('utf-8'))

            ret = rsa.decrypt(data, priKey)
            print(ret)

    def readUserInfo(self):
        # ret = self.get('userInfo')
        ret = self.getSaveContent()
        retDict = json.loads(ret)
        results = retDict['results']
        self.userDict = {}
        for userInfo in results:
            name = self.decrypt(userInfo['name'])
            passwd = self.decrypt(userInfo['pass'])
            self.userDict[name] = passwd

        for name, passwd in self.userDict.items():
            print(name, passwd)

    def addData(self, table, data):
        headers = self.getHeaders()
        headers['Content-Type'] = 'application/json'
        url = self.base + table
        ret = requests.post(url, headers=headers, data=data)
        logging.info('add data content:{}'.format(ret.content))
        return ret.content

    def putData(self, objId, table, data):
        headers = self.getHeaders()
        headers['Content-Type'] = 'application/json'
        url = self.base + table + '/' + objId
        requests.put(url, headers=headers, data=data)

    def deleteData(self, table, objId):
        headers = self.getHeaders()
        url = self.base + table + '/' + objId
        requests.delete(url, headers=headers)

    def test(self):
        ret = self.getSaveContent()
        ret = json.loads(ret)['results']
        dic = {}
        for i in ret:
            name = i['name']
            passwd = i['pass']
            dic[self.decrypt(name)] = self.decrypt(passwd)

        for k,v in dic.items():
            print(k, v)


if __name__ == '__main__':
    pri_name = os.path.join('secret', 'pri_191be71fff.pem')
    pub_name = os.path.join('secret', 'pub_191be71fff.pem')
    BMOB(pri_name, pub_name)
    BMOB().test()
