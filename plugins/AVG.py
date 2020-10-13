"""正在开发的文字冒险游戏类"""

import GLOBAL
from bs4 import BeautifulSoup
from PIL import ImageFont,ImageDraw
from PIL import Image as PImage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from functools import wraps
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
import traceback
import http.client
import statistics
import csv
import hashlib
import zlib
import time
import datetime

GLOBAL.PROGRESS = {} # 说话锁
GLOBAL.QUESTING = {} # 关卡锁
GLOBAL.REQUESTS = {} # 请求队列
GLOBAL.RUSHRATE = {} # 用户消息加速倍率
GLOBAL.AWAITING = {} # 等待锁

def check_host(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if GLOBAL.AVGHost:
            return func(*args, **kwargs)
        else:
            return [Plain('没有配置旮旯game！')]
    return decorator


def __getLocks__(PLAYER):
    return GLOBAL.PROGRESS.setdefault(PLAYER,[]),GLOBAL.QUESTING.setdefault(PLAYER,[]),GLOBAL.REQUESTS.setdefault(PLAYER,[]),GLOBAL.AWAITING.setdefault(PLAYER,[])


async def __msgSerializer__(jmsg:list,**kwargs):
    p = getPlayer(**kwargs)
    pro, qst, req, wat = __getLocks__(p)
    try:
        for _i in jmsg:
            msgSerializer(_i, **kwargs)
            if 'action' in _i and _i['action'] == 'wait':
                req.append(({'qq':p}, kwargs))
                print('【杀虫】发送请求协程信号')
                asyncio.ensure_future(__requestMaker__(p,_i['length']))
    except:
        print(traceback.format_exc())
    GLOBAL.PROGRESS[p] = []

async def __requestMaker__(pl, dl=0):
    pro, qst, req, wat = __getLocks__(pl)
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
            j = __requestValidater__("asobi",kw,**kwargs)
            pro.append(asyncio.ensure_future(__msgSerializer__(j['data'],**kwargs)))
            extra_msg = j['msg']
            await msgDistributer(msg=extra_msg,typ='P',**kwargs)
    else:
        print('【错误】有解谜')
        req.pop()

def __requestValidater__(lnk,kw,tle=5,**kwargs):
    r = requests.post(f"{GLOBAL.AVGHost}/api/v1/domain/{lnk}", json=kw, timeout=tle)
    j = json.loads(r.text)
    if not j['status']:
        print(j)
        asyncio.ensure_future(msgDistributer(msg=f"【错误】封装器里炸了：{j['msg']}", typ='P', **kwargs))
        raise NameError('【异常】总之请求炸了')
    return j

@check_host
def AVGDatabaseMonitor(*attrs, **kwargs):
    player = getPlayer(**kwargs)
    if len(attrs):
        api = attrs[0]
    else:
        api = 'status'
    kw = {'qq':player}
    kw['args'] = ' '.join(attrs[1:])

    j = __requestValidater__(api, kw, **kwargs)
    l = []
    if j['data']:
        l.append(Plain(f"数据 => {json.dumps(j['data'], sort_keys=True, indent=2)}"))
    if j['msg']:
        l.append(Plain(f"信息 => {j['msg']}"))
    if l:
        return l
    else:
        return [Plain('【成功】没消息就是好消息')]

@check_host
def AVGHandler(*attrs, **kwargs):
    player = getPlayer(**kwargs)
    pro, qst, req, wat = __getLocks__(player)
    if len(pro)==0:
        if len(qst)!=0: # 既没有运行中的游戏，又没有等待，还没有正在对话
            return [Plain('【错误】有正在进行的解谜，请先完成或放弃')]
        if len(req) == 0:
            kw = {'qq':player,'args':' '.join(attrs)}
            req.append((kw,kwargs))
            print('来自HANDLER的调用')
            asyncio.ensure_future(__requestMaker__(player))
    return []

@check_host
def AVGStoryTeller(*attrs, **kwargs):
    player = getPlayer(**kwargs)    
    pro, qst, req, wat = __getLocks__(player)
    if len(pro) == 0:
        if attrs:
            j = __requestValidater__('story',{'qq':player,'storyid':attrs[0]},**kwargs)
            pro.append(asyncio.ensure_future(__msgSerializer__(j['data'],**kwargs)))
            return []
        else:
            return [Plain('您要读哪块数据？看看$view里面有没有感兴趣的')]

@check_host
def AVGGamer(*attrs, **kwargs):
    player = getPlayer(**kwargs)    
    pro, qst, req, wat = __getLocks__(player)
    print(f'【杀虫】进入Gamer:{pro},{qst}')
    kw = {'qq':player}
    if len(pro) == 0:
        print(f'【杀虫】PROGRESS => {pro}\nQUEST => {qst}\nattrs => {attrs}')
        if len(wat):
            if len(qst):
                if attrs:
                    print(f'【杀虫】进入了游戏体,{attrs}')
                    if qst[-1][0].q(*attrs, **kwargs):
                        print('【杀虫】过关')
                        t = qst.pop()
                        kw = {'qq':player,'questid':t[1]}
                        js = __requestValidater__('solve',kw,**kwargs)
                        asyncio.ensure_future(msgDistributer(msg=js['data']['note'],typ='P',**kwargs))
                        asyncio.ensure_future(msgDistributer(msg=f"获得了{js['data']['score']}单位计算能力",typ='P',**kwargs))
                        asyncio.ensure_future(msgDistributer(msg=f"获得了{js['data']['bitcoin']}单位电子货币",typ='P',**kwargs))
                else:
                    print('没有参数')
                    return [Plain('没指定是哪关？！')]
            else:
                js = __requestValidater__('status',kw,**kwargs)
                print(f'【杀虫】 js==>{js}')
                if '$quest' in js['data']['menus']:
                    if attrs:
                        if attrs[0] in js['data']['quests']:
                            qid = attrs[0]
                            kw = {'qq':player,'questid':qid}
                            js = __requestValidater__('quest',kw,**kwargs)
                            pro.append(asyncio.ensure_future(__msgSerializer__(js['data'],**kwargs)))
                            qst.append((questsMap[qid](**kwargs),qid))
                        else:
                            return [Plain('关卡未开放或者未开发（')]
                    else:
                        return [Plain('没写参数？！')]
                else:
                    return [Plain('解谜游戏功能还没解锁')]
        else:
            return [Plain('害没到可以解谜的时候')]

def AVGGameClearer(*attrs, **kwargs):
    player = getPlayer(**kwargs)    
    pro, qst, req, wat = __getLocks__(player)
    if qst:
        if len(req) == 0:
            print('来自GAMECLEARER的调用')
            req.append(({'qq':player},kwargs))
            asyncio.ensure_future(__requestMaker__(player))
        qst.pop()
        
def AVGDEBUGGER(*attrs, **kwargs): return [Plain(f'PROGRESS => {GLOBAL.PROGRESS}\nQUEST => {GLOBAL.QUESTING}\nREQUESTS => {GLOBAL.REQUESTS}\nAWAITING => {GLOBAL.AWAITING}')]

@check_host
def AVGRecover(*attrs, **kwargs):
    player = getPlayer(**kwargs)    
    for i in __getLocks__(player):
        while i:
            print(i.pop())
    kw = {'qq':player, 'progress':attrs[0]}
    j = __requestValidater__('recover', kw, **kwargs)
    if j['msg']:
        return [Plain(j['msg'])]
    else:
        return [Plain('【读档成功】没消息就是好消息')]

def AVGAccelerater(*attrs, **kwargs):
    player = getPlayer(**kwargs)
    try:
        if float(attrs[0]) < 0.1:
            return [Plain('【错误】倍率调太小会卡死的（')]
        GLOBAL.RUSHRATE[player] = float(attrs[0])
        return [Plain(f'【成功】说话速度已调至{float(attrs[0])}')]
    except:
        return [Plain('【错误】加速的倍率得是正经的浮点yo')]

@check_host
def AVGStatusViewer(*attrs, **kwargs):
    player = getPlayer(**kwargs)
    pro, qst, req, wat = __getLocks__(player)
    l = []
    if len(pro) == 0:
        js = __requestValidater__('status',{'qq':player},**kwargs)
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

@check_host
def AVGSaver(*attrs, **kwargs):
    player = getPlayer(**kwargs)
    if attrs:
        js = __requestValidater__('save', {'qq':player, 'chkp':' '.join(attrs)}, **kwargs)
    else:
        return [Plain('得告诉我你想存在哪个档（')]
    if js['status']:
        return [Plain('保存成功')]
    else:
        return [Plain(f'保存失败，信息：{js}')]

class BinarySearchGame():
    def __init__(self, **kwargs):
        player = getPlayer(**kwargs)
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
    def q(self, *attrs, **kwargs):
        try:
            n = int(attrs[0])
            player = getPlayer(**kwargs)
            try:
                with open(f'BinarySearchGame/{player}','r') as f:
                    self.num = int(f.readline().strip())
                    self.ctr = int(f.readline().strip())
            except:
                asyncio.ensure_future(msgDistributer(msg=f'前一局游戏已结束，请使用$return后再$quest来重新初始化',**kwargs))
                return False
            if self.ctr > 20:
                asyncio.ensure_future(msgDistributer(msg='达到了查询上限，任务失败',**kwargs))
                AVGGameClearer(**kwargs)
                os.remove(f'BinarySearchGame/{player}')
                return False
            self.ctr += 1
            if n==self.num:
                asyncio.ensure_future(msgDistributer(msg=f'恭喜，猜对了,查询次数{self.ctr}',**kwargs))
                os.remove(f'BinarySearchGame/{player}')
                return True
            elif n>self.num:
                asyncio.ensure_future(msgDistributer(msg=f'答案比你的小,查询次数{self.ctr}',**kwargs))
                with open(f'BinarySearchGame/{player}','w') as f:
                    f.write(f'{self.num}\n{self.ctr}')
                return False
            asyncio.ensure_future(msgDistributer(msg=f'答案比你的大,查询次数{self.ctr}',**kwargs))
            with open(f'BinarySearchGame/{player}','w') as f:
                f.write(f'{self.num}\n{self.ctr}')
            return False
            
        except Exception as e:
            raise e

class NimGame():
    def __init__(self,**kwargs):
        player = getPlayer(**kwargs)
        if not os.path.exists('NimGame/'):
            os.mkdir('NimGame/')
        if os.path.exists(f'NimGame/{player}'):
            with open(f'NimGame/{player}','r') as f:
                self.num = int(f.readline().strip())
                asyncio.ensure_future(msgDistributer(msg=f'继续游戏...目前跃点:{self.num}',**kwargs))
            return
        self.num = random.randint(20,100)
        asyncio.ensure_future(msgDistributer(msg=f'初始跃点:{self.num}'))
        with open(f'NimGame/{player}','w') as f:
            f.write(f'{self.num}')
    def q(self,*attrs, **kwargs):
        try:
            n = int(attrs[0])
            player = getPlayer(**kwargs)
            try:
                with open(f'NimGame/{player}','r') as f:
                    self.num = int(f.readline().strip())
            except:
                asyncio.ensure_future(msgDistributer(msg='前一局游戏已结束，请使用$return后再$quest来重新初始化',**kwargs))
                return False
            if n not in range(1,3):
                asyncio.ensure_future(msgDistributer(msg='输入不合法',**kwargs))
                return False
            self.num -= n
            asyncio.ensure_future(msgDistributer(msg=f'现跃点数:{self.num}',**kwargs))
            if self.num <= 0:
                asyncio.ensure_future(msgDistributer(msg=f'恭喜，对方无法转移了',**kwargs))
                os.remove(f'NimGame/{player}')
                AVGGameClearer(**kwargs)
                return True
            rd = random.randint(1,3)
            self.num -= rd
            asyncio.ensure_future(msgDistributer(msg=f'对方转移消耗了{rd}个跃点，剩余:{self.num}',**kwargs))
            if self.num <= 0:
                asyncio.ensure_future(msgDistributer(msg=f'很遗憾，您无法转移了',**kwargs))
                os.remove(f'NimGame/{player}')
                AVGGameClearer(**kwargs)
            with open(f'NimGame/{player}','w') as f:
                f.write(f'{self.num}')
            return False
            
        except Exception as e:
            raise e

questsMap = {
    'q1':BinarySearchGame,
    'q2':NimGame
}

functionMap = {
    '#AVG':AVGHandler,
    '#ADB':AVGDEBUGGER,
    '#AVGDB':AVGDatabaseMonitor,
    '$quest':AVGGamer,
    '$rec':AVGRecover,
    '$story':AVGStoryTeller,
    '$view':AVGStatusViewer,
    '$acc':AVGAccelerater,
    '$return':AVGGameClearer,
    '$save':AVGSaver
}

shortMap = {}

functionDescript = {
    '#AVG':
"""
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
""",
    '#ADB':"""【测试用】打印PROGRESS、QUEST、REQUESTS、AWAITING四个锁的工作情况""",
    '#AVGDB':'由于太危险就不放tut了',
    '$view':'查看目前的账号资料',
    '$return':'放弃当前运行中关卡，若等待事件结束则直接进入事件',
    '$quest':
"""
开启关卡，进入关卡后AVG对话主线会被阻塞，正在等待的会话若早于游戏结束，则将于游戏结束后方继续进行。
注意只有在会话被挂起等待的时候可以进行关卡游戏。
用法：
    $quest <关卡名>
例:
    $quest q1
使用$view来查看目前有哪些开放关卡
""",

    '$rec':
"""
读档，将当前AVG进度恢复到对应存档点
用法：
    $rec <存档名>
例：
    $rec 1-1-2
使用$view来查看目前有哪些存档点
""",

    '$story':
"""
读取额外的剧情资料
用法：
    $story <资料名>
例:
    $story README
使用$view来查看目前有哪些开放资料
""",

    '$save':
"""
存档，将当前AVG进度存到指定名称的存档点。
【若存档点已存在则会直接覆盖】
【没有二次确认，请注意】
用法：
    $save <存档名>
例：
    $save 233
使用$view来查看目前有哪些存档点
""",

    '$acc':
"""
设置语速，默认的1倍速为秒速5个字
用法：
    $acc <语速倍率（浮点数）>
例:
    $acc 1e1
    调整说话速度为10倍
"""
}