from mirai import Mirai, Plain, MessageChain, Friend, Face, MessageChain,Group,Image,Member,At
from mirai.face import QQFaces
from bs4 import BeautifulSoup
from PIL import ImageFont,ImageDraw
from PIL import Image as PImage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import asyncio
import requests
import json5
import json
import numpy
import random
import os
import base64
import qrcode
import io
import string
import math
import urllib
import copy
import ctypes
import functools
import traceback
import http.client
import statistics
import csv
import hashlib
import zlib
import time
import datetime
import urllib
import mido
import GLOBAL
from Utils import *

def BVCoder(*attrs,**kwargs):
    def dec(x):
        r=0
        for i in range(6):
            r+=tr[x[s[i]]]*58**i
        return (r-add)^xor

    def enc(x):
        x=(x^xor)+add
        r=list('BV1  4 1 7  ')
        for i in range(6):
            r[s[i]]=table[x//58**i%58]
        return ''.join(r)
    table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr={}
    for i in range(58):
        tr[table[i]]=i
    s=[11,10,3,8,4,6]
    xor=177451812
    add=8728348608
    try:
        try:
            ostr = [Plain(text=enc(int(i))+'\n') for i in attrs]
        except:
            ostr = [Plain(text='av'+str(dec(i))+'\n') for i in attrs]
    except Exception as e:
        ostr = [Plain(text=str(e))]
    return ostr
        
def 编码base64(*attrs,**kwargs):
    try:
        return [Plain(text=str(base64.b64encode(bytes(i,'utf-8')))+'\n') for i in attrs]
    except Exception as e:
        return [Plain(text=str(e))]

def 解码base64(*attrs,**kwargs):
    try:
        return [Plain(text=str(base64.b64decode(i))+'\n') for i in attrs]
    except Exception as e:
        return [Plain(text=str(e))]

def rot_13(*attrs,**kwargs):
    upperdict = {'A': 'N', 'B': 'O', 'C': 'P', 'D': 'Q', 'E': 'R', 'F': 'S', 'G': 'T', 'H': 'U', 'I': 'V', 'J': 'W', 'K': 'X', 'L': 'Y',
			 'M': 'Z', 'N': 'A', 'O': 'B', 'P': 'C', 'Q': 'D', 'R': 'E', 'S': 'F', 'T': 'G', 'U': 'H', 'V': 'I', 'W': 'J', 'X': 'K', 'Y': 'L', 'Z': 'M'}

    lowerdict = {'a': 'n', 'b': 'o', 'c': 'p', 'd': 'q', 'e': 'r', 'f': 's', 'g': 't', 'h': 'u', 'i': 'v', 'j': 'w', 'k': 'x', 'l': 'y',
                'm': 'z', 'n': 'a', 'o': 'b', 'p': 'c', 'q': 'd', 'r': 'e', 's': 'f', 't': 'g', 'u': 'h', 'v': 'i', 'w': 'j', 'x': 'k', 'y': 'l', 'z': 'm'}
    ostr = []
    for j in attrs:
        dst=[]
        for i in j:
            if i in upperdict:
                dst.append(upperdict[i])
            elif i in lowerdict:
                dst.append(lowerdict[i])
            else:
                dst.append(i)
        ostr.append(Plain(text=''.join(dst)+'\n'))
    return ostr

def 字符串反转(*attrs,**kwargs):
    return [Plain(text=' '.join(attrs)[::-1])]

def 二维码生成器(*attrs,**kwargs):
    s = ' '.join(attrs)
    q = qrcode.make(s)
    fn = randstr(GLOBAL.randomStrLength)+'tmpqrcode'+str(kwargs['mem'].id)
    q.save(fn)
    #threading.Thread(target=rmTmpFile).start()
    asyncio.ensure_future(rmTmpFile(fn),loop=None)
    return [Image.fromFileSystem(fn)]

def 字符串签名(*attrs,**kwargs):
    if 'pic' in kwargs and kwargs['pic']:
        src = requests.get(kwargs['pic'].url).content
    elif attrs:
        src = bytes(' '.join(attrs),'utf-8')
    else:
        return [Plain('没法处理空串哦！')]
    return [
        Plain(f"MD5:{hashlib.md5(src).hexdigest()}\n"),
        Plain(f"SHA1:{hashlib.sha1(src).hexdigest()}\n"),
        Plain(f"SHA256:{hashlib.sha256(src).hexdigest()}\n"),
        Plain(f"CRC32:{hex(zlib.crc32(src))}\n")
        ]
    
StringMap = {
    '#BV':BVCoder,
    '#b64e':编码base64,
    '#b64d':解码base64,
    '#rot13':rot_13,
    '#rev':字符串反转,
    '#qr':二维码生成器,
    '#digest':字符串签名
}

StringShort = {}

StringDescript = {
    '#b64e':'base64编码,例：#b64e mirai',
    '#b64d':'base64解码,例：#b64d 114514==',
    '#rot13':'rot_13编码转换（仅大小写ascii字母）',
    '#qr':'将输入字符串专为二维码,例:#qr mirai',
    '#rev':'字符串反转，例:#rev mirai',
    '#digest':'传入字符串则计算字符串的md5，sha1，sha256，crc32，如传入图片则只处理第一张图片，例:#digest 1145141919810',
    '#BV':
'''
格式：
    #BV <BV号，需带BV两个字>
    即返回av号
    #BV <av号,纯数字，不带av两个字>
    即返回BV号
'''
}
