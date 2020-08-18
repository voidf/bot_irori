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
    
with open('zh2morse.json','r') as f:
    z2m = json.load(f)

with open('morse2zh.json','r') as f:
    m2z = json.load(f)

k1 = """ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.:,;?='/!-_"()$&@"""
k2 = """.- -... -.-. -..
. ..-. --. ....
.. .--- -.- .-..
-- -. --- .--.
--.- .-. ... -
..- ...- .-- -..-
-.-- --..
----- .---- ..--- ...--
....- ..... -.... --...
---.. ----.
.-.-.- ---... --..-- -.-.-.
..--.. -...- .----. -..-.
-.-.-- -....- ..--.- .-..-.
-.--. -.--.-
...-..- .-... .--.-."""

a2m = dict(zip(k1,k2.split()))
m2a = dict(zip(k2.split(),k1))

def 转电码(*attrs,**kwargs):
    global z2m,a2m
    msg = ' '.join(attrs).upper()

    conf = re.findall('''SPLIT=(.*?) ''',msg)
    split_symbol = '/'
    print(conf)
    if not conf:
        conf = re.findall('''SPLIT=(.*?)$''',msg)
        print(conf)
        if conf:
            split_symbol = conf[0]
            for i in conf:
                msg = msg.replace(f'''SPLIT={i}''','')
    else:
        split_symbol = conf[0]
        for i in conf:
            msg = msg.replace(f'''SPLIT={i}''','')

    msg = msg.replace(' ','_')
    ans = []
    cmsg = msg
    for i in msg:
        if i in z2m:
            cmsg = cmsg.replace(i,'_'+z2m[i]+'_')
        elif i not in z2m and i not in a2m:
            return [Plain(f'不合法的字符：{i}')]
    # while '  ' in cmsg:
    #     cmsg = cmsg.replace('  ',' ')

    for i in cmsg:
        ans.append(a2m[i])
    
    return [Plain(split_symbol.join(ans))]

def 译电码(*attrs,**kwargs):
    global m2a
    msg = ' '.join(attrs).upper()

    conf = re.findall('''SPLIT=(.*?) ''',msg)
    split_symbol = '/'
    print(conf)
    if not conf:
        conf = re.findall('''SPLIT=(.*?)$''',msg)
        print(conf)
        if conf:
            split_symbol = conf[0]
            for i in conf:
                msg = msg.replace(f'''SPLIT={i}''','')
    else:
        split_symbol = conf[0]
        for i in conf:
            msg = msg.replace(f'''SPLIT={i}''','')
    
    msg = msg.replace(' ','')
    ans = []
    for i in msg.split(split_symbol):
        if i not in m2a:
            return [Plain(f'不合法的电码：{i}')]
        ans.append(m2a[i])
    return [Plain(''.join(ans))]

def 译中文电码(*attrs,**kwargs):
    global m2z
    msg = ' '.join(attrs).upper()

    conf = re.findall('''SPLIT=(.*?) ''',msg)
    split_symbol = '_'
    print(conf)
    if not conf:
        conf = re.findall('''SPLIT=(.*?)$''',msg)
        print(conf)
        if conf:
            split_symbol = conf[0]
            for i in conf:
                msg = msg.replace(f'''SPLIT={i}''','')
    else:
        split_symbol = conf[0]
        for i in conf:
            msg = msg.replace(f'''SPLIT={i}''','')
    
    msg = msg.replace(' ','')
    ans = []
    for i in msg.split(split_symbol):
        if i:
            if i not in m2z:
                ans.append(i)
            else:
                ans.append(m2z[i])
    return [Plain(''.join(ans))]


StringMap = {
    '#BV':BVCoder,
    '#b64e':编码base64,
    '#b64d':解码base64,
    '#rot13':rot_13,
    '#rev':字符串反转,
    '#qr':二维码生成器,
    '#digest':字符串签名,
    '#a2m':转电码,
    '#m2a':译电码,
    '#m2z':译中文电码
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
''',
    '#a2m':
'''
将输入字符转为morse电码
如存在中文则依据《标准电码本》转换成四位数字编码
空格会被转换成下划线
可以指定分隔符,用例:
    #a2m 1145141919810 931 split=?
    使用问号作为字符串"1145141919810 931"的morse电码分隔符
''',
    '#m2a':
'''
将输入morse电码转换成明文
可以指定分隔符,用例:
    #m2a -.--/---/..-/-.-/---/.../--- split=/
    使用/作为电码"-.--/---/..-/-.-/---/.../---"的分隔符
''',
    '#m2z':
'''
将输入数字电码转换成中文
可以指定分隔符,用例:
    #m2z _7093__2448__5530__5358_ split=_
    使用/作为电码"_7093__2448__5530__5358_"的分隔符
''',
}
