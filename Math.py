from mirai import Mirai, Plain, MessageChain, Friend, Face, MessageChain,Group,Image,Member,At
from mirai.face import QQFaces
from bs4 import BeautifulSoup
from PIL import ImageFont,ImageDraw
from PIL import Image as PImage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import quine_mccluskey.qmccluskey
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



def CalC(*attrs,**kwargs):
    try:
        if len(attrs)==3:
            a,b=(int(i) for i in attrs[1:3])
            if a<b:
                a,b=b,a
            if a>GLOBAL.CaLimit or b>GLOBAL.CbLimit:
                return [Plain(text='太大了我放不下(>///<)')]
            c = 1
            for i in range(a-b,a):
                c*=i+1
            return [Plain(text=str(c))]
        elif len(attrs)==2:
            a,b=(int(i) for i in attrs[:2])
            if a<b:
                a,b=b,a
            if a>GLOBAL.CaLimit or b>GLOBAL.CbLimit:
                return [Plain(text='太大了我放不下(>///<)')]
            return [Plain(text=str(comb(a,b)))]
        elif len(attrs)==1:
            b=int(attrs[0])
            if b>GLOBAL.CbLimit:
                return [Plain(text='太大了我放不下(>///<)')]
            return [Plain(text=str(math.factorial(b)))]
        else:
            return []
    except Exception as e:
        return [Plain(str(e))]

def CalA(*attrs,**kwargs):
    return CalC('A',*attrs,**kwargs)

def CalKatalan(*attrs,**kwargs):
    try:
        if len(attrs):
            a = int(attrs[0])
            if a>GLOBAL.CbLimit:
                return [Plain(text='太大了我放不下(>///<)')]
            return [Plain(str(comb(2*a,a)//(a+1)))]
        else:
            return []
    except Exception as e:
        return [Plain(str(e))]

def 统计姬from104(*attrs,**kwargs):
    l=[float(x) for x in attrs]
    ostr = []
    ostr.append(Plain(f"Mean 平均数:{statistics.mean(l)}\n"))
    ostr.append(Plain(f"Median 中位数:{statistics.median(l)}\n"))
    ostr.append(Plain(f"Low Median 低中位数:{statistics.median_low(l)}\n"))
    ostr.append(Plain(f"High Median 高中位数:{statistics.median_high(l)}\n"))
    ostr.append(Plain(f"Sample Variance 样本方差:{statistics.variance(l)}\n"))
    ostr.append(Plain(f"Sample Standard Deviation 样本标准差:{statistics.stdev(l)}\n"))
    ostr.append(Plain(f"Variance 总体方差:{statistics.pvariance(l)}\n"))
    ostr.append(Plain(f"Standard Deviation 总体标准差:{statistics.pstdev(l)}\n"))
    return ostr

def QM化简器(*attrs,**kwargs):
    v = list(attrs)
    if len(v[0].split(',')) > 1: # 最小项输入
        if len(v) == 1:
            return [Plain(text=quine_mccluskey.qmccluskey.maid(minterms=v[0].split(',')))]
        else:
            return [Plain(text=quine_mccluskey.qmccluskey.maid('',*v[1:3],minterms=v[0].split(',')))]
    else:
        return [Plain(text=quine_mccluskey.qmccluskey.maid(*v[:3]))]

def 逆元(*attrs,**kwargs):
    return [Plain(str(getinv(int(attrs[0]),int(attrs[1]))))]

def 孙子定理(*attrs,**kwargs):
    il = ' '.join(attrs).strip().split()
    li = []
    for i in il:
        if i.isdigit():
            li.append(int(i))
    if len(li)&1:
        return [Plain('输入不合法')]
    else:
        r = li.pop()
        f = li.pop()
        while li:
            C1 = li.pop()
            M1 = li.pop()
            M2 = f
            C2 = r
            G = math.gcd(M2,M1)
            L = M1*M2//G
            if (C1-C2)%G:
                return [Plain('输入数据无解')]
            f = L
            r = ((getinv(M2//G, M1//G) * (C1 - C2) // G) % (M1 // G) * M2 + C2) % f
        return [Plain(str(r))]
            




MathMap = {
    '#QM':QM化简器,
    '#C':CalC,
    '#A':CalA,
    '#K':CalKatalan,
    '#统计':统计姬from104,
    '#inv':逆元,
    '#CRT':孙子定理
}

MathShort = {
    '#stat':'#统计',
}

MathDescript = {
    '#K':'计算Katalan数，例:#K 4',
    '#A':'计算排列数，例:#A 3 3',
    '#统计':'焊接自104空间的统计代码，接受空格分隔的浮点参数，返回样本中位数，平均数，方差等信息，例:#统计 11.4 51.4 19.19 8.10',
    '#C':
'''
两个参数计算组合数，一个参数计算阶乘
例:
    #C 9 7
    计算组合数C(9,7)
    #C 20
    计算阶乘20!
''',
    '#QM':
"""
用QM法化简逻辑式，参数格式:原式 显示字母 无关项的最小项，例
用法：
    #QM <原式的逗号隔开的最小项表示> [无关项的最小项表示] [化简后显示字母]
    #QM <原式的逻辑式表示> [无关项的最小项表示]
例:
    #QM 1,4,2,8,5,7 3 a,b,c,d
    #QM b'd+a'bc'+a'bcd' 1,2
""",
    '#inv':'求给定的x在模m意义下的逆元（exgcd',
    '#CRT':
"""
用中国剩余定理解剩余方程
输入格式：
    模数1 余数1 模数2 余数2 ...
当然如果你愿意可以以回车或者空格-回车交替这样分隔输入
又如：
    模数1 余数1
    模数2 余数2
    ...
如果有解，返回值是满足所有剩余方程的最小结果
"""
}
