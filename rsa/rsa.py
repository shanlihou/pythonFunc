from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import traceback
import urllib.request
import sys 
import http
def createPem():
	key = RSA.generate(1024)
	print(key.publickey().exportKey('PEM'))
	private = open('private.pem', 'wb')
	private.write(key.exportKey('PEM'))
	private.close()
	public = open('public.pem', 'wb')
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
def post(url, data):
	header = {}
	header["X-Bmob-Application-Id"] = "f959535a39bb9dec9ac4dab32e5961c5"
	header["X-Bmob-REST-API-Key"] = "17342bb32e2df845778bb70391b1c4a6"
	header["Content-Type"] = "application/json"
	print(header)

	opener = urllib.request.build_opener()
	opener.addheaders =  [(k, v) for k,v in header.items()]
	req = ''
	try:
		req = opener.open(url)
		print(req.read())
	except OSError:
		print(traceback.format_exc())
post('https://api.bmob.cn/1/classes/pubkey', '{"pubkey":"1235215355"}'.encode())
post('https://www.baidu.com', '{"pubkey":"1235215355"}'.encode())
	
