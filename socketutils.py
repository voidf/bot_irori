import pyzipper
from io import BytesIO

def zip_msg(msg: str):
    BB = BytesIO()
    with pyzipper.AESZipFile(
        BB, 'w',
        compression=pyzipper.ZIP_LZMA,
        encryption=pyzipper.WZ_AES
    ) as zf:
        zf.setpassword(b'114514')
        zf.writestr('m', msg)
    BB.seek(0)
    return BB.read()

def unzip_msg(zipped: bytes):
    BB = BytesIO(zipped)
    # print(BB.read())
    # BB.seek(0)
    with pyzipper.AESZipFile(BB) as zf:
        zf.setpassword(b'114514')
        print(zf.read('m'))

# class Test(Document): 存文件
#     file = FileField()

# test = Test()
# image_bytes = open("path/to/image.png", "rb")
# test.file.put(image_bytes, content_type='image/png', filename='test123.png')
# test.save()

# Test.objects.as_pymongo()   # [{u'_id': ObjectId('5cdac41d992db9bfcaa870df'), u'file': ObjectId('5cdac419992db9bfcaa870dd')}]

# t = Test.objects.first()
# t.file              # <GridFSProxy: 5cdac419992db9bfcaa870dd>
# t.file.content_type     # 'image/png'
# t.file.filename         # 'test123.png'
# content = t.file.read()

from pydantic import BaseModel # 为了用json
from typing import *


class Content(BaseModel):
    pass

class Element(BaseModel):
    pass

class MessageChain(BaseModel):
    __root__: List[Element]

class SendMsgContent(Content):
    target: int
    messageChain: MessageChain

class MiraiReq(BaseModel):
    syncId: int
    command: str
    subCommand: str = None
    content: dict = {} #