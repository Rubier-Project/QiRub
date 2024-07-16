"""
This Source is part of QiRub Project

Make Sure you use the latest version of QiRub, for
More info you can visit our github, also you can access
To new News, Updates, Bug Fixes, ... with github

Github: https://github.com/Rubier-Project/QiRub

"""

import httpx
import random
import fake_useragent
import json

from .crypto import encryption

class ProxyType(object):
    ...

class QiStream(object):
    def choiceObject(items: list = []):
        return random.choice(items)
    
    def randomIntSteram() -> int:
        return random.randint(100000, 999999999)
    
    def randomStrStream() -> str:
        return str(random.randint(-99999999, 99999999))
    
    def deviceHashGenerator() -> str:
        return "".join(random.choices("0123456789", k=26))

class QiNetwork(object):
    def __init__(self, AuthToken: str, PrivateKey: str, Proxy: ProxyType = None):
        self.auth = AuthToken
        self.key = PrivateKey
        self.proxy = Proxy
        self.agent = fake_useragent.UserAgent().random

        self.enc = encryption(self.auth, self.key)
        
        self.newAuth = encryption.change(self.auth)
        
        self.client = {
            "app_name": "Main",
            "app_version": "3.5.7",
            "lang_code": "fa",
            "package": "app.rbmain.a",
            "temp_code": "27",
            "platform": "Android"
        }
        
        self.apis = [
            "https://messengerg2c2.iranlms.ir",
            "https://messengerg2c3.iranlms.ir"
        ]

        self.selectedApi = QiStream.choiceObject(self.apis)
    
    def option(self,
               input_data: dict,
               method: str,
               use_fake_useragent: bool = True
               ):
        
        data = json.dumps({
            "input": input_data,
            "method": method,
            "client": self.client
        })

        encs = self.enc.encrypt(data)
        sig = self.enc.Sign(encs)

        notData = json.dumps({
            "api_version": "6",
            "auth": self.newAuth,
            "sign": sig,
            "data_enc": encs
        })

        heads = {"User-Agent": self.agent, "Referer": "https://rubika.ir"} if use_fake_useragent else {"Referer": "https://rubika.ir"}

        net = httpx.Client(proxy=self.proxy)

        try:
            data = json.loads(self.enc.decrypt(json.loads(net.post(self.selectedApi, data=notData, headers=heads).text)['data_enc']))
            return data
        except Exception as ERROR_QI:
            return str(ERROR_QI)
