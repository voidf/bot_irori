from mirai import Mirai, Plain, MessageChain, Friend, Face, MessageChain,Group,Image,Member,At
from mirai.face import QQFaces
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
import GLOBAL
import importlib
shortMap = {}
functionMap = {}
functionDescript = {}
Classes = {}

GLOBAL.randomStrLength = 4
GLOBAL.webPngLimit = int(1e6)
GLOBAL.CaLimit = 1e13
GLOBAL.CbLimit = 1e5
GLOBAL.revTag = chr(8238)
GLOBAL.pingCtr = 0


import Utils
importlib.reload(Utils)
from Utils import *


try:
    with open('hakushinAVG.txt','r') as jfr:
        GLOBAL.AVGHost = jfr.readline().strip()
        GLOBAL.AVGPort = int(jfr.readline().strip())
        
except Exception as e:
    print(e)
    GLOBAL.AVGHost = ''
    GLOBAL.AVGPort = 0


def printHelp(*attrs,**kwargs):
    l = []
    img = []
    ext = []
    if not attrs:
        l.append('命令分类：')
        l.append('\tAVG 正在开发的文字冒险游戏类')
        l.append('\tGame 小游戏类')
        l.append('\tString 字符串处理类')
        l.append('\tFile 异步与文件读写类')
        l.append('\tSpider 爬虫类')
        l.append('\tTest 测试类（开发用')
        l.append('\tGenerator 生成器类')
        l.append('\tTranslate 翻译类')
        l.append('\tMath 数学类')
        l.append('输入#h <类名> 以查询分类下命令')
        l.append('使用#h <命令名> 可以查询详细用法')
        l.append('尖括号表示参数必要，方括号表示参数可选，实际使用')
        l.append('使用#h #abb可以查询缩写表')
    else:
        if attrs[0] in shortMap:
            attrs = [shortMap[attrs[0]],*attrs[1:]]
        if attrs[0] in functionDescript:
            l.append(functionDescript[attrs[0]])

        elif attrs[0] in ('all','old'):
            l.append('可用命令表：')
            for k in functionMap:
                l.append('\t'+k)
            l.append('使用#h 命令名（带井号）可以查询详细用法')
            l.append('使用#h #abb可以查询缩写表')
            l.append('注命令后需打空格，之后的参数如存在空格即以空格分开多个参数，如#qr 1 1 4 5 1 4')
            img.append(Image.fromFileSystem('muzukashi.png'))
        elif attrs[0] in Classes:
            l.append(f'分类：{attrs[0]}')
            for k in Classes[attrs[0]]:
                l.append(f'''\t{k}\t{functionDescript[k].strip()[:10] if len(functionDescript[k].strip()[:10])<=10 else functionDescript[k].strip()[:10]+'...'}\n''' )
        else:
            l.append('【错误】参数不合法\n')
            ext = printHelp()
        
    return [Plain('\n'.join(l))] + img + ext


"""
AVG用
"""
import AVG
importlib.reload(AVG)
from AVG import *
functionDescript.update(AVGDescript)
functionMap.update(AVGMap)
shortMap.update(AVGShort)
"""
待改游戏类
"""
import Game
importlib.reload(Game)
from Game import *
functionDescript.update(GameDescript)
functionMap.update(GameMap)
shortMap.update(GameShort)
"""
字符串处理类
"""
import String
importlib.reload(String)
from String import *
functionDescript.update(StringDescript)
functionMap.update(StringMap)
shortMap.update(StringShort)

"""
异步与文件读写类
"""
import File
importlib.reload(File)
from File import *
functionDescript.update(FileDescript)
functionMap.update(FileMap)
shortMap.update(FileShort)
"""
爬虫类（chromeNMSL）
"""
import Spider
importlib.reload(Spider)
from Spider import *
functionDescript.update(SpiderDescript)
functionMap.update(SpiderMap)
shortMap.update(SpiderShort)

"""
测试函数类（危）
"""
import Test
importlib.reload(Test)
from Test import *
functionDescript.update(TestDescript)
functionMap.update(TestMap)
shortMap.update(TestShort)

"""
生成器类
"""
import Generator
importlib.reload(Generator)
from Generator import *
functionDescript.update(GeneratorDescript)
functionMap.update(GeneratorMap)
shortMap.update(GeneratorShort)

"""
翻译类 from fufu
"""
import Translate
importlib.reload(Translate)
from Translate import *
functionDescript.update(TranslateDescript)
functionMap.update(TranslateMap)
shortMap.update(TranslateShort)
"""
数学类：
CalC        - 计算组合数
CalA        - 计算排列数
CalKatalan  - 计算卡特兰数
"""
import Math
importlib.reload(Math)
from Math import *
functionDescript.update(MathDescript)
functionMap.update(MathMap)
shortMap.update(MathShort)



Classes = {
    'Math':MathMap,
    'Generator':GeneratorMap,
    'Test':TestMap,
    'String':StringMap,
    'Spider':SpiderMap,
    'Translate':TranslateMap,
    'File':FileMap,
    'Game':GameMap,
    'AVG':AVGMap,
}

functionMap['#h'] = printHelp

functionDescript['#h'] = '不传参打印命令表，传参则解释命令'
functionDescript['#abb'] = f'可用缩写表:{shortMap}'

print('Callable LOAD DONE =========>')
