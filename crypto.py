"""
This Source is part of QiRub Project

Make Sure you use the latest version of QiRub, for
More info you can visit our github, also you can access
To new News, Updates, Bug Fixes, ... with github

Github: https://github.com/Rubier-Project/QiRub

"""

import base64,Crypto.Util.Padding,Crypto.Hash
from Crypto.Cipher import AES
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA 

class encryption:
  def __init__(self, auth:str, private_key:str=None):
    self.auth = auth
    self.key = bytearray(self.secret(auth), "UTF-8")
    self.iv = bytearray.fromhex('00000000000000000000000000000000')
    self.keypair = RSA.import_key("-----BEGIN PRIVATE KEY-----\n"+private_key+"\n-----END PRIVATE KEY-----") if private_key else None

  def change(auth_enc):
        return ''.join([chr(((32 - (ord(s) - 97)) % 26) + 97) if s.islower() else chr(((29 - (ord(s) - 65)) % 26) + 65) if s.isupper() else chr(((13 - (ord(s) - 48)) % 10) + 48) if s.isdigit() else s for s in auth_enc])
  def secret(self, e):
        return ''.join([chr((ord(char) - ord('0') + 5) % 10 + ord('0')) if char.isdigit() else chr((ord(char) - ord('a') + 9) % 26 + ord('a')) for char in (e[16:24] + e[0:8] + e[24:32] + e[8:16])])
  def encrypt(self, text):
        return base64.b64encode(AES.new(self.key, AES.MODE_CBC, self.iv).encrypt(Crypto.Util.Padding.pad(text.encode('UTF-8'), AES.block_size))).decode('UTF-8')
  def decrypt(self, text):
        return Crypto.Util.Padding.unpad(AES.new(self.key, AES.MODE_CBC, self.iv).decrypt(base64.urlsafe_b64decode(text.encode('UTF-8'))), AES.block_size).decode('UTF-8')
  def Sign(self, data_enc:str):
        return base64.b64encode(pkcs1_15.new(self.keypair).sign(Crypto.Hash.SHA256.new(data_enc.encode("utf-8")))).decode("utf-8")
  def decryptRsaOaep(private:str,data_enc:str):
        return Crypto.Cipher.PKCS1_OAEP.new(RSA.import_key(private.encode("utf-8"))).decrypt(base64.b64decode(data_enc)).decode("utf-8")
  def rsaKey():
       Grt = RSA.generate(1024)
       return encryption.change(base64.b64encode(Grt.publickey().export_key()).decode("utf-8")),Grt.export_key().decode("utf-8")
  def auth_decrypt(key):
       return ''.join([chr(((13 - (ord(s) - 48)) % 10) + 48) if s.isdigit() else chr(((32 - (ord(s) - 97)) % 26) + 97) if s.islower() else chr(((29 - (ord(s) - 65)) % 26) + 65) if s.isupper() else s for s in key])
