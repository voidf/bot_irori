import GLOBAL
from bs4 import BeautifulSoup
import quine_mccluskey.qmccluskey
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
import importlib
shorts = {}
funs = {}
desc = {}

pluginfuns = {}

GLOBAL.randomStrLength = 4
GLOBAL.webPngLimit = int(1e6)
GLOBAL.CaLimit = 1e13
GLOBAL.CbLimit = 1e5
GLOBAL.revTag = chr(8238)
GLOBAL.pingCtr = 0


import Utils
importlib.reload(Utils)
from Utils import *
importMirai()

pluginsdir = 'plugins'
plugindocs = {}

for plugin in os.listdir(pluginsdir):
    pkgname = os.path.splitext(plugin)[0]
    if pkgname == '__pycache__': continue
    print(f'importing {plugin}')
    module = importlib.import_module(pluginsdir+'.'+pkgname)
    importlib.reload(module)
    names = module.__dict__.get("__all__", [x for x in module.__dict__ if x[:1] != '_'])
    globals().update({k: getattr(module, k) for k in names})
    pluginfuns[pkgname] = getattr(module, "functionMap")
    funs.update(getattr(module, "functionMap"))
    shorts.update(getattr(module, "shortMap"))
    desc.update(getattr(module, "functionDescript"))
    plugindocs[pkgname] = module.__doc__

for k, v in list(desc.items()):
    if k not in funs:
        print(f'Unused description for {k}, remove it.')
        desc.pop(k)
    elif not funs[k].__doc__:
        funs[k].__doc__ = v

async def printHelp(*attrs,**kwargs):
    l = []
    img = []
    ext = []
    if not attrs:
        l.append('已导入的模块：')
        for k, v in plugindocs.items():
            l.append(f'''\t{k} {v}''')
        l.append('输入#h <类名> 以查询模块下命令')
        l.append('使用#h <命令名> 可以查询详细用法')
        l.append('尖括号表示参数必要，方括号表示参数可选，实际使用中不必一定需要')
        l.append('使用#h #abb可以查询缩写表')
    else:
        if attrs[0] in shorts:
            attrs = [shorts[attrs[0]],*attrs[1:]]
        if attrs[0] in desc:
            l.append(desc[attrs[0]])

        elif attrs[0] in ('all', 'old'):
            l.append('可用命令表：')
            for k in funs:
                l.append('\t'+k)
            l.append('使用#h 命令名（带井号）可以查询详细用法')
            l.append('使用#h #abb可以查询缩写表')
            l.append('注命令后需打空格，之后的参数如存在空格即以空格分开多个参数，如#qr 1 1 4 5 1 4')
            img.append(generateImageFromFile('Assets/muzukashi.png'))
        elif attrs[0] in pluginfuns:
            l.append(f'分类：{attrs[0]}')
            for k in pluginfuns[attrs[0]]:
                print(f'descLen = {len(desc[k].strip()[:20])}')
                l.append(f'''\t{k}\t{desc[k].strip()[:20] 
                if len(desc[k].strip()[:20])<=20
                else desc[k].strip()[:20]+'...'}\n''' )
        else:
            l.append('【错误】参数不合法\n')
            ext = printHelp()
        
    return [Plain('\n'.join(l))] + img + ext


funs['#h'] = printHelp
desc['#h'] = '不传参打印命令表，传参则解释命令'
desc['#abb'] = f'可用缩写表:{shorts}'

print('Callable LOAD DONE =========>')
