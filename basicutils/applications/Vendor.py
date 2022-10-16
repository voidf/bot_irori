"""临时开的转发接口类"""
import base64
import collections
from dataclasses import dataclass
import enum
import os
import pickle
import string
import sys

from async_timeout import timeout
from click import prompt

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
    """#约稿 [#waifu, #召唤, #产粮]
    ai画图，txt2img，容易被封所以还是建议优先直接用网页
    """
    ses = requests.session()
    authdir = 'waifusd_auth.pickle'
    apibase = 'http://127.0.0.1:7012'


    if os.path.exists(authdir):
        with open(authdir, 'rb') as f:
            usr, pw = pickle.load(f)
        ses.post(apibase+'/login', data={'username':usr,'password':pw})
    
    filter_p = re.compile('<.*?>', re.MULTILINE)
    def get_resolution(src):
        mc = re.compile('([0-9]+)[x\*]([0-9]+)').search(src)
        if mc:
            w, h = mc.groups()
            return int(w), int(h)
        else:
            return 512, 512

    def filter(src):
        b = []
        for i in filter_p.sub(' ', src).replace('\n', ' ').strip().replace('{', '(').replace('}', ')'):
            if b[-1:] == [' '] and ' ' == i:
                continue
            else:
                b.append(i)
        return ''.join(b)

    def parser(src):
        pm = [
            'prompt:', 'negative prompt:', 'steps:', 'sampler:', 'cfg scale:',
            'seed:', 'size:', 'model hash:', 'denoising strength:', 'clip skip:',
        ]
        b = [[] for i in pm]

        cur = b[0]
        p = 0

        def chk():
            nonlocal p
            nonlocal cur
            for ind, token in enumerate(pm):
                if src[p:p+len(token)].lower() == token:
                    p += len(token)
                    cur = b[ind]
                    return False
            return True

        while p < len(src):
            if chk():
                cur.append(src[p])
                p += 1
        for p, i in enumerate(b):
            b[p] = ''.join(i).strip().removesuffix(',')
        return {j:i for i, j in zip(b, pm) if i}

    rawinputs = ent.chain.tostr()
    if rawinputs == '样例':
        with open('Assets/waifusd/cn_cheatsheet_list.pkl', 'rb') as f:
            li = pickle.load(f)
        return random.choice(li)
    if rawinputs == '词汇表':
        with open('Assets/waifusd/cn_cheatsheet_dict.pkl', 'rb') as f:
            d = pickle.load(f)
        return '\n'.join(random.sample([f'{k}:{v}' for k, v in d.items()], 10))
    if rawinputs == '模板':
        return """((masterpiece)), best quality, illustration, 1 girl, beautiful,beautiful detailed sky, catgirl,beautiful detailed water, cinematic lighting, Ice Wings, (few clothes),loli,(small breasts),light aero blue hair, Cirno(Touhou), wet clothes,underwater,hold breath,bubbles,cat ears ,dramatic angle
Negative prompt: lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad feet, huge breasts
Steps: 75, Sampler: DDIM, CFG scale: 11, Seed: 3323485853, Size: 512x768, Model hash: e6e8e1fc, Clip skip: 2"""

    txt2img_inputs = collections.namedtuple('txt2img_inputs',
        field_names=[
            "prompt", "negative_prompt", "prompt_style", "prompt_style2", "steps",
            "sampler", "restore_faces", "tiling", "batch_count", "batch_size",
            "cfg_scale", "seed", "sub_seed", "subseed_strength", "seed_resize_from_h",
            "seed_resize_from_w", "unk_1", "height", "width", "highres_fix",
            "denoising_strength","firstpass_width","firstpass_height","script",
        ], defaults=[
            "loli", "nsfw", "None", "None", 30,
            "DDIM", False, False, 1, 1,
            7, -1, -1, 0, 0,
            0, False, 512, 512, False,
            0.85,0,0, "None",
        ])

    def nums(src):
        b = []
        for i in src:
            if i in string.digits+'-':
                b.append(i)
        return int(''.join(b))
    def floats(src):
        b = []
        for i in src:
            if i in string.digits+'.':
                b.append(i)
        return float(''.join(b))
    
    mapping_string = { # 迫真萃取
        float: floats,
        int: nums,
        str: lambda x: x
    }
    
    parsed = parser(filter(rawinputs))
    # model = txt2img_inputs()
    if len(parsed) > 1: # 有东西，高级模式
        modify = {}
        for k, v in parsed.items():
            pk = k[:-1].replace(' ', '_')
            if pk in txt2img_inputs._fields:
                modify[pk] = mapping_string[type(txt2img_inputs._field_defaults[pk])](v)

        if sz := parsed.get('size:', ''):
            w, h = get_resolution(sz)
            modify['width'] = w
            modify['height'] = h
        if 'denoising strength:' in parsed:
            modify['highres_fix'] = True
        model = txt2img_inputs(**modify)
    else: # 简易模式
        inp = parsed['prompt:']

        if re.compile(r'[\u4e00-\u9fa5]').search(parsed.get('prompt:', '')):
            import jieba
            with open('Assets/waifusd/cn_cheatsheet_dict.pkl', 'rb') as f:
                d = pickle.load(f)
            jieba.load_userdict('Assets/waifusd/cn_cheatsheet.dict')
            c = list(jieba.cut(inp))
            cn_neg_tokens = ['不要', '别']
            tokens = [
                [], []
            ]
            unk = []
            hint_position = 0

            for sp in c:
                if sp in cn_neg_tokens:
                    hint_position = 1
                else:
                    if v := d.get(sp):
                        tokens[hint_position].append(random.choice(v))
                    else:
                        unk.append(sp)

            w, h = get_resolution(inp)
            modify = {
                'width': w,
                'height': h,
                'prompt': ','.join(tokens[0]),
                'negative_prompt': ','.join(tokens[1]),
            }
            if '-d' in ent.meta or '-debug' in ent.meta:
                return f"modify={modify}, unk={unk}, c={c}"
            
        else:
            modify = {
                'prompt': inp,
                'negative_prompt': ''
            }
        modify['negative_prompt'] += ',nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry'
        modify['prompt'] += ',((masterpiece)), best quality, illustration, beautiful, beautiful detailed eyes'
        model = txt2img_inputs(**modify)
       
    args = model + (
        False, False, None, "", "Seed",
        "", "Nothing", "", True, False,
        False, None,
        "", # json like object
        ""  # html like object
    )
    req = ses.post(f"{apibase}/api/predict", json={'fn_index':13, 'data':args})
    j = req.json()['data']
    # return f"{req.request.body}\nj={j}"
    return [Image(url=f"{apibase}/file={j[0][0]['name']}"), Plain(filter(j[2]))]
    




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