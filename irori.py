from mirai import Mirai, Plain, MessageChain, Friend, Face, MessageChain,Group,Image,Member,At,Source
from mirai.face import QQFaces
from bs4 import BeautifulSoup
import quine_mccluskey.qmccluskey
from PIL import ImageFont,ImageDraw
from PIL import Image as PImage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import importlib
import re
import asyncio
import requests
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
try:
    from Translate import googleTrans,BDtranslate
except:
    print('fufu Extention no exists!')
import time
import datetime



# exec(open("""Callable.py""").read())

# java -jar mirai-console-wrapper-0.2.0-all.jar -Djava.awt.headless=true

with open('authdata','r') as f:
    qq = int(f.readline().strip())
    authKey = f.readline().strip()
    mirai_api_http_locate = f.readline().strip() # httpapi所在主机的地址端口,如果 setting.yml 文件里字段 "enableWebsocket" 的值为 "true" 则需要将 "/" 换成 "/ws", 否则将接收不到消息.

irori = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")

try:
    with open('cfg.json','r') as jfr:
        cfg = json.load(jfr)
        banGroup = {int(k):v for k,v in cfg.get('banGroup',{}).items()}
        allowGroup = {int(k):v for k,v in cfg.get('allowGroup',{}).items()}
        botList = set(cfg.get('botList',[]))
        proxy = cfg.get('proxy',{})
        muteList = set(cfg.get('muteList',[]))
        masterID = set(cfg.get('masters',[]))
        
except Exception as e:
    print(e)
    banGroup = {}
    allowGroup={}
    botList = set()
    muteList = set()
    proxy = {}
    masterID = set()

import Callable
Callable.CFRenderFlag=set()
Callable.ddlQueuerGlobal = {}
Callable.CFNoticeQueueGlobal={}
Callable.QuickCalls = {}
Callable.proxy = proxy

@irori.receiver("GroupMessage")
async def NormalHandler(message: MessageChain,app: Mirai, group: Group,member:Member):
    mes = message.toString()
    pic = message.getFirstComponent(Image)
    # print(dir(pic))
    # print(pic)
    # print(pic.url)
    s = mes.split(' ')
    Callable.app = app
    player = group.id+2**39
    if member.id not in botList:
        if mes == '!@#$%^&*()_+' and member.id in masterID:
            importlib.reload(Callable)
            await app.sendGroupMessage(group,[Plain('热重载完成')])
            return
        elif mes[:3] == '我单推' and mes[-1] == '！' and member.id in masterID:
            await app.sendGroupMessage(group,[Plain(os.popen('git pull').read())])
            return
        a,*b = s
        if a in Callable.shortMap:
            a = Callable.shortMap[a]
        if player in Callable.QuickCalls:
            print(Callable.QuickCalls)
            l = Callable.QuickCalls[player][0](*Callable.QuickCalls[player][1:],*s,gp = group.id,mem = member.id)
            if l:
                await app.sendGroupMessage(group,l)
                return
        elif a in Callable.functionMap and (group.id not in allowGroup and group.id not in banGroup) or ((group.id in banGroup and banGroup[group.id] != a) or (group.id in allowGroup and allowGroup[group.id] == a)):
            l = Callable.functionMap[a](*b, gp = group, mem = member,pic = pic)
            print(f"MESSAGESLENGTH ===> {len(l)}")
            if l:
                await app.sendGroupMessage(group,l)

@irori.receiver("FriendMessage")
async def event_gm1(message: MessageChain,app: Mirai, hurenzu: Friend):
    Callable.app = app
    s = message.toString().split(' ')
    player = hurenzu.id
    pic = message.getFirstComponent(Image)
    if hurenzu.id not in muteList:
        a,*b = s
        if a in Callable.shortMap:
            a = Callable.shortMap[a]
        if player in Callable.QuickCalls:
            l = Callable.QuickCalls[player][0](*Callable.QuickCalls[player][1:],*s,mem = hurenzu.id)
            if l:
                await app.sendFriendMessage(hurenzu,l)
                return
        elif a in Callable.functionMap:
            l = Callable.functionMap[a](*b, mem = hurenzu,pic = pic)
            if l and len(l):
                await app.sendFriendMessage(hurenzu,l)

#Image.fromFileSystem('80699361_p0.jpg')

@irori.subroutine
async def startup(bot: Mirai):
    global cfg
    print(cfg)
    for _ in cfg.get('onlineMsg',[]): # 上线提醒
        await bot.sendGroupMessage(_[0],[Plain(_[1])])
    for _ in os.listdir('ddl/'): # 文件名即群号
        with open('ddl/'+_,'r') as fr:
            jj = json.load(fr)
        print(jj)
        for j,v in jj.items(): # j是title，v是(时间,发送成员)
            t = datetime.datetime.strptime(v[0],'%Y,%m,%d,%H,%M,%S')
            Callable.ddl通知姬(recover=True,gp=int(_),mb=v[1],tit=j,dtime=t-datetime.datetime.now())
    asyncio.ensure_future(Callable.CFLoopRoutiner())

if __name__ == '__main__':
    irori.run()
    