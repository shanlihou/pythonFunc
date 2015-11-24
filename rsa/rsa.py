from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import sys 
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
createPem()
