import hashlib
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