import requests
from basicutils.algorithms import *
import basicutils.CONST as GLOBAL

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