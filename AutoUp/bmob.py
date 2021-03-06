import requests
import json
import rsa
import base64
import os


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class BMOB(object):
    def __init__(self):
        self.appId = 'f959535a39bb9dec9ac4dab32e5961c5'
        self.apiKey = '17342bb32e2df845778bb70391b1c4a6'
        self.base = 'https://api.bmob.cn/1/classes/'
        self.saveFile = 'testSave'
        self.loadPriKey('pri_191be71fff.pem')
        self.loadPubKey()

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
                r'E:\shgithub\python\pythonFunc\bmob', keyFile)
        with open(keyFile) as fr:
            pri_data = fr.read()
            self.priKey = rsa.PrivateKey._load_pkcs1_pem(pri_data)

    def loadPubKey(self):
        ret = self.get('pubKey', True)
        retDict = json.loads(ret)
        pubKey = retDict['results'][0]['pubKey']
        self.pubKey = rsa.PublicKey.load_pkcs1_openssl_pem(pubKey)

    def encrypt(self, data):
        data = data.encode('utf-8')
        return base64.b64encode(rsa.encrypt(data, self.pubKey)).decode('utf-8')

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
        requests.post(url, headers=headers, data=data)

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
        self.addMyPwd('123', '456', '789')


if __name__ == '__main__':
    BMOB().test()
