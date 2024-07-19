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
import filetype

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
        self.agent = fake_useragent.UserAgent()

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
    
    def checkLink(self, link: str):
        if link.startswith("http://") or link.startswith("https://"):
            return True
        else:
            return False
    
    def getMimeFromByte(self, bytes: bytes):
        mime = filetype.guess(bytes)
        return "qirubika" if mime is None else mime.extension
    
    def generateFileName(self, mime: str):
        return "QiRubika_{}.{}".format(random.randint(1, 100000), mime)
    
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

        heads = {"User-Agent": self.agent.random, "Referer": "https://rubika.ir"} if use_fake_useragent else {"Referer": "https://rubika.ir"}

        net = httpx.Client(proxy=self.proxy)

        try:
            data = json.loads(self.enc.decrypt(json.loads(net.post(self.selectedApi, data=notData, headers=heads).text)['data_enc']))
            return data
        except Exception as ERROR_QI:
            return str(ERROR_QI)
        
    def RequestSendFile(self, file_name: str, mime: str, size: str):
        return self.option({"file_name": file_name, "mime": mime, "size": size}, "requestSendFile", True)

    def upload(self, file:str, fileName:str=None, chunkSize:int=131072):

        if isinstance(file, str):
            if file.startswith("http"):
                file:bytes = httpx.get(file).text 
                mime:str = self.getMimeFromByte(bytes=file)
                fileName = fileName or self.generateFileName(mime=mime)
            else:
                fileName = fileName or file
                mime = file.split(".")[-1]
                file = open(file, "rb").read()

        elif not isinstance(file, bytes):
            raise FileNotFoundError("Enter a valid path or url or bytes of file.")
        else:
            mime = self.getMimeFromByte(bytes=file)
            fileName = fileName or self.generateFileName(mime=mime)

        def send_chunk(data, maxAttempts=2):
            for attempt in range(maxAttempts):
                try:
                    response = httpx.post(
                        url=requestSendFileData["upload_url"],
                        headers=header,
                        data=data
                    )

                    return json.loads(response.text)
                except Exception:
                    print(f"\nError uploading file! (Attempt {attempt + 1}/{maxAttempts})")
            
            print("\nFailed to upload the file!")

        requestSendFileData:dict = self.RequestSendFile(
            file_name = fileName,
            mime = mime,
            size = len(file)
        )['data']

        header = {
            "auth": self.auth,
            "access-hash-send": requestSendFileData["access_hash_send"],
            "file-id": requestSendFileData["id"],
        }

        totalParts = (len(file) + chunkSize - 1) // chunkSize

        for partNumber in range(1, totalParts + 1):
            startIdx = (partNumber - 1) * chunkSize
            endIdx = min(startIdx + chunkSize, len(file))
            header["chunk-size"] = str(endIdx - startIdx)
            header["part-number"] = str(partNumber)
            header["total-part"] = str(totalParts)
            data = file[startIdx:endIdx]
            hashFileReceive = send_chunk(data)

            if not hashFileReceive:
                return
            
            if partNumber == totalParts:

                if not hashFileReceive["data"]:
                    return
                
                requestSendFileData["file"] = file
                requestSendFileData["access_hash_rec"] = hashFileReceive["data"]["access_hash_rec"]
                requestSendFileData["file_name"] = fileName
                requestSendFileData["mime"] = mime
                requestSendFileData["size"] = len(file)
                return requestSendFileData
