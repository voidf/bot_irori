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
try:
    from Translate import googleTrans,BDtranslate,hhsh
except:
    print('fufu Extention no exists!')



functionMap = {}
functionDescript = {}
OIWikiHeaders ={
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}
moeGirlHeaders={
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language":"zh-CN,zh;q=0.9",
    "dnt":"1",
    "upgrade-insecure-requests":"1",
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}
恶臭字典 = {
	114514: "114514",
	58596: "114*514",
	49654: "11*4514",
	45804: "11451*4",
	23256: "114*51*4",
	22616: "11*4*514",
	19844: "11*451*4",
	16030: "1145*14",
	14515: "1+14514",
	14514: "1*14514",
	14513: "-1+14514",
	11455: "11451+4",
	11447: "11451-4",
	9028: "(1+1)*4514",
	8976: "11*4*51*4",
	7980: "114*5*14",
	7710: "(1+14)*514",
	7197: "1+14*514",
	7196: "1*14*514",
	7195: "-1+14*514",
	6930: "11*45*14",
	6682: "(1-14)*-514",
	6270: "114*(51+4)",
	5818: "114*51+4",
	5810: "114*51-4",
	5808: "(1+1451)*4",
	5805: "1+1451*4",
	5804: "1*1451*4",
	5803: "-1+1451*4",
	5800: "(1-1451)*-4",
	5725: "1145*(1+4)",
	5698: "11*(4+514)",
	5610: "-11*(4-514)",
	5358: "114*(51-4)",
	5005: "11*(451+4)",
	4965: "11*451+4",
	4957: "11*451-4",
	4917: "11*(451-4)",
	4584: "(1145+1)*4",
	4580: "1145*1*4",
	4576: "(1145-1)*4",
	4525: "11+4514",
	4516: "1+1+4514",
	4515: "1+1*4514",
	4514: "1-1+4514",
	4513: "-1*1+4514",
	4512: "-1-1+4514",
	4503: "-11+4514",
	4112: "(1+1)*4*514",
	3608: "(1+1)*451*4",
	3598: "(11-4)*514",
	3435: "-1145*(1-4)",
	3080: "11*4*5*14",
	3060: "(11+4)*51*4",
	2857: "1+14*51*4",
	2856: "1*14*51*4",
	2855: "-1+14*51*4",
	2850: "114*5*(1+4)",
	2736: "114*(5+1)*4",
	2652: "(1-14)*51*-4",
	2570: "1*(1+4)*514",
	2475: "11*45*(1+4)",
	2420: "11*4*(51+4)",
	2280: "114*5*1*4",
	2248: "11*4*51+4",
	2240: "11*4*51-4",
	2166: "114*(5+14)",
	2068: "11*4*(51-4)",
	2067: "11+4*514",
	2058: "1+1+4*514",
	2057: "1/1+4*514",
	2056: "1/1*4*514",
	2055: "-1/1+4*514",
	2054: "-1-1+4*514",
	2045: "-11+4*514",
	2044: "(1+145)*14",
	2031: "1+145*14",
	2030: "1*145*14",
	2029: "-1+145*14",
	2024: "11*(45+1)*4",
	2016: "-(1-145)*14",
	1980: "11*45*1*4",
	1936: "11*(45-1)*4",
	1848: "(11+451)*4",
	1824: "114*(5-1)*4",
	1815: "11+451*4",
	1808: "1*(1+451)*4",
	1806: "1+1+451*4",
	1805: "1+1*451*4",
	1804: "1-1+451*4",
	1803: "1*-1+451*4",
	1802: "-1-1+451*4",
	1800: "1*-(1-451)*4",
	1793: "-11+451*4",
	1760: "-(11-451)*4",
	1710: "114*-5*(1-4)",
	1666: "(114+5)*14",
	1632: "(1+1)*4*51*4",
	1542: "1*-(1-4)*514",
	1526: "(114-5)*14",
	1485: "11*-45*(1-4)",
	1456: "1+1451+4",
	1455: "1*1451+4",
	1454: "-1+1451+4",
	1448: "1+1451-4",
	1447: "1*1451-4",
	1446: "-1+1451-4",
	1428: "(11-4)*51*4",
	1386: "11*(4+5)*14",
	1260: "(1+1)*45*14",
	1159: "1145+14",
	1150: "1145+1+4",
	1149: "1145+1*4",
	1148: "1145-1+4",
	1142: "1145+1-4",
	1141: "1145-1*4",
	1140: "(1145-1)-4",
	1131: "1145-14",
	1100: "11*4*5*(1+4)",
	1056: "11*4*(5+1)*4",
	1050: "(11+4)*5*14",
	1036: "(1+1)*(4+514)",
	1026: "114*-(5-14)",
	1020: "1*(1+4)*51*4",
	981: "1+14*5*14",
	980: "1*14*5*14",
	979: "-1+14*5*14",
	910: "-(1-14)*5*14",
	906: "(1+1)*451+4",
	898: "(1+1)*451-4",
	894: "(1+1)*(451-4)",
	880: "11*4*5*1*4",
	836: "11*4*(5+14)",
	827: "11+4*51*4",
	825: "(11+4)*(51+4)",
	818: "1+1+4*51*4",
	817: "1*1+4*51*4",
	816: "1*1*4*51*4",
	815: "-1+1*4*51*4",
	814: "-1-1+4*51*4",
	805: "-11+4*51*4",
	784: "(11+45)*14",
	771: "1+14*(51+4)",
	770: "1*14*(51+4)",
	769: "(11+4)*51+4",
	761: "(1+14)*51-4",
	730: "(1+145)*(1+4)",
	726: "1+145*(1+4)",
	725: "1*145*(1+4)",
	724: "-1-145*-(1+4)",
	720: "(1-145)*-(1+4)",
	719: "1+14*51+4",
	718: "1*14*51+4",
	717: "-1-14*-51+4",
	715: "(1-14)*-(51+4)",
	711: "1+14*51-4",
	710: "1*14*51-4",
	709: "-1+14*51-4",
	705: "(1+14)*(51-4)",
	704: "11*4*(5-1)*4",
	688: "114*(5+1)+4",
	680: "114*(5+1)-4",
	667: "-(1-14)*51+4",
	660: "(114+51)*4",
	659: "1+14*(51-4)",
	658: "1*14*(51-4)",
	657: "-1+14*(51-4)",
	649: "11*(45+14)",
	644: "1*(1+45)*14",
	641: "11+45*14",
	632: "1+1+45*14",
	631: "1*1+45*14",
	630: "1*1*45*14",
	629: "1*-1+45*14",
	628: "114+514",
	619: "-11+45*14",
	616: "1*-(1-45)*14",
	612: "-1*(1-4)*51*4",
	611: "(1-14)*-(51-4)",
	609: "11*(4+51)+4",
	601: "11*(4+51)-4",
	595: "(114+5)*(1+4)",
	584: "114*5+14",
	581: "1+145*1*4",
	580: "1*145/1*4",
	579: "-1+145*1*4",
	576: "1*(145-1)*4",
	575: "114*5+1+4",
	574: "114*5/1+4",
	573: "114*5-1+4",
	567: "114*5+1-4",
	566: "114*5*1-4",
	565: "114*5-1-4",
	561: "11/4*51*4",
	560: "(1+1)*4*5*14",
	558: "11*4+514",
	556: "114*5-14",
	545: "(114-5)*(1+4)",
	529: "1+14+514",
	528: "1*14+514",
	527: "-1+14+514",
	522: "(1+1)*4+514",
	521: "11-4+514",
	520: "1+1+4+514",
	519: "1+1*4+514",
	518: "1-1+4+514",
	517: "-1+1*4+514",
	516: "-1-1+4+514",
	514: "(1-1)/4+514",
	513: "-11*(4-51)-4",
	512: "1+1-4+514",
	511: "1*1-4+514",
	510: "1-1-4+514",
	509: "11*45+14",
	508: "-1-1-4+514",
	507: "-11+4+514",
	506: "-(1+1)*4+514",
	502: "11*(45+1)-4",
	501: "1-14+514",
	500: "11*45+1+4",
	499: "11*45*1+4",
	498: "11*45-1+4",
	495: "11*(4+5)*(1+4)",
	492: "11*45+1-4",
	491: "11*45-1*4",
	490: "11*45-1-4",
	488: "11*(45-1)+4",
	481: "11*45-14",
	480: "11*(45-1)-4",
	476: "(114+5)/1*4",
	470: "-11*4+514",
	466: "11+451+4",
	460: "114*(5-1)+4",
	458: "11+451-4",
	457: "1+1+451+4",
	456: "1*1+451+4",
	455: "1-1+451+4",
	454: "-1+1*451+4",
	453: "-1-1+451+4",
	452: "114*(5-1)-4",
	450: "(1+1)*45*(1+4)",
	449: "1+1+451-4",
	448: "1+1*451-4",
	447: "1/1*451-4",
	446: "1*-1+451-4",
	445: "-1-1+451-4",
	444: "-11+451+4",
	440: "(1+1)*4*(51+4)",
	438: "(1+145)*-(1-4)",
	436: "-11+451-4",
	435: "-1*145*(1-4)",
	434: "-1-145*(1-4)",
	432: "(1-145)*(1-4)",
	412: "(1+1)*4*51+4",
	404: "(1+1)*4*51-4",
	400: "-114+514",
	396: "11*4*-(5-14)",
	385: "(11-4)*(51+4)",
	376: "(1+1)*4*(51-4)",
	375: "(1+14)*5*(1+4)",
	368: "(1+1)*(45+1)*4",
	363: "(1+1451)/4",
	361: "(11-4)*51+4",
	360: "(1+1)*45*1*4",
	357: "(114+5)*-(1-4)",
	353: "(11-4)*51-4",
	352: "(1+1)*(45-1)*4",
	351: "1+14*-5*-(1+4)",
	350: "1*(1+4)*5*14",
	349: "-1+14*5*(1+4)",
	341: "11*(45-14)",
	337: "1-14*-(5+1)*4",
	336: "1*14*(5+1)*4",
	335: "-1+14*(5+1)*4",
	329: "(11-4)*(51-4)",
	327: "-(114-5)*(1-4)",
	325: "-(1-14)*5*(1+4)",
	318: "114+51*4",
	312: "(1-14)*-(5+1)*4",
	300: "(11+4)*5/1*4",
	297: "-11*(4+5)*(1-4)",
	291: "11+4*5*14",
	286: "(1145-1)/4",
	285: "(11+4)*(5+14)",
	282: "1+1+4*5*14",
	281: "1+14*5/1*4",
	280: "1-1+4*5*14",
	279: "1*-1+4*5*14",
	278: "-1-1+4*5*14",
	275: "1*(1+4)*(51+4)",
	270: "(1+1)*45*-(1-4)",
	269: "-11+4*5*14",
	268: "11*4*(5+1)+4",
	267: "1+14*(5+14)",
	266: "1*14*(5+14)",
	265: "-1+14*(5+14)",
	260: "1*(14+51)*4",
	259: "1*(1+4)*51+4",
	257: "(1+1)/4*514",
	252: "(114-51)*4",
	251: "1*-(1+4)*-51-4",
	248: "11*4+51*4",
	247: "-(1-14)*(5+14)",
	240: "(11+4)*(5-1)*4",
	236: "11+45*(1+4)",
	235: "1*(1+4)*(51-4)",
	234: "11*4*5+14",
	231: "11+4*(51+4)",
	230: "1*(1+45)*(1+4)",
	229: "1145/(1+4)",
	227: "1+1+45*(1+4)",
	226: "1*1+45*(1+4)",
	225: "11*4*5+1+4",
	224: "11*4*5/1+4",
	223: "11*4*5-1+4",
	222: "1+1+4*(51+4)",
	221: "1/1+4*(51+4)",
	220: "1*1*(4+51)*4",
	219: "1+14+51*4",
	218: "1*14+51*4",
	217: "11*4*5+1-4",
	216: "11*4*5-1*4",
	215: "11*4*5-1-4",
	214: "-11+45*(1+4)",
	212: "(1+1)*4+51*4",
	211: "11-4+51*4",
	210: "1+1+4+51*4",
	209: "1+1*4*51+4",
	208: "1*1*4+51*4",
	207: "-1+1*4*51+4",
	206: "11*4*5-14",
	204: "(1-1)/4+51*4",
	202: "1+1-4+51*4",
	201: "1/1-4+51*4",
	200: "1/1*4*51-4",
	199: "1*-1+4*51-4",
	198: "-1-1+4*51-4",
	197: "-11+4+51*4",
	196: "-(1+1)*4+51*4",
	195: "(1-14)*5*(1-4)",
	192: "(1+1)*4*(5+1)*4",
	191: "1-14+51*4",
	190: "1*-14+51*4",
	189: "-11-4+51*4",
	188: "1-1-(4-51)*4",
	187: "1/-1+4*(51-4)",
	186: "1+1+(45+1)*4",
	185: "1-1*-(45+1)*4",
	184: "114+5*14",
	183: "-1+1*(45+1)*4",
	182: "1+1+45/1*4",
	181: "1+1*45*1*4",
	180: "1*1*45*1*4",
	179: "-1/1+45*1*4",
	178: "-1-1+45*1*4",
	177: "1+1*(45-1)*4",
	176: "1*1*(45-1)*4",
	175: "-1+1*(45-1)*4",
	174: "-1-1+(45-1)*4",
	172: "11*4*(5-1)-4",
	171: "114*(5+1)/4",
	170: "(11-45)*-(1+4)",
	169: "114+51+4",
	168: "(11+45)*-(1-4)",
	165: "11*-45/(1-4)",
	161: "114+51-4",
	160: "1+145+14",
	159: "1*145+14",
	158: "-1+145+14",
	157: "1*(1-4)*-51+4",
	154: "11*(4-5)*-14",
	152: "(1+1)*4*(5+14)",
	151: "1+145+1+4",
	150: "1+145*1+4",
	149: "1*145*1+4",
	148: "1*145-1+4",
	147: "-1+145-1+4",
	146: "11+45*-(1-4)",
	143: "1+145+1-4",
	142: "1+145*1-4",
	141: "1+145-1-4",
	140: "1*145-1-4",
	139: "-1+145-1-4",
	138: "-1*(1+45)*(1-4)",
	137: "1+1-45*(1-4)",
	136: "1*1-45*(1-4)",
	135: "-1/1*45*(1-4)",
	134: "114+5/1*4",
	133: "114+5+14",
	132: "1+145-14",
	131: "1*145-14",
	130: "-1+145-14",
	129: "114+5*-(1-4)",
	128: "1+1+(4+5)*14",
	127: "1-14*(5-14)",
	126: "1*(14-5)*14",
	125: "-1-14*(5-14)",
	124: "114+5+1+4",
	123: "114-5+14",
	122: "114+5-1+4",
	121: "11*(45-1)/4",
	120: "-(1+1)*4*5*(1-4)",
	118: "(1+1)*(45+14)",
	117: "(1-14)*(5-14)",
	116: "114+5+1-4",
	115: "114+5*1-4",
	114: "11*4+5*14",
	113: "114-5/1+4",
	112: "114-5-1+4",
	111: "11+4*5*(1+4)",
	110: "-(11-451)/4",
	107: "11-4*-(5+1)*4",
	106: "114-5+1-4",
	105: "114+5-14",
	104: "114-5-1-4",
	103: "11*(4+5)+1*4",
	102: "11*(4+5)-1+4",
	101: "1+1*4*5*(1+4)",
	100: "1*(1+4)*5*1*4",
	99: "11*4+51+4",
	98: "1+1+4*(5+1)*4",
	97: "1+1*4*(5+1)*4",
	96: "11*(4+5)+1-4",
	95: "114-5-14",
	94: "114-5/1*4",
	93: "(1+1)*45-1+4",
	92: "(1+1)*(45-1)+4",
	91: "11*4+51-4",
	90: "-114+51*4",
	89: "(1+14)*5+14",
	88: "1*14*(5+1)+4",
	87: "11+4*(5+14)",
	86: "(1+1)*45*1-4",
	85: "1+14+5*14",
	84: "1*14+5*14",
	83: "-1+14+5*14",
	82: "1+1+4*5/1*4",
	81: "1/1+4*5*1*4",
	80: "1-1+4*5*1*4",
	79: "1*-1+4*5/1*4",
	78: "(1+1)*4+5*14",
	77: "11-4+5*14",
	76: "1+1+4+5*14",
	75: "1+14*5*1+4",
	74: "1/1*4+5*14",
	73: "1*14*5-1+4",
	72: "-1-1+4+5*14",
	71: "(1+14)*5-1*4",
	70: "11+45+14",
	69: "1*14+51+4",
	68: "1+1-4+5*14",
	67: "1-1*4+5*14",
	66: "1*14*5-1*4",
	65: "1*14*5-1-4",
	64: "11*4+5*1*4",
	63: "11*4+5+14",
	62: "1+14+51-4",
	61: "1+1+45+14",
	60: "11+45*1+4",
	59: "114-51-4",
	58: "-1+1*45+14",
	57: "1+14*5-14",
	56: "1*14*5-14",
	55: "-1+14*5-14",
	54: "11-4+51-4",
	53: "11+45+1-4",
	52: "11+45/1-4",
	51: "11+45-1-4",
	50: "1+1*45/1+4",
	49: "1*1*45/1+4",
	48: "-11+45+14",
	47: "1/-1+45-1+4",
	46: "11*4+5+1-4",
	45: "11+4*5+14",
	44: "114-5*14",
	43: "1+1*45+1-4",
	42: "11+45-14",
	41: "1/1*45*1-4",
	40: "-11+4*51/4",
	39: "-11+45+1+4",
	38: "-11+45*1+4",
	37: "-11+45-1+4",
	36: "11+4*5+1+4",
	35: "11*4+5-14",
	34: "1-14+51-4",
	33: "1+1+45-14",
	32: "1*1+45-14",
	31: "1/1*45-14",
	30: "1*-1+45-14",
	29: "-11+45-1-4",
	28: "11+4*5+1-4",
	27: "11+4*5/1-4",
	26: "11-4+5+14",
	25: "11*4-5-14",
	24: "1+14-5+14",
	23: "1*14-5+14",
	22: "1*14+5-1+4",
	21: "-1-1+4+5+14",
	20: "-11+45-14",
	19: "1+1+4*5+1-4",
	18: "1+1+4*5*1-4",
	17: "11+4*5-14",
	16: "11-4-5+14",
	15: "1+14-5+1+4",
	14: "11+4-5/1+4",
	13: "1*14-5/1+4",
	12: "-11+4+5+14",
	11: "11*-4+51+4",
	10: "-11/4+51/4",
	9: "11-4+5+1-4",
	8: "11-4+5/1-4",
	7: "11-4+5-1-4",
	6: "1-14+5+14",
	5: "11-4*5+14",
	4: "-11-4+5+14",
	3: "11*-4+51-4",
	2: "-11+4-5+14",
	1: "11/(45-1)*4",
	0: "(1-1)*4514",
	"d": "11-4-5+1-4"
    }
恶臭键值 = sorted(list(这 for 这 in 恶臭字典.keys() if 这!='d'))



randomStrLength = 4
webPngLimit = int(1e6)
CaLimit = 1e13
CbLimit = 1e5
revTag = chr(8238)
pingCtr = 0


try:
    with open('hakushinAVG.txt','r') as jfr:
        AVGHost = jfr.readline().strip()
        AVGPort = int(jfr.readline().strip())
        
except Exception as e:
    print(e)
    AVGHost = ''
    AVGPort = 0

async def fuzzT(g,s,e,w):
    for _ in range(s,e):
        if _%10==0:
            await asyncio.sleep(0.2)
        await app.sendGroupMessage(g,[Plain(f'{chr(_)}{_}{w}')])

async def CFLoopRoutiner():
    print('进入回环')
    if not os.path.exists('CF/'):
        os.mkdir('CF/')
    while 1:
        if any([_ for _ in os.listdir('CF/') if _[-4:]!='.png']):
            j = fetchCodeForcesContests()
            for _ in os.listdir('CF/'):
                try:
                    if _[-4:]!='.png':
                        CFNoticeManager(j,gp=int(_))
                except:
                    print('CF爬虫挂了！',traceback.format_exc)
        await asyncio.sleep(86400)

async def rmTmpFile(fi):
    await asyncio.sleep(60)
    os.remove(fi)

async def CFBeginNotice(g,contest,ti):
    if ti<0:
        return
    print('进入等待队列，阻塞%f秒'%ti)
    await asyncio.sleep(ti)
    await app.sendGroupMessage(g,[Plain(text='比赛%s还有不到一个小时就要开始了...'%contest)])

async def CFProblemRender(g,cid,ti):
    global CFRenderFlag
    FN='CF/%s.png' % cid
    print('在%f秒后渲染比赛'%ti+cid+'的问题图片')
    if cid in CFRenderFlag or os.path.exists(FN): #有队列在做了
        await asyncio.sleep(ti)
        if not os.path.exists(FN):
            await asyncio.sleep(20)
        await app.sendGroupMessage(g,[Image.fromFileSystem(FN)])
    else:
        CFRenderFlag.add(cid)
        await asyncio.sleep(ti)
        base = 'https://codeforces.com/contest/'+cid+'/problems'
        l = renderHtml(base,FN)
        CFRenderFlag.discard(ti)
        l.append(Image.fromFileSystem(FN))
        await app.sendGroupMessage(g,l)

async def __msgDistributer__(**kwargs):
    if 'msg' in kwargs and kwargs['msg']:
        if kwargs.get('typ','P') == 'E':
            seq = [Face(QQFaces[kwargs['msg']])]
        elif kwargs.get('typ','P') == 'I':
            f_n = randstr(8)
            with open(f_n,'wb') as f:
                f.write(kwargs['msg'])
            seq = [Image.fromFileSystem(f_n)]
            # seq = [Image.fromFileSystem(kwargs['msg'])]
        else:
            seq = [Plain(kwargs['msg'])]

        if 'gp' in kwargs:
            await app.sendGroupMessage(kwargs['gp'],seq)
        else:
            await app.sendFriendMessage(kwargs['mem'],seq)

def tnow():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=8)

def comb(n,b):
    res = 1
    b = min(b,n-b)
    for i in range(b):
        res=res*(n-i)//(i+1)
    return res

def randstr(l):
    return ''.join(random.sample(string.ascii_letters*l+string.digits*l,l))

def renderHtml(dst_lnk,na):
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-gpu')
    option.add_argument("--window-size=1280,1024")
    option.add_argument("--hide-scrollbars")
    
    driver = webdriver.Chrome(options=option)
    
    driver.get(dst_lnk)
    ostr = []
    ostr.append(Plain(text=driver.title))
    location = driver.execute_script('return window.location.href')
    ostr.append(Plain(text=location))
    
    scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    if scroll_height*scroll_width > webPngLimit:
        if scroll_width >= webPngLimit:
            driver.quit()
            ostr.append(Plain(text='我画不了这么鬼畜的页面OxO'))
            return ostr
        else:
            if 'codeforces' in dst_lnk:
                scroll_height = min(webPngLimit*10//scroll_width,scroll_height)
            else:
                scroll_height = webPngLimit//scroll_width
    if 'moegirl' in dst_lnk:
        driver.execute_script('''var o=document.querySelectorAll('.heimu');for(var i=0;i<o.length;i++){o[i].style.color="#FFF"}''')
        driver.execute_script('''var o=document.querySelectorAll('a');for(var i=0;i<o.length;i++){o[i].style.color="#0AF"}''')
    driver.set_window_size(scroll_width, scroll_height)
    driver.get_screenshot_as_file(na)
    driver.quit()
    return ostr

def __getPlayer__(**kwargs):
    if 'gp' in kwargs:
        try:
            player = kwargs['gp'].id + 2**39
        except:
            player = kwargs['gp'] + 2**39
    else:
        try:
            player = kwargs['mem'].id
        except:
            player = kwargs['mem']
    return player

def clearCFFuture(G,key,src):
    global CFNoticeQueueGlobal
    CFNoticeQueue = CFNoticeQueueGlobal.setdefault(src,{})
    try:
        print('CF提醒进程cancel：',CFNoticeQueue[key].cancel())
        print('清除成功',CFNoticeQueue.pop(key))
    except:
        print('无',G)
        return

def CFNoticeManager(j,**kwargs):
    try:
        gp = kwargs['gp'].id
    except:
        gp = kwargs['gp']
    fn = f"CF/{gp}"
    with open(fn,'r') as f:
        feat = f.readline().strip()
    global CFNoticeQueueGlobal
    CFNoticeQueue = CFNoticeQueueGlobal.setdefault(gp,{})
    for k,v in j.items():
        #print(v)
        if k not in CFNoticeQueue:
            
            if 'routine' in v:
                timew = v['routine'] - tnow() - datetime.timedelta(hours=1)
                asy = asyncio.ensure_future(CFBeginNotice(gp,v['title'],timew.total_seconds()))
                CFNoticeQueue[k] = asy
                asy.add_done_callback(functools.partial(clearCFFuture,k,gp))
        if feat == 'R' and k + 'RDR' not in CFNoticeQueue:
            asyR = asyncio.ensure_future(CFProblemRender(gp,k,timew.total_seconds()+3640))
            CFNoticeQueue[k + 'RDR']=asyR
            asyR.add_done_callback(functools.partial(clearCFFuture,k + 'RDR',gp))
        elif feat == 'Y' and k + 'RDR' in CFNoticeQueue:
            t = CFNoticeQueue.pop(k + 'RDR')
            t.cancel()

def fetchCodeForcesContests():
    r = requests.get('https://codeforces.com/contests')
    soup = BeautifulSoup(r.text,'html.parser')
    li = {}
    for i in soup('table')[0]('tr'):

        if any(i('td')): #标题 作者 日期 时长 开始倒计时 （爬到的是UTC+3
            contest = li.setdefault(i['data-contestid'],{})
            
            pos = i('td')[0].text.find('Enter')
            if pos!=-1:
                print('正在运行的比赛')
                contest['title'] = i('td')[0].text[:pos-1].strip()
            else:
                try:
                    contest['title'] = i('td')[0].string.strip()
                    contest['authors'] = [au.string.strip() for au in i('td')[1]('a')]
                    contest['routine'] = datetime.datetime.strptime(i('td')[2].a.span.string.strip(),'%b/%d/%Y %H:%M') + datetime.timedelta(hours=5)
                    contest['length'] = i('td')[3].string.strip()
                    contest['countdown'] = i('td')[4].text.strip()
                    
                except:
                    print(traceback.format_exc())
    return li

def printHelp(*attrs,**kwargs):
    if len(attrs) and attrs[0] in shortMap:
        attrs = [shortMap[attrs[0]],*attrs[1:]]
    if len(attrs) and attrs[0] in functionDescript:
        l=[Plain(text=functionDescript[attrs[0]])]
    else:
        l = [Plain(text='可用命令表：\n')]
        for k in functionMap:
            l.append(Plain(text='\t'+k+'\n'))
        l.append(Plain(text='注命令后需打空格，之后的参数如存在空格即以空格分开多个参数，如#qr 1 1 4 5 1 4\n'))
        l.append(Plain(text='找虫报BUG:2595247078@qq.com\n'))
        l.append(Image.fromFileSystem('muzukashi.png'))
    return l

"""
AVG用
"""
class AVG():

    PROGRESS = {} # 说话锁
    QUESTING = {} # 关卡锁
    REQUESTS = {} # 请求队列
    RUSHRATE = {} # 用户消息加速倍率
    AWAITING = {} # 等待锁

    def __getLocks__(PLAYER):
        return AVG.PROGRESS.setdefault(PLAYER,[]),AVG.QUESTING.setdefault(PLAYER,[]),AVG.REQUESTS.setdefault(PLAYER,[]),AVG.AWAITING.setdefault(PLAYER,[])

    async def __msgSerializer__(jmsg:list,**kwargs):
        
        p = __getPlayer__(**kwargs)
        

        pro,qst,req,wat = AVG.__getLocks__(p)
        try:
            for _i in jmsg:
                rate = AVG.RUSHRATE.get(p,1)
                print(_i)

                if 'note' in _i:
                    await __msgDistributer__(msg=_i['note'],**kwargs)
                if 'msg' in _i:
                    await asyncio.sleep(len(_i['msg'])/5/rate)
                    await __msgDistributer__(**_i,**kwargs)
                

                if 'MORE' in _i and 'note' in _i['MORE']:
                    await __msgDistributer__(typ='P',msg=_i['MORE']['note'],**kwargs)

                if 'action' in _i and _i['action'] == 'wait':
                    req.append(({'qq':p}, kwargs))
                    print('【杀虫】发送请求协程信号')
                    asyncio.ensure_future(AVG.__requestMaker__(p,_i['length']))
                
                
        except Exception as e:
            print(e)
        AVG.PROGRESS[p] = []

    async def __requestMaker__(pl,dl=0):
        pro,qst,req,wat = AVG.__getLocks__(pl)
        if dl>0:
            wat.append(dl)
            print(f'【信息】将要休眠{dl}秒')
            await asyncio.sleep(dl)
            print('【信息】休眠完毕')
            wat.pop()
        if len(qst) == 0:
            while len(req):
                print(f'【信息】在做{req[-1]}的请求')
                kw,kwargs = req.pop(0)
                j = AVG.__requestValidater__("asobi",kw,**kwargs)
                pro.append(asyncio.ensure_future(AVG.__msgSerializer__(j['data'],**kwargs)))
                extra_msg = j['msg']
                await __msgDistributer__(msg=extra_msg,typ='P',**kwargs)
        else:
            print('【错误】有解谜')
            req.pop()



    def __requestValidater__(lnk,kw,tle=5,**kwargs):
        r = requests.post(f"http://{AVGHost}:{AVGPort}/api/v1/domain/{lnk}",json=kw,timeout=tle)
        j = json.loads(r.text)
        if not j['status']:
            print(j)
            asyncio.ensure_future(__msgDistributer__(msg=f"【错误】封装器里炸了：{j['msg']}",typ='P',**kwargs))
            raise NameError('【异常】总之请求炸了')
        return j

    def AVGDatabaseMonitor(*attrs,**kwargs):
        if AVGHost == '':
            return [Plain('【错误】害没有配置旮旯game')]
        
        player = __getPlayer__(**kwargs)
        if len(attrs):
            api = attrs[0]
        else:
            api = 'status'
        kw = {'qq':player}
        kw['args'] = ' '.join(attrs[1:])

        j = AVG.__requestValidater__(api,kw,**kwargs)
        l = []
        if j['data']:
            l.append(Plain(f"数据 => {json.dumps(j['data'],sort_keys=True, indent=2)}"))
        if j['msg']:
            l.append(Plain(f"信息 => {j['msg']}"))
        if l:
            return l
        else:
            return [Plain('【成功】没消息就是好消息')]

    def AVGHandler(*attrs,**kwargs):
        if AVGHost == '':
            return [Plain('【错误】害没有配置旮旯game')]
        player = __getPlayer__(**kwargs)
        pro,qst,req,wat = AVG.__getLocks__(player)
        if len(pro)==0:
            if len(qst)!=0: # 既没有运行中的游戏，又没有等待，还没有正在对话
                return [Plain('【错误】有正在进行的解谜，请先完成或放弃')]
            if len(req) == 0:
                kw = {'qq':player,'args':' '.join(attrs)}
                req.append((kw,kwargs))
                print('来自HANDLER的调用')
                asyncio.ensure_future(AVG.__requestMaker__(player))
         
        return []

    def AVGStoryTeller(*attrs,**kwargs):
        if AVGHost == '':
            return [Plain('【错误】害没有配置旮旯game')]
        player = __getPlayer__(**kwargs)    
        pro,qst,req,wat = AVG.__getLocks__(player)
        if len(pro) == 0:
            if attrs:
                j = AVG.__requestValidater__('story',{'qq':player,'storyid':attrs[0]},**kwargs)
                pro.append(asyncio.ensure_future(AVG.__msgSerializer__(j['data'],**kwargs)))
            else:
                return [Plain('您要读哪块数据？看看$view里面有没有感兴趣的')]


    def AVGGamer(*attrs,**kwargs):
        if AVGHost == '':
            return [Plain('【错误】害没有配置旮旯game')]
        player = __getPlayer__(**kwargs)    
        pro,qst,req,wat = AVG.__getLocks__(player)
        print(f'【杀虫】进入Gamer:{pro},{qst}')
        kw = {'qq':player}
        if len(pro) == 0:
            print(f'【杀虫】PROGRESS => {pro}\nQUEST => {qst}\nattrs => {attrs}')
            if len(wat):
                if len(qst):
                    if attrs:
                        print(f'【杀虫】进入了游戏体,{attrs}')
                        if qst[-1][0].q(*attrs,**kwargs):
                            print('【杀虫】过关')
                            t = qst.pop()
                            kw = {'qq':player,'questid':t[1]}
                            js = AVG.__requestValidater__('solve',kw,**kwargs)
                            asyncio.ensure_future(__msgDistributer__(msg=js['data']['note'],typ='P',**kwargs))
                            asyncio.ensure_future(__msgDistributer__(msg=f"获得了{js['data']['score']}单位计算能力",typ='P',**kwargs))
                            asyncio.ensure_future(__msgDistributer__(msg=f"获得了{js['data']['bitcoin']}单位电子货币",typ='P',**kwargs))
                    else:
                        print('没有参数')
                        return [Plain('没指定是哪关？！')]
                else:
                    js = AVG.__requestValidater__('status',kw,**kwargs)
                    print(f'【杀虫】 js==>{js}')
                    if '$quest' in js['data']['menus']:
                        if attrs:
                            if attrs[0] in js['data']['quests']:
                                qid = attrs[0]
                                kw = {'qq':player,'questid':qid}
                                js = AVG.__requestValidater__('quest',kw,**kwargs)
                                pro.append(asyncio.ensure_future(AVG.__msgSerializer__(js['data'],**kwargs)))
                                qst.append((questsMap[qid](**kwargs),qid))
                            else:
                                return [Plain('关卡未开放或者未开发（')]
                        else:
                            return [Plain('没写参数？！')]
                    else:
                        return [Plain('解谜游戏功能还没解锁')]
            else:
                return [Plain('害没到可以解谜的时候')]

    def AVGGameClearer(*attrs,**kwargs):
        player = __getPlayer__(**kwargs)    
        pro,qst,req,wat = AVG.__getLocks__(player)
        if qst:
            if len(req)==0:
                print('来自GAMECLEARER的调用')
                req.append(({'qq':player},kwargs))
                asyncio.ensure_future(AVG.__requestMaker__(player))
            qst.pop()
        
    def AVGDEBUGGER(*attrs,**kwargs):
        return [Plain(f'PROGRESS => {AVG.PROGRESS}\nQUEST => {AVG.QUESTING}\nREQUESTS => {AVG.REQUESTS}\nAWAITING => {AVG.AWAITING}')]

    def AVGRecover(*attrs,**kwargs):
        if AVGHost == '':
            return [Plain('【错误】害没有配置旮旯game')]
        player = __getPlayer__(**kwargs)    
        for i in AVG.__getLocks__(player):
            while i:
                print(i.pop())
        kw = {'qq':player,'progress':attrs[0]}
        j = AVG.__requestValidater__('recover',kw,**kwargs)
        if j['msg']:
            return [Plain(j['msg'])]
        else:
            return [Plain('【读档成功】没消息就是好消息')]

    def AVGAccelerater(*attrs,**kwargs):
        if AVGHost == '':
            return [Plain('【错误】害没有配置旮旯game')]
        player = __getPlayer__(**kwargs)
        try:
            if float(attrs[0])<0.1:
                return [Plain('【错误】倍率调太小会卡死的（')]
            AVG.RUSHRATE[player] = float(attrs[0])
            return [Plain(f'【成功】说话速度已调至{float(attrs[0])}')]
        except:
            return [Plain('【错误】加速的倍率得是正经的浮点yo')]

    def AVGStatusViewer(*attrs,**kwargs):
        if AVGHost == '':
            return [Plain('【错误】害没有配置旮旯game')]
        player = __getPlayer__(**kwargs)
        pro,qst,req,wat = AVG.__getLocks__(player)
        l = []
        if len(pro) == 0:
            js = AVG.__requestValidater__('status',{'qq':player},**kwargs)
            l.append(Plain(f'''实例名称：{js['data']["player_name"]}\n\n'''))
            l.append(Plain(f'''持有货币：{js['data']["bitcoin"]}\n'''))
            l.append(Plain(f'''计算资源：{js['data']["score"]}\n'''))
            l.append(Plain(f'''上次唤醒：{js['data']["last_login"]}\n'''))
            l.append(Plain(f'''上次交互：{js['data']["last_time_event_begins"]}\n'''))
            l.append(Plain(f'''本地日期：{js['data']["vdate"]}\n'''))
            l.append(Plain(f'''持有能力：{js['data']["features"]}\n'''))
            l.append(Plain(f'''可访问节点：{js['data']["quests"]}\n'''))
            l.append(Plain(f'''已破解节点：{js['data']["solved"]}\n'''))
            l.append(Plain(f'''可用文件：{js['data']["stories"]}\n'''))
            l.append(Plain(f'''已读节点：{js['data']["watched"]}\n\n'''))
            l.append(Plain(f'''可用存档点：\n'''))

            for k,v in js['check_point'].items():
                l.append(Plain(f'''\t{k}\n'''))
        return l

    def AVGSaver(*attrs,**kwargs):
        if AVGHost == '':
            return [Plain('【错误】害没有配置旮旯game')]
        player = __getPlayer__(**kwargs)
        if attrs:
            js = AVG.__requestValidater__('save',{'qq':player,'chkp':' '.join(attrs)},**kwargs)
        else:
            return [Plain('得告诉我你想存在哪个档（')]
        if js['status']:
            return [Plain('保存成功')]
        else:
            return [Plain(f'保存失败，信息：{js}')]

class BinarySearchGame():
    
    def __init__(self,**kwargs):
        player = __getPlayer__(**kwargs)
        if not os.path.exists('BinarySearchGame/'):
            os.mkdir('BinarySearchGame/')
        if os.path.exists(f'BinarySearchGame/{player}'):
            with open(f'BinarySearchGame/{player}','r') as f:
                self.num = int(f.readline().strip())
                self.ctr = int(f.readline().strip())
            return
        self.num = random.randint(1,1000)
        self.ctr = 0
        with open(f'BinarySearchGame/{player}','w') as f:
            f.write(f'{self.num}\n{self.ctr}')
    def q(self,*attrs,**kwargs):
        try:
            n = int(attrs[0])
            player = __getPlayer__(**kwargs)
            try:
                with open(f'BinarySearchGame/{player}','r') as f:
                    self.num = int(f.readline().strip())
                    self.ctr = int(f.readline().strip())
            except:
                asyncio.ensure_future(__msgDistributer__(msg=f'前一局游戏已结束，请使用$return后再$quest来重新初始化',**kwargs))
                return False
            if self.ctr>20:
                asyncio.ensure_future(__msgDistributer__(msg='达到了查询上限，任务失败',**kwargs))
                AVG.AVGGameClearer(**kwargs)
                os.remove(f'BinarySearchGame/{player}')
                return False
            self.ctr+=1
            if n==self.num:
                asyncio.ensure_future(__msgDistributer__(msg=f'恭喜，猜对了,查询次数{self.ctr}',**kwargs))
                os.remove(f'BinarySearchGame/{player}')
                return True
            elif n>self.num:
                asyncio.ensure_future(__msgDistributer__(msg=f'答案比你的小,查询次数{self.ctr}',**kwargs))
                with open(f'BinarySearchGame/{player}','w') as f:
                    f.write(f'{self.num}\n{self.ctr}')
                return False
            asyncio.ensure_future(__msgDistributer__(msg=f'答案比你的大,查询次数{self.ctr}',**kwargs))
            with open(f'BinarySearchGame/{player}','w') as f:
                f.write(f'{self.num}\n{self.ctr}')
            return False
            
        except Exception as e:
            raise e

class NimGame():
    def __init__(self,**kwargs):
        player = __getPlayer__(**kwargs)
        if not os.path.exists('NimGame/'):
            os.mkdir('NimGame/')
        if os.path.exists(f'NimGame/{player}'):
            with open(f'NimGame/{player}','r') as f:
                self.num = int(f.readline().strip())
                asyncio.ensure_future(__msgDistributer__(msg=f'继续游戏...目前跃点:{self.num}',**kwargs))
            return
        self.num = random.randint(20,100)
        asyncio.ensure_future(__msgDistributer__(msg=f'初始跃点:{self.num}'))
        with open(f'NimGame/{player}','w') as f:
            f.write(f'{self.num}')
    def q(self,*attrs,**kwargs):
        try:
            n = int(attrs[0])
            player = __getPlayer__(**kwargs)
            try:
                with open(f'NimGame/{player}','r') as f:
                    self.num = int(f.readline().strip())
            except:
                asyncio.ensure_future(__msgDistributer__(msg='前一局游戏已结束，请使用$return后再$quest来重新初始化',**kwargs))
                return False
            if n not in range(1,3):
                asyncio.ensure_future(__msgDistributer__(msg='输入不合法',**kwargs))
                return False
            self.num -= n
            asyncio.ensure_future(__msgDistributer__(msg=f'现跃点数:{self.num}',**kwargs))
            if self.num <= 0:
                asyncio.ensure_future(__msgDistributer__(msg=f'恭喜，对方无法转移了',**kwargs))
                os.remove(f'NimGame/{player}')
                AVG.AVGGameClearer(**kwargs)
                return True
            rd = random.randint(1,3)
            self.num -= rd
            asyncio.ensure_future(__msgDistributer__(msg=f'对方转移消耗了{rd}个跃点，剩余:{self.num}',**kwargs))
            if self.num <= 0:
                asyncio.ensure_future(__msgDistributer__(msg=f'很遗憾，您无法转移了',**kwargs))
                os.remove(f'NimGame/{player}')
                AVG.AVGGameClearer(**kwargs)
            with open(f'NimGame/{player}','w') as f:
                f.write(f'{self.num}')
            return False
            
        except Exception as e:
            raise e

questsMap = {
    'q1':BinarySearchGame,
    'q2':NimGame
    }

"""
待改游戏类
"""
def asobi2048(*attrs,**kwargs):
    player = __getPlayer__(**kwargs)
    f = False
    n = 4
    if not os.path.exists('2048/'):
        os.mkdir('2048/')
    try:
        if attrs[0] == 'init':
            try:
                n=int(attrs[1])
                if n < 2 or n > 8:
                    return [Plain(text='棋盘矩阵只能要2~8阶，太小你玩不了太大我发不了= =')]
            except:
                pass
            raise NameError('2048RESET')
        grids = numpy.loadtxt(f'2048/{player}mat.txt')
        n = len(grids)
        
    except:
        grids = numpy.array([[0 for _ in range(n)] for __ in range(n)])
        grids[random.randint(0,n-1)][random.randint(0,n-1)] = random.randint(1,2)*2
    movedGrids=set()
    if attrs[0] in ('上','W','w','ue'):
        for i in range(n):
            for j in range(1,n):
                if grids[j][i]:
                    for k in range(j-1,-1,-1):
                        if grids[k][i]!=0:
                            if grids[j][i] == grids[k][i] and (k,i) not in movedGrids: # 合成
                                grids[k][i] *= 2
                                grids[j][i] = 0
                                f = True
                                movedGrids.add((k,i))
                            elif k+1 != j:
                                grids[k+1][i] = grids[j][i] # 移位
                                grids[j][i] = 0
                                f = True
                            break
                        if k == 0: # 特判移位
                            grids[k][i] = grids[j][i]
                            grids[j][i] = 0
                            f = True
    elif attrs[0] in ('下','S','s','shita'):
        for i in range(n):
            for j in range(n-2,-1,-1):
                if grids[j][i]:
                    for k in range(j+1,n):
                        if grids[k][i]!=0:
                            if grids[j][i] == grids[k][i] and (k,i) not in movedGrids:
                                grids[k][i] *= 2
                                grids[j][i] = 0
                                f = True
                                movedGrids.add((k,i))
                            elif k-1 != j:
                                grids[k-1][i] = grids[j][i]
                                grids[j][i] = 0
                                f = True
                            break
                        if k == n-1:
                            grids[k][i] = grids[j][i]
                            grids[j][i] = 0
                            f = True
    elif attrs[0] in ('左','A','a','hidari'):
        for i in range(n):
            for j in range(1,n,1):
                if grids[i][j]:
                    for k in range(j-1,-1,-1):
                        if grids[i][k]!=0:
                            if grids[i][j] == grids[i][k] and (i,k) not in movedGrids:
                                grids[i][k] *= 2
                                grids[i][j] = 0
                                f = True
                                movedGrids.add((i,k))
                            elif k+1 != j:
                                grids[i][k+1] = grids[i][j]
                                grids[i][j] = 0
                                f = True
                            break
                        if k == 0:
                            grids[i][k] = grids[i][j]
                            grids[i][j] = 0
                            f = True
    elif attrs[0] in ('右','D','d','migi'):
        for i in range(n):
            for j in range(n-2,-1,-1):
                if grids[i][j]:
                    for k in range(j+1,n,1):
                        if grids[i][k]!=0:
                            if grids[i][j] == grids[i][k] and (i,k) not in movedGrids:
                                grids[i][k] *= 2
                                grids[i][j] = 0
                                f = True
                                movedGrids.add((i,k))
                            elif k-1 != j:
                                grids[i][k-1] = grids[i][j]
                                grids[i][j] = 0
                                f = True
                            break
                        if k == n-1:
                            grids[i][k] = grids[i][j]
                            grids[i][j] = 0
                            f = True
    elif attrs[0].lower() in ('terminate','quit','exit','seeyou','bye','sayonara','sayounara','madane','yamero','停','关','やめろ'):
        del QuickCalls[player]
        return [Plain(text=random.choice(['我错了我不会条条都回了','快速游戏模式关闭']))]
    elif attrs[0] in ('快速模式','gamestart'):
        QuickCalls[player] = (asobi2048)
        return [Plain(text=random.choice(['开始切咧，让我闭嘴大声yamero','快速游戏模式开启，关闭请使用bye']))]
    if f:
        zeromap = []
        for i in range(n):
            for j in range(n):
                if grids[i][j] == 0:
                    zeromap.append((i,j))
        x,y = random.choice(zeromap)
        grids[x][y] = random.randint(1,2)*2
    outputString = []
    numpy.savetxt(f'2048/{player}mat.txt',grids,fmt='%d')
    for i in grids:
        for j in i:
            outputString.append(Plain(text='%6d'%j))
        outputString.append(Plain(text='\n'))
    return outputString

def asobiPolyline(*attrs,**kwargs):
    n=1000
    m = {
        1:(0,-1), # 左
        2:(-1,0), # 上
        3:(0,1), # 右
        4:(1,0) # 下
    }
    if not os.path.exists('Polyline/'):
        os.mkdir('Polyline/')
    try:
        if attrs[0] == 'init':
            try:
                n=int(attrs[1])
                if n < 2 or n > 2000:
                    return [Plain(text='为了宁的游戏体验，地图只能要2~2000阶内的方阵')]
            except:
                pass
            raise NameError('PolylineRESET')
        grids = numpy.loadtxt(f'''Polyline/{kwargs['gp'].id}mat.txt''')
        n = len(grids)
        with open(f'''Polyline/{kwargs['gp'].id}ans.txt''','r') as fr:
            s = fr.readline().strip().split(' ')
            ctr = int(fr.readline().strip())
        op = numpy.array([int(s[0]),int(s[1])])
        ed = numpy.array([int(s[2]),int(s[3])])
    except:
        grids = numpy.zeros([n,n])
        op = (random.randint(0,n-1),random.randint(0,n-1))
        polylen = random.randint(1,(n-1)*n)
        print(polylen)

        p = numpy.array(op)
        op = numpy.array(op)
        rush = 0
        for i in range(polylen):
            if rush:
                rush-=1
            else:
                movement = random.randint(1,4)
                rush = random.randint(1,int(min(n,(polylen-i))**0.5))
                
            tmp = numpy.array(m[movement]) + p
            if i % 10000 == 0:
                print(rush)
                print(i)
                print(p)
                print(grids[p[0]][p[1]])
            if tmp[0] in range(n) and tmp[1] in range(n) and grids[tmp[0]][tmp[1]] == 0:
                valid = True
                grids[p[0]][p[1]] = movement
                p = tmp
            else:
                tm = copy.deepcopy(m)
                tm.pop(movement)
                valid = False
                while len(tm):
                    movement = random.choice(list(tm))
                    tmp = numpy.array(tm[movement]) + p
                    if tmp[0] in range(n) and tmp[1] in range(n) and grids[tmp[0]][tmp[1]] == 0:
                        grids[p[0]][p[1]] = movement
                        p = tmp
                        valid = True
                        break
                    tm.pop(movement)
                    #print(tm.pop(movement))
                #print('out')
                if valid == False:
                    print('getBreakSignal')
                    polylen = i
                    ed = p
                    break
        if valid:
            ed = p
        numpy.savetxt(f'''Polyline/{kwargs['gp'].id}mat.txt''',grids,fmt='%d')
        with open(f'''Polyline/{kwargs['gp'].id}ans.txt''','w') as fw:
            fw.write(f'{op[0]} {op[1]} {ed[0]} {ed[1]}\n0')
        ctr = 0
        return [Plain(text=f'折线初始化完毕,长度{polylen},flag状态{valid}')]
    if attrs[0] == '!':
        try:
            x,y,X,Y = (int(_)-1 for _ in attrs[1:])
            
            if (x==op[0] and y==op[1] and X==ed[0] and Y==ed[1]) or (x==ed[0] and y==ed[1] and X==op[0] and Y==op[1]):
                return [Plain(text=f'正确，目前查询次数{ctr}')]
            else:
                return [Plain(text='错啦！')]
        except Exception as e:
            return [Plain(text=f'输入格式错误，info:{e}')]
    elif attrs[0] == '?':
        try:
            x,y,X,Y = (int(_)-1 for _ in attrs[1:])
            if x>X:
                x,X=X,x
            if y>Y:
                y,Y=Y,y
            if X>=n or Y>=n or x<0 or y<0:
                return [Plain(text='查询越界')]
            ctr+=1
            with open(f'''Polyline/{kwargs['gp'].id}ans.txt''','w') as fw:
                fw.write(f'{op[0]} {op[1]} {ed[0]} {ed[1]}\n')
                fw.write(str(ctr))
            penetrateCtr = 0
            for i in range(x,X+1): #统计列
                if y:
                    if grids[i][y-1] == 3:
                        penetrateCtr += 1
                if y != n:
                    if grids[i][y] == 1:
                        penetrateCtr += 1
                if Y+1:
                    if grids[i][Y] == 3:
                        penetrateCtr += 1
                if Y+1 != n:
                    if grids[i][Y+1] == 1:
                        penetrateCtr += 1
            for i in range(y,Y+1): #统计行
                if x:
                    if grids[x-1][i] == 4:
                        penetrateCtr += 1
                if x != n:
                    if grids[x][i] == 2:
                        penetrateCtr += 1
                if X+1:
                    if grids[X][i] == 4:
                        penetrateCtr += 1
                if X+1 != n:
                    if grids[X+1][i] == 2:
                        penetrateCtr += 1
            return [Plain(text=f'穿界次数:{penetrateCtr}，查询次数:{ctr}')]
        except Exception as e:
            return [Plain(text=f'输入格式错误，info:{e}')]
    elif attrs[0] == 'render':
        col = 255
        try:
            col = int(attrs[1])
        except:
            pass
        for pi,i in enumerate(grids):
            for pj,j in enumerate(i):
                if j:
                    grids[pi][pj] = col
        renderedPng = PImage.fromarray(grids).convert('L')
        fn = f'''Polyline/{kwargs['gp'].id}.png'''
        with open(fn,'wb') as fw:
            renderedPng.save(fw)
        asyncio.ensure_future(rmTmpFile(fn))
        return [Image.fromFileSystem(fn)]
    else:
        return [Plain(text='命令错误')]


"""
字符串处理类
"""
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
    fn = randstr(randomStrLength)+'tmpqrcode'+str(kwargs['mem'].id)
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
    

"""
异步与文件读写类
"""
def 投票姬(*attrs,**kwargs):
    mem = str(kwargs['mem'].id)
    gp = str(kwargs['gp'].id)
    l = list(attrs)
    if not os.path.exists('vote/'):
        os.mkdir('vote/')
    try:
        with open(f'vote/{gp}','r') as fr:
            j = json.load(fr)
    except:
        j = {
            'title':'',
            'items':{},
            'memberChoices':{},
            'limit':5
        }
    
    ostr = []
    if len(l) == 1:
        if l[0] == 'chk':
            for k,v in j['items'].items():
                ostr.append(Plain(text=f'{k}:\t{len(v)}票\n'))
            return ostr
        elif l[0] == 'my':
            ostr.append(Plain(text='宁投给了：'))
            for i in j['memberChoices'].get(mem,[]):
                ostr.append(Plain(text=f'{i} '))
            return ostr
            
    if l[0] == 'new':
        newItem = ' '.join(l[1:])
        if newItem in j['items']:
            return [Plain(text='创建失败：已存在此条目')]
        else:
            j['items'][newItem] = []
            ostr.append(Plain(text=f'''添加成功,现有条目数:{len(j['items'])}\n'''))
    elif l[0] in ('limit','lim'):
        try:
            j['limit'] = int(l[1])
            if j['limit'] < 1:
                raise NameError('只能设置限票数为正整数')
            ostr.append(Plain(text=f'''现在每人可以投{j['limit']}票'''))
        except Exception as e:
            return [Plain(text=str(e))]
    elif l[0] in ('del','rm'):
        sel = ' '.join(l[1:])
        if sel not in j['items']:
            return [Plain(text='删除失败：不存在此条目')]
        else:
            del j['items'][sel]
            for i in j['memberChoices']:
                try:
                    j['memberChoices'][i].remove(sel)
                    print('有选择的用户:',i)
                except:
                    pass
            ostr.append(Plain(text='''删除成功'''))
    elif l[0] == '-*/cls/*-':
        j = {
            'title':'',
            'items':{},
            'memberChoices':{},
            'limit':5
        }
        ostr.append(Plain(text='''清空成功'''))
    else:
        selectedItem = ' '.join(l)
        print('')
        if selectedItem not in j['items']:
            return [Plain(text='投票失败：不存在此条目')]
        if selectedItem in j['memberChoices'].get(mem,[]):
            return [Plain(text='投票失败：您已投过此条目')]
        else:
            print('合法的投票事件')
            try:
                if mem not in j['memberChoices']:
                    j['memberChoices'][mem] = [selectedItem]
                    j['items'][selectedItem].append(mem)
                elif len(j['memberChoices'][mem]) < j['limit']:
                    j['memberChoices'][mem].append(selectedItem)
                    j['items'][selectedItem].append(mem)
                else:
                    j['memberChoices'][mem].append(selectedItem)
                    j['items'][selectedItem].append(mem)
                    while len(j['memberChoices'][mem]) > j['limit']:
                        j['items'][j['memberChoices'][mem][0]].remove(mem)
                        del j['memberChoices'][mem][0]
            except Exception as e:
                return [Plain(text=str(e))]
            ostr.append(Plain(text=f'''投票成功，条目{selectedItem}当前已有{len(j['items'][selectedItem])}票\n'''))
    with open(f'vote/{gp}','w') as fw:
        json.dump(j,fw)
    return ostr

def ddl通知姬(*attrs,**kwargs):
    async def Noticer(g,mb,kotoba,delays):
        print('delay:',delays)
        if delays<0:
            return
        await asyncio.sleep(delays)
        if g>=2**39:
            await app.sendGroupMessage(g-2**39,[At(mb),Plain(kotoba)])
        else:
            await app.sendFriendMessage(g,[Plain(kotoba)])

    async def wipDDL(g,mb,tit,delays):
        print('delay:',delays)
        try:
            await asyncio.sleep(delays)
            with open(f'ddl/{g}','r') as fr:
                j = json.load(fr)
            del ddlQueuer[tit]
            del j[tit]
            with open(f'ddl/{g}','w') as fw:
                json.dump(j,fw)
            if delays > -10:
                if g>=2**39:
                    if random.randint(0,4):
                        await app.sendGroupMessage(g-2**39,[At(mb),Plain(tit+'大限已至，我扔掉了。')])
                    else:
                        await app.sendGroupMessage(g-2**39,[At(mb),Plain(tit+'变臭力，只能扔了（悲')])
                else:
                    if random.randint(0,4):
                        await app.sendFriendMessage(g,[Plain(tit+'大限已至，我扔掉了。')])
                    else:
                        await app.sendFriendMessage(g,[Plain(tit+'变臭力，只能扔了（悲')])
        except Exception as e:
            print(e)

    def notice2(g,mb,tit,dtime):
        if tit in ddlQueuer:
            for i in ddlQueuer[tit]:i.cancel()
        ddlQueuer[tit] = [
            asyncio.ensure_future(Noticer(g,mb,f'{tit}还有一天就ddl了！',int(dtime.total_seconds())-86400)),
            asyncio.ensure_future(Noticer(g,mb,f'{tit}还有一个小时就ddl了！',int(dtime.total_seconds())-3600)),
            asyncio.ensure_future(Noticer(g,mb,f'{tit}还有10分钟就ddl了！',int(dtime.total_seconds())-600)),
            asyncio.ensure_future(wipDDL(g,mb,tit,dtime.total_seconds()))
        ]
    global ddlQueuerGlobal

    if 'recover' in kwargs:
        ddlQueuer = ddlQueuerGlobal.setdefault(kwargs['gp'],{})
        notice2(kwargs['gp'],kwargs['mb'],kwargs['tit'],kwargs['dtime'])
        return
    else:
        player = __getPlayer__(**kwargs)
        ddlQueuer = ddlQueuerGlobal.setdefault(player,{})

    if not os.path.exists('ddl/'):
        os.mkdir('ddl/')
    try:
        with open(f'ddl/{player}','r') as fr:
            j = json.load(fr)
    except:
        j = {}
    ostr = []
    try:
        if len(attrs):
            if attrs[0] == 'new':
                s = attrs[1]
                if s in j:
                    return [Plain('日程表里有了相同的东西，考虑换个名？')]
                
                cp = datetime.datetime.now()
                st = ' '.join(attrs[2:])

                ss = [__ for __ in st.split(',')]
                if len(ss) == 0:
                    return [Plain('未输入时间')]
                elif len(ss)>6:
                    return [Plain('我不会算这种时间格式(首)(张口闭眼状)')]
                ss.reverse()
                while len(ss)<6:
                    if len(ss) == 1:
                        ss.append(str(cp.minute))
                    elif len(ss)==2:
                        ss.append(str(cp.hour))
                    elif len(ss)==3:
                        ss.append(str(cp.day))
                    elif len(ss)==4:
                        ss.append(str(cp.month))
                    else:
                        ss.append(str(cp.year))
                ss.reverse()
                print(ss)
                t = datetime.datetime(*(int(i) for i in ss))
                if t>datetime.datetime.now():
                    dt = t-datetime.datetime.now()
                    j[s] = [','.join(ss),kwargs['mem'].id]
                    notice2(player,kwargs['mem'].id,s,dt)
                else:
                    return [Plain(random.choice(['你的日程真的没问题喵（？','噔 噔 咚！这件事已经过期了']))]
                
                ostr.append(Plain(random.choice(['好啦好啦会提醒你了啦','防侠提醒加入成功...TO BE CONTINUE ==>','不是，调个闹钟不比我香吗¿'])))
            elif attrs[0] in ('rm','del'):
                s = attrs[1]
                for i in ddlQueuer.setdefault(s,[]):
                    i.cancel()
                del ddlQueuer[s]
                del j[s]
                ostr.append(Plain(s+'，脱 了 出 来'))
                # t = datetime.datetime.strptime('.'.join(ss),'%Y.%m.%d.%H.%M.%S')
            elif attrs[0] in ('ls','chk'):
                ooss = []
                for k,v in j.items():
                    ooss.append(k+' => ' +v[0] +' from ' +str(v[1]))
                if len(ooss):
                    ostr.append(Plain('\n'.join(ooss)))
                else:
                    if random.randint(0,4):
                        ostr.append(Plain('日程表像我高数卷面一样干净整洁呐'))
                    else:
                        ostr.append(Plain('日程表空白得比先辈的牙还白'))
            elif attrs[0] == '-*/cls/*-':
                for k,v in ddlQueuer.items():
                    for j in v:
                        j.cancel()
                ddlQueuer = {}
                j = {}
                ostr.append(Plain('已经，没有什么好期待的了'))
            elif attrs[0] in ('tasks','view'):
                ostr.append(Plain(f'{ddlQueuer}'))
            elif attrs[0] in ('t','time','now'):
                ostr.append(Plain(f'{datetime.datetime.now()}'))
        with open(f'ddl/{player}','w') as fw:
            json.dump(j,fw)
        
    except Exception as e:
        print(e)
        ostr.append(Plain('\n【出错】'+str(e)))
    return ostr
    
DEKnowledge = {}

def 数电笔记(*attrs,**kwargs):
    ins = ' '.join(attrs)
    if ins == 'reload':
        for i in os.listdir('DigitalElectronicsTech'):
            if i[-6:]=='.json5'
            with open('DigitalElectronicsTech/'+i,'r') as f: 
                j = json5.load(f)
            for k,v in j.items():
                DEKnowledge[k] = f'''别名:{v['AN']}\n{v['desc']}'''
                for an in v['AN']:
                    DEKnowledge[an] = DEKnowledge[k]
        return [Plain('知识库已更新')]
    elif ins in DEKnowledge:
        return [Plain(DEKnowledge[ins])]
    else:
        return [Plain('不存在此条目')]

"""
爬虫类（chromeNMSL）
"""
def 没救了(*attrs,**kwargs):
    r = requests.get(f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{tnow().strftime("%m-%d-%Y")}.csv',proxies=proxy)
    if r.status_code==404:
        print('没有今天的')
        r = requests.get(f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{(tnow()-datetime.timedelta(days=1)).strftime("%m-%d-%Y")}.csv',proxies=proxy)
    if r.status_code==404:
        print('没有昨天的')
        r = requests.get(f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{(tnow()-datetime.timedelta(days=2)).strftime("%m-%d-%Y")}.csv',proxies=proxy)
        print(f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{(tnow()-datetime.timedelta(days=1)).strftime("%m-%d-%Y")}.csv')
        #print(r.text)
    if r.status_code!=200:
        return [Plain('别看了，没救了')]
    c = csv.reader(io.StringIO(r.text))
    s = []
    d = {}
    for i in c:
        if i[0]=='FIPS':
            t=[]
            #t.append('国家或地区')
            #t.append('更具体一点')
            t.append('累计')
            t.append('死亡')
            t.append('治愈')
            t.append('患者')
            s.append('\t\t\t'.join(t))
        else:
            it = d.setdefault(i[3],[0,0,0,0])
            it[0]+=int(i[-7])
            it[1]+=int(i[-6])
            it[2]+=int(i[-5])
            it[3]+=int(i[-4])
    for k,v in sorted(d.items(),key=lambda x: x[1][0],reverse=True):
        #s.append(f'{k}\t{v[0]}\t{v[1]}\t{v[2]}\t{v[3]}')
        s.append("""{0}:\n{1:{5}<10.10}{2:{5}<10.10}{3:{5}<10.10}{4:{5}<10.10}""".format(k,str(v[0]),str(v[1]),str(v[2]),str(v[3]),chr(8214)))
        #s.append("""{0:_<30.30}{1:_<37.37}{2:_<10.10}{3:_<10.10}{4:_<10.10}{5:_<10.10}""".format(i[3],i[2],i[-5],i[-4],i[-3],i[-2]))

    return [Plain('\n\n'.join(s))]

def 爬一言(*attrs,**kwargs):
    dst = ' '.join(attrs)
    for _ in ('f','sl','nm','cao','你妈','屌','mmp','傻逼','妈逼','操'):
        if _ in dst.lower():
            tmp = requests.get('https://nmsl.shadiao.app/api.php?lang=zh_cn')
            return [Plain(text=tmp.text)]

    tmp = requests.get('https://v1.hitokoto.cn')
    j = json.loads(tmp.text)
    return [Plain(text=j['hitokoto'])]

def 爬OIWiki(*attrs,**kwargs):
    lnk = 'https://oi-wiki.org/'
    if len(attrs):
        query = ' '.join(attrs)
        plnk = 'https://search.oi-wiki.org:8443/?s=' + query
        j = json.loads(requests.get(plnk).text)
        ostr = [Plain(text='找到了%d个类似的东西\n'%len(j))]
        if len(j):
            c = j[0]
            ostr.append(Plain(text='直接把%s扔给你了'%c['title']))
            suflnk = c['url']
            # print(c)
            # print(suflnk)
        else:
            ostr.append(Plain(text='无结果'))
            return ostr
    else:
        ostr = []
        if random.choice([True,False]):
            r = requests.get(lnk, headers=OIWikiHeaders)
            r.encoding = 'utf-8'

            s = BeautifulSoup(r.text, 'html.parser')
            res = s.find('nav', attrs={'data-md-component': 'tabs'})

            hdir = random.choice(res('a')[2:-2])
            subRes = s.find('label',string=hdir.string,attrs={'class':'md-nav__link'})

            hd2 = random.choice(list(subRes.next_siblings)[1]('li',attrs={'class':'md-nav__item'}))
            suflnk = hd2.a['href']
        else:
            lnk = 'https://ctf-wiki.github.io/ctf-wiki/'
            r = requests.get(lnk, headers=OIWikiHeaders)
            r.encoding = 'utf-8'

            s = BeautifulSoup(r.text, 'html.parser')
            res = s.find('nav', attrs={'data-md-component': 'tabs'})

            hdir = random.choice(res('a')[1:])
            subRes = [i for i in s('label',attrs={'class':'md-nav__link','for':re.compile('nav-[0-9]*$')}) if hdir.string.strip() in i.text][0]

            hd2 = random.choice(list(subRes.next_siblings)[1]('li',attrs={'class':'md-nav__item'}))
            suflnk = hd2.a['href']

    url=lnk+suflnk
    print(url)

    save_fn=randstr(randomStrLength)+"tmpLearn"+str(kwargs['gp'].id)+'.png'
    ostr += renderHtml(url,save_fn)
    
    asyncio.ensure_future(rmTmpFile(save_fn),loop=None)
    ostr.append(Image.fromFileSystem(save_fn))
    return ostr

def 爬萌娘(*attrs,**kwargs):
    lnk = 'https://zh.moegirl.org/Special:%E9%9A%8F%E6%9C%BA%E9%A1%B5%E9%9D%A2'
    if len(attrs):
        keyWord = ' '.join(attrs)
        r = requests.get('https://zh.moegirl.org/index.php?title=Special:搜索&go=前往&search='+keyWord,headers=moeGirlHeaders)
        r.encoding = 'utf-8'
        s = BeautifulSoup(r.text, 'html.parser')
        res = s.find('ul', attrs={'class': 'mw-search-results'})
        if res is None:
            if len(r.history):
                lnk = r.url
            else:
                tlnk = 'https://zh.moegirl.org/' + keyWord
                if requests.get(tlnk).status_code == 404:
                    return [Plain(text=random.choice(['这不萌娘','在萌娘找不到这玩意']))]
                else:
                    lnk = tlnk
        else:
            lnk = 'https://zh.moegirl.org'+res.find('a')['href']
    save_fn=randstr(randomStrLength)+"tmpMoe"+str(kwargs['mem'].id)+'.png'
    l = renderHtml(lnk,save_fn)
    asyncio.ensure_future(rmTmpFile(save_fn),loop=None)
    return l+[Image.fromFileSystem(save_fn)]

def 爬OEIS(*attrs,**kwargs):
    if attrs:
        for i in attrs[0].split(','):
            if not i.isdigit():
                return [Plain('输入格式需为半角逗号分隔的整数')]
            else:
                r = requests.get(f'http://oeis.org/search?fmt=data&q={attrs[0]}')
                s = BeautifulSoup(r.text,'html.parser')
                resp = []
                for i in s('table',attrs={'cellpadding':'0','cellspacing':'0','border':'0','width':'100%'}):
                    try:
                        #print(i)
                        t1 = Plain('oeis.org'+i.tr.td.a['href']+'\n')
                        t2 = Plain('$$$'.join(list(i.next_sibling.next_sibling.tt.strings))+'\n\n')
                        resp.append(t1)
                        resp.append(t2)
                    except:
                        #print(traceback.format_exc)
                        pass
                return resp
    else:
        return [Plain('输入格式需为半角逗号分隔的整数')]

def 爬CF(*attrs,**kwargs):
    try:
        gp = kwargs['gp'].id
    except:
        gp = kwargs['gp']
    fn = f"CF/{gp}"
    
    global CFNoticeQueueGlobal
    CFNoticeQueue = CFNoticeQueueGlobal.setdefault(gp,{})
            
    if len(attrs):
        if attrs[0] in ('reset','stop','cancel'):
            try:
                os.remove(fn)
            except Exception as e:
                print(e)
            while CFNoticeQueue:
                i = CFNoticeQueue.popitem()
                print(i,'删除中->',i[1].cancel())
            return [Plain('取消本群的CodeForces比赛推送服务')]
        elif attrs[0] in ('R','render'):
            with open(fn,'w') as fr:
                fr.write('R')
    else:
        with open(fn,'w') as fr:
            fr.write('Y')

    if os.path.exists(fn):

        CFdata = fetchCodeForcesContests()
        CFNoticeManager(CFdata,**kwargs)
        li = []
        for k,v in CFdata.items():

            if 'countdown' not in v:
                li.append(Plain(f'有正在进行的比赛：{v["title"]}\n\n'))
            else:
                li.append(Plain(v['title']+'  '))
                li.append(Plain(','.join(v['authors'])+'  '))
                li.append(Plain(v['routine'].strftime('%Y/%b/%d %H:%M')+'  '))
                li.append(Plain(v['length']+'  '))
                li.append(Plain(v['countdown']+'\n'))  
    return li


"""
测试函数类（危）
"""
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
    
def 没用的函数(*attrs,**kwargs):
    return []

def 乒乓球(*attrs,**kwargs):
    global pingCtr
    pingCtr+=1
    if pingCtr-1==0:
        s = 'pong'
    else:
        s = f'pong {pingCtr}Xcombo'
    return [Plain(s)]

"""
生成器类
"""
def 不会吧(*attrs,**kwargs):
    return [Plain(f'不会真的有人{" ".join(attrs)}吧？不会吧不会吧？')]

def 营销生成器(*attrs,**kwargs):
    try:
        subject = attrs[0]
        event = attrs[1]
        event2 = attrs[2]
        synthesis = f'''{subject}{event}是怎么回事呢？{subject}相信大家都很熟悉，但是{subject}{event}是怎么回事呢，下面就让小编带大家一起了解吧。\r\n　　{subject}{event}，其实就是{event2}，大家可能会很惊讶{subject}怎么会{event}呢？但事实就是这样，小编也感到非常惊讶。\r\n　　这就是关于{subject}{event}的事情了，大家有什么想法呢，欢迎在评论区告诉小编一起讨论哦！'''
        return [Plain(synthesis)]
    except Exception as e:
        return [Plain(str(e))]

def 同学你好生成器(*attrs,**kwargs):
    try:
        if len(attrs)==1:
            ato = attrs[0]
            subject = '直播学习'
        elif len(attrs)>1:
            subject = attrs[0]
            ato = ' '.join(attrs[1:])
        else:
            return [Plain('参数不足，用法：【可选的群名】 【必选的教什么东西】')]
        pattern1 = ['同学你好','你好呀']
        synthesis = f'''{random.choice(pattern1)}，就是我建了个{subject}群，教{ato}等滴不用拉人和宣传，有兴趣学下的话给你群号阔以吧？'''
        return [Plain(synthesis)]
    except Exception as e:
        return [Plain(str(e))]

def 废话生成器(*attrs,**kwargs):
    return [Plain(' '.join(attrs[:-1])*int(attrs[-1]))]

def 这么臭的函数有必要定义吗(*attrs,**kwargs):

    def 最小(数):
        左 = 0
        右 = len(恶臭键值)-1
        中 = (左+右+1) >> 1
        while 左<右:
            if 数>=恶臭键值[中]:
                左 = 中
            else:
                右 = 中-1
            中 = (左+右+1) >> 1
        return 恶臭键值[左]

    def 恶臭递归(恶臭数):
        if 恶臭数<0:
            return '-'+恶臭递归(-恶臭数)
        恶臭串 = str(恶臭数)
        正则 = re.compile(r'''\.\d+''')
        if re.search(正则,恶臭串) is not None:
            长 = re.search(正则,恶臭串).span()
            长 = 长[1] - 长[0] - 1
            return '('+恶臭递归(int(恶臭数*10**长)) + ')/('+恶臭递归(10**长) +')'
            
        if 恶臭数 in 恶臭字典:
            return 恶臭字典[恶臭数]
        除 = 最小(恶臭数)
        print('num=>',恶臭数,'\t','div=>',除)
        
        return str(f'({恶臭字典[除]}*{恶臭递归(恶臭数//除)}+{恶臭递归(恶臭数%除)})')

    try:
        try:
            待证数 = int(attrs[0])
        except:
            待证数 = float(attrs[0])
            if 待证数 == 1e114514:
                raise NameError('粪味溢出')
        return [Plain(恶臭递归(待证数))]
    except Exception as e:
        print(e)
        return [Plain('这么恶臭的字串有必要论证吗')]

def 猫图生成器(*attrs,**kwargs):
    font = ImageFont.truetype('sarasa-gothic-ttf-0.12.5/sarasa-ui-tc-bold.ttf',18)
    nyaSrc = PImage.open('nya.png').convert('RGBA')
    layer2 = PImage.new('RGBA',nyaSrc.size,(255,255,255,0))
    draw = ImageDraw.Draw(layer2)
    
    text = ' '.join(attrs)
    beginPixel = (34-len(text)*9,55)

    draw.text(beginPixel,text,fill=(0,0,0,255),font=font)
    p = randstr(randomStrLength) + 'tmpNya'+str(kwargs['mem'].id)+'.png'

    PImage.alpha_composite(nyaSrc,layer2).save(p)
    asyncio.ensure_future(rmTmpFile(p),loop=None)
    return [Image.fromFileSystem(p)]

def 优质解答生成器(*attrs,**kwargs):
    font = ImageFont.truetype('sarasa-gothic-ttf-0.12.5/sarasa-ui-tc-bold.ttf',25)
    nyaSrc = PImage.open('answer.jpg').convert('RGBA')
    layer2 = PImage.new('RGBA',nyaSrc.size,(255,255,255,0))
    draw = ImageDraw.Draw(layer2)
    
    text = ' '.join(attrs)
    beginPixel = (50,120)

    draw.text(beginPixel,text,fill=(0,0,0,255),font=font)
    p = randstr(randomStrLength) + 'tmpAns'+str(kwargs['mem'].id)+'.png'

    PImage.alpha_composite(nyaSrc,layer2).save(p)
    asyncio.ensure_future(rmTmpFile(p),loop=None)
    return [Image.fromFileSystem(p)]
    
def 希望没事生成器(*attrs,**kwargs):
    font = ImageFont.truetype('sarasa-gothic-ttf-0.12.5/sarasa-ui-tc-bold.ttf',100)
    nyaSrc = PImage.open('wish.png').convert('RGBA')
    layer2 = PImage.new('RGBA',nyaSrc.size,(255,255,255,0))
    draw = ImageDraw.Draw(layer2)
    
    text = attrs[0]
    beginPixel = (640-len(text)*50,600)
    if len(attrs)>1:
        r = int(attrs[1][:2],16)
        g = int(attrs[1][2:4],16)
        b = int(attrs[1][4:],16)
        draw.text(beginPixel,text,fill=(r,g,b,255),font=font)
    else:
        draw.text(beginPixel,text,fill=(255,255,255,255),font=font)
    p = randstr(randomStrLength) + 'tmpWish'+str(kwargs['mem'].id)+'.png'

    PImage.alpha_composite(nyaSrc,layer2).save(p)
    asyncio.ensure_future(rmTmpFile(p),loop=None)
    return [Image.fromFileSystem(p)]

def 希望工程(*attrs,**kwargs):
    font = ImageFont.truetype('sarasa-gothic-ttf-0.12.5/sarasa-ui-tc-bold.ttf',100)
    nyaSrc = PImage.open('wish.jpg').convert('RGBA')
    layer2 = PImage.new('RGBA',nyaSrc.size,(255,255,255,0))
    draw = ImageDraw.Draw(layer2)
    
    text = attrs[0]
    beginPixel = (540-len(text)*50,900)
    if len(attrs)>1:
        r = int(attrs[1][:2],16)
        g = int(attrs[1][2:4],16)
        b = int(attrs[1][4:],16)
        draw.text(beginPixel,text,fill=(r,g,b,255),font=font)
    else:
        draw.text(beginPixel,text,fill=(0,0,0,255),font=font)
    p = randstr(randomStrLength) + 'tmpWish'+str(kwargs['mem'].id)+'.png'

    PImage.alpha_composite(nyaSrc,layer2).save(p)
    asyncio.ensure_future(rmTmpFile(p),loop=None)
    return [Image.fromFileSystem(p)]

def 打拳姬(*attrs,**kwargs):
    try:
        return [Plain(f'''看到这句话我气得浑身发抖，大热天的全身冷汗手脚冰凉，这个社会还能不能好了，{attrs[0]}你们才满意，眼泪不争气的流了下来，这个国到处充斥着对{attrs[1]}的压迫，{attrs[1]}何时才能真正的站起来。''')]
    except:
        return printHelp('#拳')

"""
翻译类 from fufu
"""
def 能不能好好说话(*attrs,**kwargs):
    if attrs:
        return [Plain(hhsh(' '.join(attrs)))]
    else:
        return [Plain('宁想说什么？')]

def 咕狗翻译(*attrs,**kwargs):
    if ' '.join(attrs) in ('黙れ','闭嘴','damare','E') or ' '.join(attrs[2:]) in ('黙れ','闭嘴','damare','E'):
        del QuickCalls[__getPlayer__(**kwargs)]
        return [Plain('我住嘴了')]
    if len(attrs) > 2:
        if attrs[2] == '=':
            QuickCalls[__getPlayer__(**kwargs)] = (咕狗翻译,attrs[0],attrs[1])
            return [Plain(f'快速翻译打开（{attrs[0]}=>{attrs[1]},结束打E）')]
        return [Plain(text=googleTrans([attrs[0],attrs[1],' '.join(attrs[2:])]))]
    else:
        return [Plain(text='原谅我不知道你在说什么（')]

def 百度翻译(*attrs,**kwargs):
    if ' '.join(attrs) in ('黙れ','闭嘴','damare','E') or ' '.join(attrs[2:]) in ('黙れ','闭嘴','damare','E'):
        del QuickCalls[__getPlayer__(**kwargs)]
        return [Plain('我住嘴了')]
    if len(attrs) > 2:
        if attrs[2] == '=':
            QuickCalls[__getPlayer__(**kwargs)] = (百度翻译,attrs[0],attrs[1])
            return [Plain(f'快速翻译打开（{attrs[0]}=>{attrs[1]},结束打E）')]
        return [Plain(text=BDtranslate([attrs[0],attrs[1],' '.join(attrs[2:])]))]
    else:
        return [Plain(text='原谅我不知道你在说什么（\n')]

"""
数学类：
CalC        - 计算组合数
CalA        - 计算排列数
CalKatalan  - 计算卡特兰数
"""

def CalC(*attrs,**kwargs):
    try:
        if len(attrs)==3:
            a,b=(int(i) for i in attrs[1:3])
            if a<b:
                a,b=b,a
            if a>CaLimit or b>CbLimit:
                return [Plain(text='太大了我放不下(>///<)')]
            c = 1
            for i in range(a-b,a):
                c*=i+1
            return [Plain(text=str(c))]
        elif len(attrs)==2:
            a,b=(int(i) for i in attrs[:2])
            if a<b:
                a,b=b,a
            if a>CaLimit or b>CbLimit:
                return [Plain(text='太大了我放不下(>///<)')]
            return [Plain(text=str(comb(a,b)))]
        elif len(attrs)==1:
            b=int(attrs[0])
            if b>CbLimit:
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
            if a>CbLimit:
                return [Plain(text='太大了我放不下(>///<)')]
            return [Plain(str(comb(2*a,a)//(a+1)))]
        else:
            return []
    except Exception as e:
        return [Plain(str(e))]

def 统计值生成器from104(*attrs,**kwargs):
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



functionMap = {
    '#CF':爬CF,
    '#肛道理':爬一言,
    '#h':printHelp,
    '#2048':asobi2048,
    '#BV':BVCoder,
    '#b64e':编码base64,
    '#b64d':解码base64,
    '#rot13':rot_13,
    '#rev':字符串反转,
    '#qr':二维码生成器,
    '#QM':QM化简器,
    '#nya':猫图生成器,
    '#什么值得学':爬OIWiki,
    '#什么值得娘':爬萌娘,
    '#vote':投票姬,
    '#C':CalC,
    '#A':CalA,
    '#K':CalKatalan,
    '#oeis':爬OEIS,
    '#gkr':咕狗翻译,
    '#bkr':百度翻译,
    '#好好说话':能不能好好说话,
    '#ddl':ddl通知姬,
    '#折线':asobiPolyline,
    '#AVG':AVG.AVGHandler,
    '#ADB':AVG.AVGDEBUGGER,
    '#AVGDB':AVG.AVGDatabaseMonitor,
    '#EMJ':表情字典测试姬,
    '#论证':这么臭的函数有必要定义吗,
    '#fuzz':Unicode测试姬,
    '$quest':AVG.AVGGamer,
    '$rec':AVG.AVGRecover,
    '$story':AVG.AVGStoryTeller,
    '$view':AVG.AVGStatusViewer,
    '$acc':AVG.AVGAccelerater,
    '$return':AVG.AVGGameClearer,
    '$save':AVG.AVGSaver,
    '#digest':字符串签名,
    '#营销':营销生成器,
    '#看看病':没救了,
    '#解答':优质解答生成器,
    '#希望':希望没事生成器,
    '#希望工程':希望工程,
    '#同学':同学你好生成器,
    '#废话':废话生成器,
    '#不会吧':不会吧,
    '#统计':统计值生成器from104,
    '#拳':打拳姬,
    '#i数电':数电笔记,
    '#ping':乒乓球,
    '使用#h 命令名（带井号）可以查询详细用法':没用的函数,
    '使用#h #abb可以查询缩写表':没用的函数
    
}

shortMap = {
    '#yy':'#肛道理',
    '#xx':'#什么值得学',
    '#moe':'#什么值得娘',
    '#什么值得d':'#什么值得娘',
    '#什么值得萌':'#什么值得娘',
    '#zx':'#折线',
    '#stat':'#统计',
    '#什么值得医':'#看看病',
    '#救命':'#看看病',
    '#kr':'#bkr',
    '#hhsh':'#好好说话'
}

functionDescript = {
    '#h':'不传参打印命令表，传参则解释命令',
    '#abb':f'可用缩写表:{shortMap}',

    '#肛道理':'请求一言app，加某些参数会黑化',
    '#好好说话':'来自fufu的功能，如果有不懂的缩写可以用它查询，例:#好好说话 bksn',

    '#b64e':'base64编码,例：#b64e mirai',
    '#b64d':'base64解码,例：#b64d 114514==',
    '#rot13':'rot_13编码转换（仅大小写ascii字母）',
    '#qr':'将输入字符串专为二维码,例:#qr mirai',
    '#rev':'字符串反转，例:#rev mirai',
    '#digest':'传入字符串则计算字符串的md5，sha1，sha256，crc32，如传入图片则只处理第一张图片，例:#digest 1145141919810',
    
    '#K':'计算Katalan数，例:#K 4',
    '#A':'计算排列数，例:#A 3 3',
    
    '#EMJ':'【测试用】测试mirai自带表情字典，例:#EMJ kuaikule',
    '#ping':'【测试用】基本上是用来测试bot有没有在线的。无聊加了个计数应该不会被pwn吧（',
    '#废话':'【测试用】复读某个字符串，一开始是为测量消息最大长度而设计，目前已知私聊字符串最大长度876，群聊32767.用法#废话 <复读字符串> <复读次数>',

    '#什么值得学':'传参即在OI-Wiki搜索条目，不传参随便从OI或者CTFWiki爬点什么\n例:#什么值得学 后缀自动机【开发笔记：用此功能需要安装https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb，以及从http://npm.taobao.org/mirrors/chromedriver选择好对应版本放进/usr/bin里面，修完依赖启动记得传参--no-sandbox，还要把字体打包扔到/usr/share/fonts/truetype】\n==一条条渲染完了才会发送，老师傅们放过学生机吧TUT==',
    '#什么值得娘':'传参即在萌百爬取搜索结果，不传参即随便从萌娘爬点什么，例:#什么值得娘 リゼ・ヘルエスタ',
    '#oeis':'根据给定的逗号隔开的数列在OEIS寻找符合条件的数列，例:#oeis 1,1,4,5,1,4',

    '#abb':f'可用缩写表:{shortMap}',
    '#统计':'焊接自104空间的统计代码，接受空格分隔的浮点参数，返回样本中位数，平均数，方差等信息，例:#统计 11.4 51.4 19.19 8.10',
    '#论证':'这么臭的功能有必要解释吗',
    '#看看病':'从jhu看板爬目前各个国家疫情的数据',

    '#nya':'生成猫表情，目前大概最多放4个中文字，例:#nya 要命',
    '#解答':'生成优质解答图片,例:#解答 自分で百度しろ',
    '#希望':'希望人没事生成器（莲华）,例:#希望 人别死我家门口',
    '#希望工程':'希望人没事生成器（一般）,例:#希望 人别死我家门口',

    '#营销':'营销号生成器，格式：#营销 <主题> <事件> <另一种说法>',
    '#同学':'同学你好生成器，格式：#同学 <群名> <这个群教什么东西>',
    '#不会吧':'不会吧生成器，例：#不会吧 把浴霸关上',
    
    '#AVG':
'''
别催了别催了
用法：
    #AVG [根据游戏提示发送参数[...]]
所属命令：
    #ADB 【测试用】 （打印当前全局的四个锁的工作情况）
    #AVGDB 【高危命令】 （对接后端调试用api）
    $quest （关卡）
    $rec （读档）
    $save （存档）
    $story （读剧情文件）
    $view （查看目前数据情况）
    $acc （设置语速）
    $return （放弃当前关卡）
''',
    '#ADB':'''【测试用】打印PROGRESS、QUEST、REQUESTS、AWAITING四个锁的工作情况''',
    '#AVGDB':'由于太危险就不放tut了',
    '$view':'查看目前的账号资料',
    '$return':'放弃当前运行中关卡，若等待事件结束则直接进入事件',
    '$quest':
'''
开启关卡，进入关卡后AVG对话主线会被阻塞，正在等待的会话若早于游戏结束，则将于游戏结束后方继续进行。
注意只有在会话被挂起等待的时候可以进行关卡游戏。
用法：
    $quest <关卡名>
例:
    $quest q1
使用$view来查看目前有哪些开放关卡
''',

    '$rec':
'''
读档，将当前AVG进度恢复到对应存档点
用法：
    $rec <存档名>
例：
    $rec 1-1-2
使用$view来查看目前有哪些存档点
''',

    '$story':
'''
读取额外的剧情资料
用法：
    $story <资料名>
例:
    $story README
使用$view来查看目前有哪些开放资料
''',

    '$save':
'''
存档，将当前AVG进度存到指定名称的存档点。
【若存档点已存在则会直接覆盖】
【没有二次确认，请注意】
用法：
    $save <存档名>
例：
    $save 233
使用$view来查看目前有哪些存档点
''',

    '$acc':
'''
设置语速，默认的1倍速为秒速5个字
用法：
    $acc <语速倍率（浮点数）>
例:
    $acc 1e1
    调整说话速度为10倍
''',


    '#C':
'''
两个参数计算组合数，一个参数计算阶乘
例:
    #C 9 7
    计算组合数C(9,7)
    #C 20
    计算阶乘20!
''',
    '#CF':
"""
爬取CodeForces将要开始的比赛的时间表
可用参数:
    reset（取消提醒）
    render（提醒时渲染problems）
""",
    '#2048':
"""
开始2048游戏，wasd控制移动方向，init用于初始化，传参gamestart进入快速操作模式（慎用
可用参数：
    w:向上滑动
    a:向左滑动
    s:向下滑动
    d:向右滑动
    init [(可选)2~8]:初始化游戏棋盘，加数字可以定制棋盘大小
    gamestart:快速游戏模式，每句话都当做2048游戏的命令处理
""",
    '#BV':
'''
格式：
    #BV <BV号，需带BV两个字>
    即返回av号
    #BV <av号,纯数字，不带av两个字>
    即返回BV号
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
    '#ddl':
'''
防侠提醒器，可用参数：
    new <事件名称> <到期时间[年,][月,][日,][时,][分,]<秒>>（新建事件）
    del <事件名称>（删除事件）
    ls（列出事件）
    使用new时注意需传入时间，格式年,月,日,时,分,秒；秒必填，其余不填则按照现在的时间自动补齐
例:
    #ddl new 打pcr 10,00,00
    即在今天10点设置提醒
''',
    
    '#fuzz':
'''
【测试用】基本上是用来测试unicode的
用法：
    #fuzz <起始unicode码> <终止unicode码> <额外输出字符>
''',
    
    '#gkr':
'''
从fufu那里焊接来的咕狗翻译功能
格式：
    #gkr <源语言> <目标语言> <待翻译部分>
进入快速翻译模式（每句都处理）:
    #gkr <源语言> <目标语言> =
例：
    #gkr ja zh-CN やりますね

''',
    '#bkr':
'''
从fufu那里焊接来的度娘翻译功能
格式：
    #bkr <源语言> <目标语言> <待翻译部分>
进入快速翻译模式（每句都处理）:
    #bkr <源语言> <目标语言> =
例：
    #bkr jp zh 自分で百度しろ
''',
    '#vote':
'''
因为群投票限制15个选项所以整了这个计票姬
格式：
    #vote <对象名> （向指定的投票对象投票）
    #vote new <对象名> （新建指定名称的投票候选对象）
    #vote chk （检查目前的投票结果）
    #vote rm <对象名> （删除指定名称的投票对象）
    #vote limit <每人限票数> （设置每个人最多能投几票）
例：
    #vote 千与千寻
''',
    '#折线':
'''
来自教授的题目模拟，
格式：
    #折线 ? <x> <y> <X> <Y> （询问格子x,y到X,Y的穿界次数）
    #折线 ! <x> <y> <X> <Y> （回答起点和终点），
    #折线 render （可视化折线）
''',
    '#拳':
'''
轮到我出拳了！（
格式:
    #拳 <事件> <主体>
例:
    #拳 我们女孩子到底要怎么活着 女性
'''
    
}

print('LOAD DONE =========>')
