import requests
import json
import rsa
import base64
class BMOB(object):
    def __init__(self):
        self.appId = 'f959535a39bb9dec9ac4dab32e5961c5'
        self.apiKey = '17342bb32e2df845778bb70391b1c4a6'
        self.base = 'https://api.bmob.cn/1/classes/'
        self.saveFile = 'testSave'
        self.loadPriKey('pri_191be71fff.pem')
        
    def getHeaders(self):
        return {'X-Bmob-Application-Id': self.appId,
                'X-Bmob-REST-API-Key': self.apiKey}
        
    def saveContent(self, data):
        with open(self.saveFile, 'w') as fw:
            fw.write(data)
    
    def get(self, table):
        headers = self.getHeaders()
        url = self.base + table
        ret = requests.get(url, headers=headers)
        self.saveContent(ret.text)
        return ret.text
        
    def getSaveContent(self):
        with open(self.saveFile) as fr:
            return fr.read()
    
    def loadPriKey(self, keyFile):
        with open(keyFile) as fr:
            pri_data = fr.read()
            self.priKey = rsa.PrivateKey._load_pkcs1_pem(pri_data)
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
        #ret = self.get('userInfo')
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
        
    
    def test(self):
        self.readUserInfo()
if __name__ == '__main__':
    bmob = BMOB()
    bmob.test()