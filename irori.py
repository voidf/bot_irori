from mirai import Mirai, Plain, MessageChain, Friend, Face, MessageChain,Group,Image,Member,At,Source
from mirai.face import QQFaces
from bs4 import BeautifulSoup
import quine_mccluskey.qmccluskey
from PIL import ImageFont,ImageDraw
from PIL import Image as PImage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from typing import *
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
import platform
import pexpect
import pexpect.popen_spawn
import time
import datetime
import uuid
import Test
import argparse
from Utils import *
import GLOBAL

identifier = uuid.uuid1().hex

locate = re.findall("""来自：(.*?)\r\n""",requests.get('https://202020.ip138.com/',headers={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Cache-Control":"no-cache",
    "Connection":"keep-alive",
    "DNT":"1",
    "Host":"202020.ip138.com",
    "Pragma":"no-cache",
    "Referer":"https://www.ip138.com/",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}).text)[0]

with open('authdata','r') as f:
    qq = int(f.readline().strip())
    authKey = f.readline().strip()
    mirai_api_http_locate = f.readline().strip() # httpapi所在主机的地址端口,如果 setting.yml 文件里字段 "enableWebsocket" 的值为 "true" 则需要将 "/" 换成 "/ws", 否则将接收不到消息.

irori = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")

try:
    with open('cfg.json','r',encoding='utf-8') as jfr:
        cfg = json.load(jfr)
        banGroup = {int(k):v for k,v in cfg.get('banGroup',{}).items()}
        allowGroup = {int(k):v for k,v in cfg.get('allowGroup',{}).items()}
        botList = set(cfg.get('botList',[]))
        GLOBAL.proxy = cfg.get('proxy',{})
        muteList = set(cfg.get('muteList',[]))
        masterID = set(cfg.get('masters',[]))
        GLOBAL.enable_this = set(cfg.get('enables',[0]))
        GLOBAL.lengthLim = cfg.get('lengthLim',500)
        GLOBAL.compressFontSize = cfg.get('fontSize',18)
        GLOBAL.echoMsg = cfg.get('echoMsg',False)

except Exception as e:
    print(e)
    banGroup = {}
    allowGroup={}
    botList = set()
    muteList = set()
    GLOBAL.proxy = {}
    masterID = set()
    GLOBAL.enable_this = {0}
    GLOBAL.lengthLim = 500
    GLOBAL.compressFontSize = 18
    GLOBAL.echoMsg = False

import Callable

def getmem(mono):return mono.id if getattr(mono,'id',None) else int(mono)

for k,v in banGroup.items():chkcfg(int(k)+2**39).restrict_cmd = set(v)

for k,v in allowGroup.items():chkcfg(int(k)+2**39).allow_cmd = set(v)


SHELL = {}

def sys_reload(member,player,s):importlib.reload(Callable);return '热重载完成'

def sys_pull(member,player,s):
    if '-f' in s:c = 'git fetch --all && git reset --hard origin/master'
    else:c = 'git pull'
    return os.popen(c).read()

def sys_exec(member,player,s):return f"""{exec(' '.join(s[1:]))}"""

def sys_eval(member,player,s):return f"""{eval(' '.join(s[1:]))}"""

def sys_pexc(member,player,s):chkcfg(player).print_exception=True;return '异常时打印异常信息'

def sys_cexc(member,player,s):chkcfg(player).print_exception=False;return '异常时不打印异常信息'

def sys_su(member,player,s):chkcfg(player).super_users.add(member);return 'irori:~#'

def sys_exit(member,player,s):chkcfg(player).super_users.add(member);return 'irori:~$'

def sys_terminal(member,player,s):
    if platform.platform().find('Windows') != -1:
        for i in s[1:]:
            if i in ('ps','powershell'):
                SHELL[member] = pexpect.popen_spawn.PopenSpawn('powershell')
                return '终端启动(Windows PowerShell)，退出请输入"我不玩了"'
        SHELL[member] = pexpect.popen_spawn.PopenSpawn('cmd')
        return '终端启动(Windows command prompt)，退出请输入"我不玩了"'
    else:
        SHELL[member] = pexpect.spawn('bash')
        return '终端启动(Linux bash)，退出请输入"我不玩了"'

sys_dict = {
    'reload':sys_reload,
    'pull':sys_pull,
    'eval':sys_eval,
    'exec':sys_exec,
    'pexc':sys_pexc,
    'cexc':sys_cexc,
    'su':sys_su,
    'exit':sys_exit,
    'terminal':sys_terminal,
}

def systemcall(member,player:int,s) -> (bool,str):
    tc = chkcfg(player)
    if tc.enable_this:
        if member in SHELL:
            if s[0] == '我不玩了':
                SHELL[member].kill(9)
                del SHELL[member]
                return True,'ojbk这就把你的任务扔掉'
            else:
                patts = []
                SHELL[member].sendline('\n'.join(s))
                try:
                    while True:
                        SHELL[member].expect('\r\n',timeout = 3)
                        try:
                            patts.append(SHELL[member].before.decode('utf-8'))
                        except UnicodeDecodeError:
                            patts.append(SHELL[member].before.decode('gbk'))
                except:
                    try:
                        patts.append(SHELL[member].before.decode('utf-8'))
                    except UnicodeDecodeError:
                        patts.append(SHELL[member].before.decode('gbk'))
                return True,'\n'.join(patts)
        if s[0] in sys_dict:return True,sys_dict[s[0]](member,player,s)
    if s[0] == 'instances':
        return True,f'{identifier}\n{platform.platform()} {locate}\n{tc.enable_this}'
    elif s[0] == 'use':
        if s[1] in ('*',identifier):
            tc.enable_this = True
        else:
            tc.enable_this = False
        return True,f'{identifier}响应中'
    return False,''

def msgprework(message: MessageChain, extDict: dict) -> list:
    tc = chkcfg(extDict['player'])
    s = message.toString().split(' ')
    pic = message.getFirstComponent(Image)

    member:int = getmem(extDict['mem'])
    if pic:extDict['pic'] = pic
    if member in tc.super_users:extDict['sudo'] = True
    if s[0] == 'sudo':
        s.pop(0)
        if member in masterID:
            extDict['sudo'] = True
    if GLOBAL.echoMsg:print(f"""{message}""")
    ns = []
    for i in s:
        if i[:2] == "--":
            arg,*val = i[2:].split("=")
            extDict["-"+arg] = "".join(val)
        elif i[:1] == "-":
            arg,*val = i[1:].split("=")
            extDict["-"+arg] = "".join(val)
        else: ns.append(i)
    return ns

@irori.receiver("GroupMessage")
async def GroupHandler(message: MessageChain, app: Mirai, group: Group, member:Member):
    GLOBAL.app = app
    player = group.id+2**39
    extDict = {
        'gp':group,
        'mem':member,
        'player':player
    }
    tc = chkcfg(player)
    s = msgprework(message,extDict)
    member:int = getmem(extDict['mem'])
    if member not in botList:
        try:
            if 'sudo' in extDict:
                is_called,output=systemcall(member,player,s)
                if is_called:
                    await app.sendGroupMessage(group,compressMsg([Plain(output)],extDict))
                    return
        except:
            if tc.print_exception:
                await app.sendGroupMessage(group,[Plain(traceback.format_exc())])
            return
        if not tc.enable_this:
            return
        a,*b = s
        l = []
        if a in Callable.shortMap:
            a = Callable.shortMap[a]
        
        if a in Callable.functionMap:
            
            if a not in tc.restrict_cmd and (not tc.allow_cmd or a in tc.allow_cmd):
                try:
                    l = Callable.functionMap[a](*b, **extDict)
                    if l is None:
                        print(traceback.format_exc())
                    print(f"MESSAGESLENGTH ===> {len(l)}")
                    if l:
                        await app.sendGroupMessage(group,compressMsg(l,extDict))
                except:
                    if l is None:
                        l = []
                    print(traceback.format_exc())
                    if tc.print_exception:
                        l.append(Plain(traceback.format_exc()))
                    if l:
                        await app.sendGroupMessage(group,compressMsg(l,extDict))
                return

        if tc.quick_calls:
            print(tc.quick_calls)
            try:
                for ev,mono in dict(tc.quick_calls).items():
                    if ev not in tc.restrict_cmd and (not tc.allow_cmd or ev in tc.allow_cmd):
                        for sniffKey in mono['sniff']:
                            if re.search(sniffKey,message.toString(),re.S):
                                l = Callable.functionMap[ev](*mono['attrs'],*s,**extDict)
                                if l:
                                    asyncio.ensure_future(app.sendGroupMessage(group,compressMsg(l,extDict)))
                                break

            except:
                if tc.print_exception:
                    l.append(Plain(traceback.format_exc()))
                if l:
                    await app.sendGroupMessage(group,compressMsg(l,extDict))

@irori.receiver("FriendMessage")
async def FriendHandler(message: MessageChain,app: Mirai, hurenzu: Friend):
    GLOBAL.app = app
    player = hurenzu.id
    tc = chkcfg(player)

    extDict = {
        'mem':hurenzu,
        'player':player
    }
    member = getmem(hurenzu)
    s = msgprework(message,extDict)

    if hurenzu.id not in muteList:
        
        try:
            if 'sudo' in extDict:
                is_called,output=systemcall(member,player,s)
                if is_called:
                    await app.sendFriendMessage(hurenzu,compressMsg([Plain(output)],extDict))
                    return
        except:
            if tc.print_exception:
                await app.sendFriendMessage(hurenzu,[Plain(traceback.format_exc())])
            return
        if not tc.enable_this:
            return
        a,*b = s
        l = []
        if a in Callable.shortMap:
            a = Callable.shortMap[a]
        
        if a in Callable.functionMap: # 命令模块
            if a not in tc.restrict_cmd and (not tc.allow_cmd or a in tc.allow_cmd):
                try:
                    
                    l = Callable.functionMap[a](*b, **extDict)
                    print(f"MESSAGESLENGTH ===> {len(l)}")
                    if l:
                        await app.sendFriendMessage(hurenzu,compressMsg(l,extDict))
                except:
                    print(traceback.format_exc())
                    if tc.print_exception:
                        l.append(Plain(traceback.format_exc()))
                    if l:
                        await app.sendFriendMessage(hurenzu,compressMsg(l,extDict))
                return

        if tc.quick_calls: # sniff模块
            print(tc.quick_calls)
            try:
                for ev,mono in tc.quick_calls.items():
                    if ev not in tc.restrict_cmd and (not tc.allow_cmd or ev in tc.allow_cmd):
                        for sniffKey in mono['sniff']:
                            if re.search(sniffKey,message.toString(),re.S):
                                l = Callable.functionMap[ev](*mono['attrs'],*s,**extDict)
                                if l:
                                    asyncio.ensure_future(app.sendFriendMessage(hurenzu,compressMsg(l)))
                                break

            except:
                if tc.print_exception:
                    l.append(Plain(traceback.format_exc()))
                if l:
                    await app.sendFriendMessage(hurenzu,compressMsg(l,extDict))

@irori.subroutine
async def startup(bot: Mirai):
    GLOBAL.app = bot
    try:
        if not os.path.exists('sniffer/'):
            os.mkdir('sniffer/')
        for _ in os.listdir('sniffer/'):
            Test.同步嗅探器(player=int(_))
    except:
        print('嗅探器爆炸了，有点严重\n',traceback.format_exc())
    try:
        global cfg
        print(cfg)
        for _ in cfg.get('onlineMsg',[]): # 上线提醒
            await bot.sendGroupMessage(_[0],[Plain(_[1])])
    except:
        print('未设置登录提醒（不太重要')
    try:
        if not os.path.exists('ddl/'):
            os.mkdir('ddl/')
        for _ in os.listdir('ddl/'): # 文件名即群号
            with open('ddl/'+_,'r') as fr:
                jj = json.load(fr)
            print(jj)
            for j,v in jj.items(): # j是title，v是(时间,发送成员)
                t = datetime.datetime.strptime(v[0],'%Y,%m,%d,%H,%M,%S')
                Callable.ddl通知姬(recover=True,gp=int(_),mb=v[1],tit=j,dtime=t-datetime.datetime.now())
    except:
        print('ddl模块收到异常（不太重要：\n',traceback.format_exc())
    try:
        asyncio.ensure_future(Callable.CFLoopRoutiner())
        asyncio.ensure_future(Callable.ATLoopRoutiner())
        asyncio.ensure_future(Callable.NCLoopRoutiner())
    except:
        print('竞赛日程模块出现异常（不太重要：\n',traceback.format_exc())
    try:
        asyncio.ensure_future(Callable.WeatherSubscribeRoutiner())
    except:
        print('天气预报模块出现异常（不太重要：\n',traceback.format_exc())
    try:
        asyncio.ensure_future(Callable.SentenceSubscribeRoutiner())
    except:
        print('每日一句模块出现异常（不太重要：\n',traceback.format_exc())
    
if __name__ == '__main__':
    irori.run()
    