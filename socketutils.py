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

from dataclasses import dataclass
from typing import *

@dataclass
class Task():
    player: int
    sender: int
    raw: str