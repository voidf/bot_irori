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
Callable.ATNoticeQueueGlobal={}
Callable.NCNoticeQueueGlobal={}
Callable.QuickCalls = {}
Callable.proxy = proxy
Callable.DEKnowledge = {}

Exceptions = set()
Helps = set()

@irori.receiver("GroupMessage")
async def NormalHandler(message: MessageChain,app: Mirai, group: Group,member:Member):
    s = message.toString().split(' ')
    pic = message.getFirstComponent(Image)
    extDict = {
        'gp':group,
        'mem':member
    }

    if pic:
        extDict['pic'] = pic
    

    if s[0] == 'sudo':
        s.pop(0)
        if member.id in masterID:
            extDict['sudo'] = True

    Callable.app = app
    player = group.id+2**39
    if member.id not in botList:
        if 'sudo' in extDict:
            if s[0] == 'reload':
                importlib.reload(Callable)
                await app.sendGroupMessage(group,[Plain('热重载完成')])
                return
            elif s[0] == 'pull':
                await app.sendGroupMessage(group,[Plain(os.popen('git pull').read())])
                return
            elif s[0] == 'print-help':
                Helps.add(player)
                await app.sendGroupMessage(group,[Plain('异常时打印帮助')])
                return
            elif s[0] == 'cancel-help':
                Helps.discard(player)
                await app.sendGroupMessage(group,[Plain('异常时不打印帮助')])
                return
            elif s[0] == 'print-ext':
                Exceptions.add(player)
                await app.sendGroupMessage(group,[Plain('异常时打印异常信息')])
                return
            elif s[0] == 'cancel-ext':
                Exceptions.discard(player)
                await app.sendGroupMessage(group,[Plain('异常时不打印异常信息')])
                return

        a,*b = s
        l = []
        if a in Callable.shortMap:
            a = Callable.shortMap[a]
        if player in Callable.QuickCalls:
            print(Callable.QuickCalls)
            try:
                l = Callable.QuickCalls[player][0](*Callable.QuickCalls[player][1:],*s,**extDict)
                if l:
                    await app.sendGroupMessage(group,l)
                    return
            except:
                if player in Exceptions:
                    l.append(Plain(traceback.format_exc()))
                if l:
                    await app.sendGroupMessage(group,l)
        elif a in Callable.functionMap and (group.id not in allowGroup and group.id not in banGroup) or ((group.id in banGroup and a not in banGroup[group.id]) or (group.id in allowGroup and a in allowGroup[group.id] )):
            try:
                l = Callable.functionMap[a](*b, **extDict)
                print(f"MESSAGESLENGTH ===> {len(l)}")
                if l:
                    await app.sendGroupMessage(group,l)
            except:
                print(traceback.format_exc())
                if player in Exceptions:
                    l.append(Plain(traceback.format_exc()))
                if player in Helps:
                    l.append(Callable.printHelp(a))
                if l:
                    await app.sendGroupMessage(group,l)

@irori.receiver("FriendMessage")
async def event_gm1(message: MessageChain,app: Mirai, hurenzu: Friend):
    Callable.app = app
    s = message.toString().split(' ')
    player = hurenzu.id
    pic = message.getFirstComponent(Image)

    extDict = {
        'mem':hurenzu.id
    }

    if pic:
        extDict['pic'] = pic
    

    if s[0] == 'sudo':
        s.pop(0)
        if hurenzu.id in masterID:
            extDict['sudo'] = True

    if hurenzu.id not in muteList:

        if s[0] == 'reload' and 'sudo' in extDict:
            importlib.reload(Callable)
            await app.sendFriendMessage(hurenzu,[Plain('热重载完成')])
            return
        elif s[0] == 'pull' and 'sudo' in extDict:
            await app.sendFriendMessage(hurenzu,[Plain(os.popen('git pull').read())])
            return

        a,*b = s
        if a in Callable.shortMap:
            a = Callable.shortMap[a]
        if player in Callable.QuickCalls:
            l = Callable.QuickCalls[player][0](*Callable.QuickCalls[player][1:],*s,**extDict)
            if l:
                await app.sendFriendMessage(hurenzu,l)
                return
        elif a in Callable.functionMap:
            l = Callable.functionMap[a](*b, **extDict)
            if l and len(l):
                await app.sendFriendMessage(hurenzu,l)

#Image.fromFileSystem('80699361_p0.jpg')

@irori.subroutine
async def startup(bot: Mirai):
    try:
        global cfg
        print(cfg)
        for _ in cfg.get('onlineMsg',[]): # 上线提醒
            await bot.sendGroupMessage(_[0],[Plain(_[1])])
    except:
        print('未设置登录提醒')
    for _ in os.listdir('ddl/'): # 文件名即群号
        with open('ddl/'+_,'r') as fr:
            jj = json.load(fr)
        print(jj)
        for j,v in jj.items(): # j是title，v是(时间,发送成员)
            t = datetime.datetime.strptime(v[0],'%Y,%m,%d,%H,%M,%S')
            Callable.ddl通知姬(recover=True,gp=int(_),mb=v[1],tit=j,dtime=t-datetime.datetime.now())
    asyncio.ensure_future(Callable.CFLoopRoutiner())
    asyncio.ensure_future(Callable.ATLoopRoutiner())
    asyncio.ensure_future(Callable.NCLoopRoutiner())

if __name__ == '__main__':
    irori.run()
    