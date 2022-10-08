"""临时开的转发接口类"""
import base64
from dataclasses import dataclass
import enum
import os
import pickle
import sys

from async_timeout import timeout

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

import basicutils.CONST as GLOBAL


from bs4 import BeautifulSoup
import re
import asyncio
import requests
import json
import random
import urllib
import traceback
import hashlib
import urllib
from basicutils.chain import *
from basicutils.network import *
from basicutils.task import *


from mongoengine import *

def 约稿(ent: CoreEntity):
    """#约稿 [#waifu, #召唤]
    ai画图，txt2img，容易被封所以还是建议优先直接用网页
    """
    tokens = ent.chain.tostr().lower().strip()
    if tokens == '样例':
        with open('Assets/waifusd/prompts.pickle', 'rb') as f:
            li = pickle.load(f)
        return random.choice(li)
    neg = ""

    if 'negative prompt:' in tokens:
        tokens, neg = tokens.split('negative prompt:', 1)
    model = [
        tokens,     # prompt
        neg,        # negetive prompt
        "None",
        "None",
        20,         # sampling Steps
        "Euler a",  # sampling method: Euler a, Euler, LMS, Heun, DPM2, DPM2 a, DPM fast, DPM adaptive, DDIM, PLMS
        False,
        False,
        1,          # batch count
        1,          # batch size
        7,          # CFG Scale
        -1,         # seed
        -1,
        0,
        0,
        0,
        False,
        ent.meta.get('-width', 512),        # width
        ent.meta.get('-height', 512),        # height
        False,
        False,
        0.7,
        "None",
        False,
        False,
        None,
        "",
        "Seed",
        "",
        "Steps",
        "",
        True,
        False,
        None,
        "",
        ""
    ]
    r = requests.post("http://127.0.0.1:7012/api/predict", json={'fn_index':11, 'data':model}).json()['data'][0][0][22:]
    return [Image(base64=r)]
    




def 开车(ent: CoreEntity):
    """#开车 [#car]
    fufu不在线，那交给i宝了vol.2
    格式:
        #开车 <typ>
        typ可选字段:
            nice   开好车
            ero    开痛车
            kusa   开灵车
            kawaii 开校车
            tank   开战车
    
    """
    from cfg import setu_api
    typ = ent.chain.pop_first_cmd()
    allow = [
        'ero', 
        'kawaii', 
        'nice', 
        'tank',
        'kusa'
    ]
    if not typ:
        typ = 'nice'
    if typ == 'tank':
        return Image(url=setu_api + 'autotank')
    if typ not in allow:
        return f'交警提示：您的车型{typ}不能上路'

    j = requests.get(setu_api + f'random?typ={typ}').json()
    return [
        Image(url=setu_api + f'bin/{j["id"]}'),
        Plain(
f"""{j['title']}
https://www.pixiv.net/artworks/{j['id']}""")]

def 聊天(ent: CoreEntity):
    """#chat [#cc]
    临时起的聊天机器人，黄鸡语料手工洗至31w训练而成
    """
    inputstr = ent.chain.tostr().strip()
    resp = requests.get(f'http://127.0.0.1:8999?word={inputstr}').json()
    return resp['reply']

def CloseWHU(ent: CoreEntity):
    """#openwhu [#whu]
    武大选课速查表，网络对接CloseWHU
    用法：
        查询课程概况：
        #openwhu get <课程名字:str> <老师名字:str>
        查询具体评价：
        #openwhu get <课程名字:str> <老师名字:str> <评价下标:int>
        投稿一条评价：
        #openwhu post <课程名字:str> <老师名字:str> <内容:json字符串>
    一条投稿的json schema如下定义：
        {
            comment: str = None # 你的体验
            score: float = None # 学分数量
            scoring: str = None # 给分情况
            material: List[str] = None  # 推荐教材
            appendix: str = None    # 补充说明
            examination: str = None # 考核方式
            intro: str = None   # 课程内容
            type: str = None    # 课程性质
        }
    一个示例投稿命令：
        #openwhu post 挑战2022高考数学全国卷 杜老师 {"comment":"笑死我了"}
    """
    guest_url = 'http://127.0.0.1:65472/api/v1'
    args = ent.chain.tostr().split(' ')
    if not len(args) or args[0] not in ('get', 'post'):
        return '格式错误: 期望输入操作命令(get或post)'
    if args[0] == 'get':
        if len(args) == 3:
            resp = requests.get(f'{guest_url}/post?course={args[1]}&teacher={args[2]}')
            if resp.status_code == 404:
                return '找不到该课程'
            elif resp.status_code == 200:
                j = resp.json()
                return f'''
课程名称：{j['course']}
任课教师：{j['teacher']}
共计评测数: {len(j['content'])}
                '''
            else:
                logger.critical(resp.status_code)
                logger.critical(resp.content)
                return '内部错误[backend]'
        elif len(args) == 4:
            resp = requests.get(f'{guest_url}/post/{args[3]}?course={args[1]}&teacher={args[2]}')
            if resp.status_code == 404:
                return '找不到该课程'
            elif resp.status_code == 500:
                return '内部错误[backend] 可能是数组越界'
            elif resp.status_code == 200:
                j = resp.json()
                output = []
                if tmp:=j.get('comment'): output.append(f'你的体验:{tmp}')
                if tmp:=j.get('score'): output.append(f'学分数量:{tmp}')
                if tmp:=j.get('scoring'): output.append(f'给分情况:{tmp}')
                if tmp:=j.get('material'): output.append(f'推荐教材:{"、".join(tmp)}')
                if tmp:=j.get('appendix'): output.append(f'补充说明:{tmp}')
                if tmp:=j.get('examination'): output.append(f'考核方式:{tmp}')
                if tmp:=j.get('intro'): output.append(f'课程内容:{tmp}')
                if tmp:=j.get('type'): output.append(f'课程性质:{tmp}')
                return '\n'.join(output)
            else:
                logger.critical(resp.status_code)
                logger.critical(resp.content)
                return '内部错误[backend]'
    elif args[0] == 'post':
        if len(args) < 4:
            return '格式错误：投稿参数不够'
        course, teacher, *js = args[1:]
        js = ' '.join(js)
        js = json.loads(js)
        resp = requests.post(f'{guest_url}/contrib', json={'c':{'course': course, 'teacher':teacher}, 'm': js})
        if resp.status_code == 200:
            return '投稿成功，注意投稿需要管理员审核后才会显示'
        else:
            logger.critical(resp.status_code)
            logger.critical(resp.content)
            return '投稿失败'
    return '请使用#h #openwhu查看用法'

functionMap = {
}

shortMap = {
}

functionDescript = {
}