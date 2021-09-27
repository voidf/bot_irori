import requests
from basicutils.algorithms import *
import basicutils.CONST as GLOBAL
from typing import *
from basicutils.task import *

def BaiduTTS(text: str) -> str:
    """拿百度TTS的链接"""
    return f'http://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&spd=5&text={text}'

# def generateTmpFile(b: bytes, fm='png') -> str:
#     """生成一个30s后会删掉的临时文件"""
#     fn = generateTmpFileName(ext=f'.{fm}')
#     with open(fn, 'wb') as f:
#         f.write(b)
#     asyncio.ensure_future(rmTmpFile(fn))
#     return fn


def generateTmpFileName(pref='', ext='.png', **kwargs):
    """生成一个临时文件名"""
    return f'''tmp{pref}{randstr(GLOBAL.randomStrLength)}{ext}'''


def getFileBytes(s):
    if isinstance(s, bytes):
        return s
    elif s[:4] == 'http':
        ret = requests.get(s).content
        print(len(ret))
        return ret
    else:
        with open(s, 'rb') as f:
            return f.read()

import requests
def convert_to_amr(typ: str, lnk: Union[bytes, str], mode: int=0):
    if isinstance(lnk, str):
        ret = requests.post(
            server_api(f'/convert/amr?format={typ}&mode={mode}'),
            data={'lnk': lnk}
        ).json()['url']
    else:
        ret = requests.post(
            server_api(f'/convert/amr?format={typ}&mode={mode}'),
            files={'f': BytesIO(lnk)}
        ).json()['url']
    return server_api('/worker/oss/'+ret)

def convert_file_to_amr(typ: str, fp, mode: int=0):
    ret = requests.post(
        server_api(f'/convert/amr?format={typ}&mode={mode}'),
        files={'f': open(fp,'rb')}
    ).json()['url']
    return server_api('/worker/oss/'+ret)
import base64
from PIL import Image as PImage
def pimg_base64(img: PImage.Image) -> str:
    bio = BytesIO()
    img.save(bio, format='PNG')
    bio.seek(0)
    return base64.b64encode(bio.read()).decode('utf-8')