import GLOBAL
from bs4 import BeautifulSoup
from PIL import ImageFont,ImageDraw
from PIL import Image as PImage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from Utils import *
importMirai()
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
from functools import wraps
import traceback
import http.client
import statistics
import csv
import hashlib
import zlib
import time
import datetime

def smart_decorator(decorator):
    def decorator_proxy(func=None, **kwargs):
        if func is not None:
            return decorator(func=func, **kwargs)
        def decorator_proxy(func):
            return decorator(func=func, **kwargs)
        return decorator_proxy
    return decorator_proxy

def check_host(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if GLOBAL.OJHost:
            return func(*args, **kwargs)
        else:
            return [Plain('没有配置OJ后端主机！')]
    return decorator

def requester(lnk,kw,tle=5,**kwargs):
    r = requests.post(f"{GLOBAL.OJHost}/{lnk}",json=kw,timeout=tle)
    j = json.loads(r.text)
    if not j['status']:
        print(j)
        asyncio.ensure_future(msgDistributer(msg=f"【错误】封装器里炸了：{j['msg']}",typ='P',**kwargs))
        raise NameError('【异常】总之请求炸了')
    return j

@check_host
def 查看问题(*attrs,**kwargs):
    data = {'problem_id':attrs[0]}
    rsp = requester('problem/info',data)['data']['problem']
    samples = f'样例输入{p}：{chr(10)}{i}{chr(10)}样例输出{p}：{chr(10)}{rsp["sample_outputs"][p]}{chr(10)}{chr(10)}' for p,i in enumerate(rsp['sample_inputs'])
    render = f"""
{rsp['title']}
{rsp['pdf']}
问题描述：
    {rsp['description']}


{chr(10).join(samples)}

时间限制：{rsp['time_limit']}s
内存限制：{rsp['memory_limit']}kb"""
    return [Plain(render)]

@check_host
def 提交(*attrs,**kwargs):
    player = getPlayer(**kwargs)
    data = {
        'problem_id':attrs[0],
        'qq':str(player),
        'lang':attrs[1],
        'file':' '.join(attrs[2:])
    }
    rsp = requester('submit', data)['data']['result']
    cases = (f'{p}  {i} {rsp["runtime"][p]/1000}ms {rsp["memory"][p]/1000}kb' for p,i in enumerate(rsp['verdict']))
    render = f"""
测试点  状态    时间    内存
{chr(10).join(cases)}

"""
    if rsp['score'] == 100:
        ext = '太您了！'
    elif rsp['score'] >= 80:
        ext = '加把劲（'
    elif rsp['score'] >= 40:
        ext = '再优化一下？'
    else:
        ext = '就这？'
    return [Plain(render+ext)]

OJMap = {
    "#OJ.info":查看问题,
    "#OJ.submit":提交,
}

OJShort = {
    "^info": "#OJ.info",
    "^submit": "#OJ.submit",
}

OJDescript = {
    "#OJ.info":"传入欲查看的问题的id，返回问题信息",
    "#OJ.submit":"""想交题了？
用法：
    #OJ.submit <题号> <语言> <代码...

由于是自己搭的开源灵车，语言目前只支持：
    gcc     (还没测试过)
    gccO2   (还没测试过)
    g++     (测试过了)
    g++O2   (还没测试过)
    python3 (还没搭好)
""",
}