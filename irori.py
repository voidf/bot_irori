import GLOBAL
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
import argparse
# from mirai import MessageChain
from Utils import *
from Routiner import *
from Sniffer import *
from graia.broadcast.builtin.decoraters import Depend
importMirai()
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


if not os.path.exists('credits/'): os.mkdir('credits/')
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
        GLOBAL.AVGHost = cfg.get('AVGHost','')
        GLOBAL.OJHost = cfg.get('OJHost','')


except:
    traceback.print_exc()
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
    GLOBAL.AVGHost = ''
    GLOBAL.OJHost = ''


import Callable

from GLOBAL import irori, qqbot


async def irori_statistics(
    message: MessageChain,
    member:Optional[Member]=None,
    hurenzu:Optional[Friend]=None
):
    if member:
        user = member.id
    else:
        user = hurenzu.id
    chat = GLOBAL.chat_log.setdefault(user, [])
    chat.append(message)


for k,v in banGroup.items(): chkcfg(int(k)+2**39).restrict_cmd = set(v)

for k,v in allowGroup.items(): chkcfg(int(k)+2**39).allow_cmd = set(v)


SHELL = {}

def sys_reload(member,player,s,extDict): importlib.reload(Callable); return '热重载完成'

def sys_pull(member,player,s,extDict):
    if '-f' in extDict:c = 'git fetch --all && git reset --hard origin/master'
    else:c = 'git pull'
    return os.popen(c).read()

def sys_exec(member,player,s,extDict):return f"""{exec(' '.join(s[1:]))}"""

def sys_eval(member,player,s,extDict):return f"""{eval(' '.join(s[1:]))}"""

def sys_pexc(member,player,s,extDict):chkcfg(player).print_exception=True;return '异常时打印异常信息'

def sys_cexc(member,player,s,extDict):chkcfg(player).print_exception=False;return '异常时不打印异常信息'

def sys_su(member,player,s,extDict):chkcfg(player).super_users.add(member);return 'irori:~#'

def sys_exit(member,player,s,extDict):chkcfg(player).super_users.add(member);return 'irori:~$'

def sys_terminal(member,player,s,extDict):
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

@sync_to_async
def systemcall(member,player:int,s,extDict) -> (bool,str):
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
        if s[0] in sys_dict:return True,sys_dict[s[0]](member,player,s,extDict)
    if s[0] == 'instances':
        return True,f'{identifier}\n{platform.platform()} {locate}\n{tc.enable_this}'
    elif s[0] == 'use':
        if s[1] in ('*',identifier):
            tc.enable_this = True
            return True,f'{identifier}响应中'
        else:
            tc.enable_this = False
            return True,f'{identifier}已挂起'
    return False,''

def msgprework(message: MessageChain, extDict: dict) -> list:
    """消息预处理，将特殊参数放进extDict"""
    tc = chkcfg(extDict['player'])
    s = getMessageChainText(message).split(' ')
    if GLOBAL.py_mirai_version == 3: pic = message.getAllofComponent(Image)
    else:pic = message.get(Image)

    member:int = getmem(extDict['mem'])
    if pic:extDict['pic'] = pic[0]
    extDict['pics'] = pic
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
        # elif i[:1] == "-":
            # arg,*val = i[1:].split("=")
            # extDict["-"+arg] = "".join(val)
        else: ns.append(i)
    return ns

@irori.receiver("GroupMessage", headless_decoraters=[Depend(irori_statistics)])
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
                is_called,output = await systemcall(member,player,s,extDict)
                if is_called:
                    await app.sendGroupMessage(group,await compressMsg([Plain(output)],extDict))
                    return
        except:
            if tc.print_exception:
                await app.sendGroupMessage(group,await compressMsg([Plain(traceback.format_exc())],extDict))
            return
        if not tc.enable_this:
            return
        a,*b = s
        l = []
        if a in Callable.shorts:
            a = Callable.shorts[a]
        
        if a in Callable.funs:
            
            if a not in tc.restrict_cmd and (not tc.allow_cmd or a in tc.allow_cmd):
                try:
                    l = await Callable.funs[a](*b, kwargs=extDict)
                    if l is None:
                        print(traceback.format_exc())
                    else:
                        print(f"MESSAGESLENGTH ===> {len(l)}")
                    if a in GLOBAL.credit_cmds:
                        updateCredit(member, *GLOBAL.credit_cmds[a])
                    if l:
                        await app.sendGroupMessage(group,await compressMsg(l,extDict))
                except:
                    if l is None:
                        l = []
                    print(traceback.format_exc())
                    if tc.print_exception:
                        l.append(Plain(traceback.format_exc()))
                    if l:
                        await app.sendGroupMessage(group,await compressMsg(l,extDict))
                return

        if tc.quick_calls:
            print(tc.quick_calls)
            print(getMessageChainText(message))
            try:
                for ev,mono in dict(tc.quick_calls).items():
                    if ev not in tc.restrict_cmd and (not tc.allow_cmd or ev in tc.allow_cmd):
                        for sniffKey in mono['sniff']:
                            if re.search(sniffKey,getMessageChainText(message),re.S):
                                l = await Callable.funs[ev](*mono['attrs'],*s,kwargs=extDict)
                                if l:
                                    asyncio.ensure_future(app.sendGroupMessage(group,await compressMsg(l,extDict)))
                                break

            except:
                if tc.print_exception:
                    l.append(Plain(traceback.format_exc()))
                if l:
                    await app.sendGroupMessage(group,await compressMsg(l,extDict))

@irori.receiver("FriendMessage", headless_decoraters=[Depend(irori_statistics)])
async def FriendHandler(message: MessageChain, hurenzu: Friend, app: Mirai):
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
                is_called,output = await systemcall(member, player, s, extDict)
                if is_called:
                    await app.sendFriendMessage(hurenzu,await compressMsg([Plain(output)],extDict))
                    return
        except:
            if tc.print_exception:
                await app.sendFriendMessage(hurenzu,await compressMsg([Plain(traceback.format_exc())],extDict))
            return
        if not tc.enable_this:
            return
        a,*b = s
        l = []
        if a in Callable.shorts:
            a = Callable.shorts[a]
        
        if a in Callable.funs: # 命令模块
            if a not in tc.restrict_cmd and (not tc.allow_cmd or a in tc.allow_cmd):
                try:
                    l = await Callable.funs[a](*b, kwargs=extDict)
                    print(f"MESSAGESLENGTH ===> {len(l)}")
                    if a in GLOBAL.credit_cmds:
                        updateCredit(member, *GLOBAL.credit_cmds[a])
                    if l:
                        await app.sendFriendMessage(hurenzu, await compressMsg(l,extDict))
                except:
                    print(traceback.format_exc())
                    if tc.print_exception:
                        l.append(Plain(traceback.format_exc()))
                    if l:
                        await app.sendFriendMessage(hurenzu, await compressMsg(l,extDict))
                return

        if tc.quick_calls: # sniff模块
            print(tc.quick_calls)
            try:
                for ev,mono in tc.quick_calls.items():
                    if ev not in tc.restrict_cmd and (not tc.allow_cmd or ev in tc.allow_cmd):
                        for sniffKey in mono['sniff']:
                            if re.search(sniffKey,getMessageChainText(message),re.S):
                                l = await Callable.funs[ev](*mono['attrs'],*s,kwargs=extDict)
                                if l:
                                    asyncio.ensure_future(app.sendFriendMessage(hurenzu,await compressMsg(l)))
                                break

            except:
                if tc.print_exception:
                    l.append(Plain(traceback.format_exc()))
                if l:
                    await app.sendFriendMessage(hurenzu,await compressMsg(l,extDict))

async def hajime(bot):
    GLOBAL.app = bot
    try:
        if not os.path.exists('sniffer/'):
            os.mkdir('sniffer/')
        for _ in os.listdir('sniffer/'):
            print(int(_),syncSniffer(player=int(_)))
    except:
        print('嗅探器爆炸了，有点严重\n',traceback.format_exc())
    try:
        global cfg
        print(cfg)
        for k_,v_ in cfg.get('onlineMsg',{}).items(): # 上线提醒
            await bot.sendGroupMessage(int(k_),await compressMsg([Plain(random.choice(v_))],{'player':int(k_)+2**39}))
    except:
        print('未设置登录提醒（不太重要')
        traceback.print_exc()
    try:
        if not os.path.exists('ddl/'):
            os.mkdir('ddl/')
        for _ in os.listdir('ddl/'): # 文件名即群号
            with open('ddl/'+_,'r') as fr:
                jj = json.load(fr)
            print(jj)
            for j,v in jj.items(): # j是title，v是(时间,发送成员)
                t = datetime.datetime.strptime(v[0],'%Y,%m,%d,%H,%M,%S')
                dic = {
                    'recover':True,
                    'gp':int(_),
                    'mb':v[1],
                    'tit':j,
                    'dtime':t-datetime.datetime.now()
                }
                await Callable.ddl通知姬(kwargs=dic)
    except:
        print('ddl模块收到异常（不太重要：\n',traceback.format_exc())
    
    RoutinerLoop()

if GLOBAL.py_mirai_version == 3:
    @irori.subroutine
    async def startup(bot: Mirai):
        await hajime(bot)
else:
    @irori.receiver(ApplicationLaunched)
    async def startup(bot: Mirai):
        await hajime(bot)
    

print(f"============irori running with python-mirai version {GLOBAL.py_mirai_version}=============")
if GLOBAL.py_mirai_version == 3: irori.run()
else: qqbot.launch_blocking()
