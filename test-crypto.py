from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import base64

public_key = RSA.import_key(open('pub.pem', 'rb').read())
data = open('requirements.txt', 'rb').read()

signature = base64.b64decode(open('signature.txt', 'rb').read())

pkcs1_15.new(public_key).verify(SHA256.new(data), signature)
