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

def 表情符号查询姬(*attrs,**kwargs):
    return [Plain(' '.join( [str(ord(i)) for i in ' '.join(attrs)] ))]

def Unicode测试姬(*attrs,**kwargs):
    try:
        s = int(attrs[0])
        e = int(attrs[1])
        w = attrs[2]
        asyncio.ensure_future(fuzzT(kwargs['gp'],s,e,w))
    except Exception as e:
        return [Plain(str(e))]
    return []

def 表情字典测试姬(*attrs,**kwargs):
    try:
        return [Face(QQFaces[attrs[0]])]
    except Exception as e:
        return [Plain(str(e))]
    
def 乒乓球(*attrs,**kwargs):
    GLOBAL.pingCtr+=1
    if GLOBAL.pingCtr-1==0:
        s = 'pong'
    else:
        s = f'pong {GLOBAL.pingCtr}Xcombo'
    return [Plain(s)]

def 废话生成器(*attrs,**kwargs):
    return [Plain(' '.join(attrs[:-1])*int(attrs[-1]))]


TestMap = {
    '#fuzz':Unicode测试姬,
    '#EMJ':表情字典测试姬,
    '#ping':乒乓球,
    '#废话':废话生成器,
    '#echo':表情符号查询姬
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
    '#echo':'查询当前字符串的unicode码',
    '#EMJ':'【测试用】测试mirai自带表情字典，例:#EMJ kuaikule',
    '#ping':'【测试用】基本上是用来测试bot有没有在线的。无聊加了个计数应该不会被pwn吧（',
    '#废话':'【测试用】复读某个字符串，一开始是为测量消息最大长度而设计，目前已知私聊字符串最大长度876，群聊32767.用法#废话 <复读字符串> <复读次数>',
}
