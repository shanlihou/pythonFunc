from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import traceback
import urllib.request
import sys 
import http
import json
	
def post(url, data):
	header = {}
	header["X-Bmob-Application-Id"] = "f959535a39bb9dec9ac4dab32e5961c5"
	header["X-Bmob-REST-API-Key"] = "17342bb32e2df845778bb70391b1c4a6"
	header["Content-Type"] = "application/json"

	opener = urllib.request.build_opener()
	opener.addheaders = [(k, v) for k,v in header.items()]
	print(opener.addheaders)
	req = ''
	print(type(opener))
	try:
		req = opener.open(url, data=data)
		print(req)
		print(req.reason)
	except OSError:
		print(traceback.format_exc())
	return req.read().decode()

def addPubKey(pubkey):
	url = "https://api.bmob.cn/1/classes/pubKey"
	jsonData = {}
	jsonData["pubKey"] = pubkey
	sendData = json.dumps(jsonData);
	print(sendData)
	return post(url, sendData.encode())

def createPem():
	key = RSA.generate(1024)
	print(key.publickey().exportKey('PEM').decode().replace('\n', ''))
	ret = addPubKey(key.publickey().exportKey('PEM').decode())
	jsonRet = json.loads(ret)
	print('ret')
	print(jsonRet)
	print(jsonRet['objectId'])
	objectId = jsonRet['objectId']

	private = open(objectId + '.pri.pem', 'wb')
	private.write(key.exportKey('PEM'))
	private.close()
	public = open(objectId + '.pub.pem', 'wb')
	public.write(key.publickey().exportKey('PEM'))
	public.close()
def importKey():
	public = open('public.pem', 'rb')
	private = open('private.pem', 'rb')
	pub = RSA.importKey(public.read())
	pri = RSA.importKey(private.read())
	pubN = PKCS1_v1_5.new(pub)
	priN = PKCS1_v1_5.new(pri)
	secret = pubN.encrypt('410015216'.encode())
	mess = priN.decrypt(secret, None)
	print(mess)
def decrypt(secret):
	private = open('private.pem', 'rb')
	pri = RSA.importKey(private.read())
	priN = PKCS1_v1_5.new(pri)
	mess = priN.decrypt(secret, None)
	print(mess)
if (len(sys.argv) == 2):
	if (sys.argv[1] == '-c'):
		createPem()
	elif(sys.argv[1] == '-p'):
		post("https://api.bmob.cn/1/classes/userInfo", '{"score":1337,"playerName":"Sean Plott","cheatMode":false}'.encode())
