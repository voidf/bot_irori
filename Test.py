import GLOBAL    
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
importMirai()

def 表情符号查询姬(*attrs,**kwargs):
    return [Plain(' '.join( [str(ord(i)) for i in ' '.join(attrs)] ))]

def Unicode测试姬(*attrs,**kwargs):
    s = int(attrs[0])
    e = int(attrs[1])
    s,e = min(s,e),max(s,e)
    w = ' '.join(attrs[2:])
    asyncio.ensure_future(fuzzT(kwargs['gp'],s,e,w))


def 表情字典测试姬(*attrs,**kwargs):
    return [Face(QQFaces[attrs[0]])]

    
def 乒乓球(*attrs,**kwargs):
    GLOBAL.pingCtr+=1
    if GLOBAL.pingCtr-1==0:
        s = 'pong'
    else:
        s = f'pong {GLOBAL.pingCtr}Xcombo'
    return [Plain(s)]

def 废话生成器(*attrs,**kwargs):
    return [Plain(' '.join(attrs[:-1])*int(attrs[-1]))]

def 重设渲染图片阈值(*attrs,**kwargs):
    player = getPlayer(**kwargs)
    tc = chkcfg(player)
    tc.compress_threshold = int(attrs[0])
    return [Plain(f'消息长度大于等于{attrs[0]}时转为图片发送')]
    

def 清空嗅探器(*attrs,**kwargs):
    player = getPlayer(**kwargs)
    tc = chkcfg(player)
    print('clearing')
    try:
        tc.quick_calls = {}
    except:
        print('可能是内存里没有这个嗅探器引起的：')
        print(traceback.format_exc())
    if not os.path.exists(f'sniffer/{player}'):
        return [Plain('没有储存sniffer，无需清空')]
    else:
        os.remove(f'sniffer/{player}')
        return [Plain('已清除sniffer')]

def 同步嗅探器(*attrs,**kwargs):
    if 'player' in kwargs:
        player = kwargs['player']
    else:
        player = getPlayer(**kwargs)
    tc = chkcfg(player)
    if not os.path.exists(f'sniffer/{player}'):
        try:
            tc.quick_calls = {}
        except:
            print(traceback.format_exc())
        return [Plain('同步完毕，没有活动的嗅探器')]
    else:
        with open(f'sniffer/{player}','r') as f:
            j = json.load(f)
        tc.quick_calls = j
    return [Plain(f'同步完毕，现有{len(tc.quick_calls)}个已经激活的嗅探器')]


TestMap = {
    '#fuzz':Unicode测试姬,
    '#EMJ':表情字典测试姬,
    '#ping':乒乓球,
    '#废话':废话生成器,
    '#echo':表情符号查询姬,
    '#lim':重设渲染图片阈值,
    r'%clear':清空嗅探器,
    r'%sync':同步嗅探器
}

TestShort = {

}

TestDescript = {
    '#fuzz':
"""
【测试用】基本上是用来测试unicode的
用法：
    #fuzz <起始unicode码> <终止unicode码> <额外输出字符>
""",
    '#lim':'设置返回的消息长度大于等于多少时,转换为图片发送',
    '#echo':'查询当前字符串的unicode码',
    '#EMJ':'测试mirai自带表情字典，例:#EMJ kuaikule',
    '#ping':'基本上是用来测试bot有没有在线的。无聊加了个计数应该不会被pwn吧（',
    '#废话':'【测试用】复读某个字符串，一开始是为测量消息最大长度而设计，目前已知私聊字符串最大长度876，群聊32767.用法#废话 <复读字符串> <复读次数>',
    r'%clear':'【嗅探器】清空本群的所有嗅探器',
    r'%sync':'【嗅探器】从文件同步本群的嗅探器'
}
