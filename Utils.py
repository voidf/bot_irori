import asyncio
import base64
import copy
import datetime
import functools
import importlib
import json
import os
import random
import string
import sys
import traceback
from typing import *

import requests
from bs4 import BeautifulSoup
from PIL import Image as PImage
from PIL import ImageDraw, ImageFont
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import GLOBAL
from Fetcher import *
from GLOBAL import (ApplicationLaunched, ApplicationShutdowned, At, Broadcast,
                    Face, Friend, FriendMessage, Group, GroupMessage, Image,
                    Member, MessageChain, Mirai, Plain, QQFaces, Session,
                    Source, Voice, importMirai)

importMirai()

youbi = {
    1:'月曜日',
    2:'火曜日',
    3:'水曜日',
    4:'木曜日',
    5:'金曜日',
    6:'土曜日',
    7:'日曜日',
}

from GLOBAL import SessionConfigures


def chkcfg(player):return GLOBAL.cfgs.setdefault(player,SessionConfigures(player))

def getmem(mono): return mono.id if getattr(mono, 'id', None) else int(mono)

def getPlainText(p:Plain) -> str:
    """做v3和v4的Plain兼容"""
    if GLOBAL.py_mirai_version == 3: return p.toString()
    else: return p.asDisplay()

def getMessageChainText(m:MessageChain) -> str:
    """做v3和v4的MessageChain兼容"""
    if GLOBAL.py_mirai_version == 3: return m.toString()
    else: return m.asDisplay()

def generateImageFromFile(fn:str) -> Image:
    """v3和v4的本地文件兼容"""
    if GLOBAL.py_mirai_version == 3: return Image.fromFileSystem(fn)
    else: return Image.fromLocalFile(fn)


async def rmTmpFile(fi:str):
    await asyncio.sleep(60)
    os.remove(fi)

async def contestsBeginNotice(g,contest,ti):
    if ti<0:
        return
    print('进入等待队列，阻塞%f秒'%ti)
    await asyncio.sleep(ti)
    await msgDistributer(gp=g,msg=f'比赛{contest}还有不到一个小时就要开始了...')

async def CFProblemRender(g,cid,ti):
    FN='CF/%s.png' % cid
    print('在%f秒后渲染比赛'%ti+cid+'的问题图片')
    if cid in GLOBAL.CFRenderFlag or os.path.exists(FN): #有队列在做了
        await asyncio.sleep(ti)
        if not os.path.exists(FN):
            await asyncio.sleep(20)
        await msgDistributer(gp=g,msg=FN,typ='I')
    else:
        GLOBAL.CFRenderFlag.add(cid)
        await asyncio.sleep(ti)
        base = 'https://codeforces.com/contest/'+cid+'/problems'
        l = await renderHtml(base, FN)
        GLOBAL.CFRenderFlag.discard(ti)
        l.append(generateImageFromFile(FN))
        await msgDistributer(gp=g,list=l)

async def fuzzT(g,s,e,w=''):
    for _ in range(s,e):
        if _%10==0:
            await asyncio.sleep(0.2)
        await msgDistributer(gp=g,msg=f'{chr(_)}{_}{w}')
# from graia.application.message.chain import MessageChain
async def MessageChainSpliter(chain: list, **kwargs):
    """只在v4工作的函数，把消息链拆开，一条条发送"""
    if chain:
        if 'player' in kwargs:
            kwargs['player'] = int(kwargs['player'])
            if kwargs['player'] > 1<<39:
                for seq in chain:
                    await GLOBAL.app.sendGroupMessage(kwargs['player']-(1<<39), MessageChain.create([seq]).asSendable())
            else:
                for seq in chain:
                    await GLOBAL.app.sendFriendMessage(kwargs['player'], MessageChain.create([seq]).asSendable())
        elif 'gp' in kwargs:
            for seq in chain:
                await GLOBAL.app.sendGroupMessage(kwargs['gp'], MessageChain.create([seq]).asSendable())
        elif 'mem' in kwargs:
            for seq in chain:
                await GLOBAL.app.sendFriendMessage(kwargs['mem'], MessageChain.create([seq]).asSendable())

async def msgDistributer(**kwargs):
    """
    根据player号分发消息
    输入字典msg为源文本，typ标识其类型('E'表情,'I'图片文件目录,'P'普通文本)
    扩展了也可以扔消息元素列表(list)进来的功能
    用例await msgDistributer(player=g,list=[At(mb),Plain(tit+'大限已至，我扔掉了。')])
    """
    seq = []
    
    if 'msg' in kwargs and kwargs['msg']:
        if kwargs.get('typ','P') == 'E':
            seq = [Face(faceId=QQFaces[kwargs['msg']])]
        elif kwargs.get('typ','P') == 'I':
            # print(base64.b64decode(kwargs['msg']))
            try: # 这个try用来判断msg是不是可解码的b64
                base64.b64decode(kwargs['msg'])
                f_n = 'tmp'+randstr(8)
                with open(f_n,'wb') as f:
                    f.write(base64.b64decode(kwargs['msg']))
                asyncio.ensure_future(rmTmpFile(f_n))
                seq = [generateImageFromFile(f_n)]
                # seq = [generateImageFromFile(kwargs['msg'])]
            except:
                if kwargs['msg'][:4] == 'http':
                    r = requests.get(kwargs['msg'])
                    f_n = 'tmp'+randstr(8)
                    with open(f_n,'wb') as f:
                        f.write(r.content)
                    asyncio.ensure_future(rmTmpFile(f_n))
                    seq = [generateImageFromFile(f_n)]
                else:
                    seq = [generateImageFromFile(kwargs['msg'])]
        else:
            seq = [Plain(kwargs['msg'])]

    need_compress = True
    if 'list' in kwargs and kwargs['list']:
        if not seq and isinstance(kwargs['list'], MessageChain): 
            need_compress = False
            seq = kwargs['list']
        else:
            seq += kwargs['list']

    if need_compress: seq = await compressMsg(seq, extDict=kwargs)
    print(f'\n{seq}\n')
    if seq:
        if 'player' in kwargs:
            kwargs['player'] = int(kwargs['player'])
            if kwargs['player'] > 1<<39:
                await GLOBAL.app.sendGroupMessage(kwargs['player']-(1<<39), seq)
            else:
                await GLOBAL.app.sendFriendMessage(kwargs['player'], seq)
        elif 'gp' in kwargs:
            await GLOBAL.app.sendGroupMessage(kwargs['gp'], seq)
        elif 'mem' in kwargs:
            await GLOBAL.app.sendFriendMessage(kwargs['mem'], seq)
        
async def msgSerializer(_i, **kwargs):
    p = getPlayer(**kwargs)
    rate = GLOBAL.RUSHRATE.get(p,1)
    print(_i)
    if 'note' in _i:
        await msgDistributer(msg=_i['note'], **kwargs)
    if 'msg' in _i:
        if _i.get('typ', 'P') != 'I':
            await asyncio.sleep(len(_i['msg'])/5/rate)
        await msgDistributer(**_i, **kwargs)
    if 'MORE' in _i and 'note' in _i['MORE']:
        await msgDistributer(typ='P',msg=_i['MORE']['note'],**kwargs)

                
def smart_decorator(decorator):
    def decorator_proxy(func=None, **kwargs):
        if func is not None:
            return decorator(func=func, **kwargs)
        def decorator_proxy(func):
            return decorator(func=func, **kwargs)
        return decorator_proxy
    return decorator_proxy

def tnow(): return datetime.datetime.utcnow() + datetime.timedelta(hours=8)

binocular_calculate_map = {
    '+': lambda x,y:x+y,
    '-': lambda x,y:x-y,
    '*': lambda x,y:x*y,
    '/': lambda x,y:x/y,
    '=': lambda x,y:x is y,
    '==': lambda x,y:x==y,
    '//': lambda x,y:x//y,
    '%': lambda x,y:x%y,
    '&&': lambda x,y:x and y,
    '&': lambda x,y:x&y,
    '||': lambda x,y:x or y,
    '|': lambda x,y:x|y,
    '^': lambda x,y:x^y,
    '**': lambda x,y:x**y,
    '<<': lambda x,y:x<<y,
    '<': lambda x,y:x<y,
    '>>': lambda x,y:x>>y,
    '>': lambda x,y:x>y
}

unary_calculate_map = {
    '-': lambda x:-x,
    '~': lambda x:~x
}


def evaluate_expression(exp: str) -> str:
    """处理不带空格和其他空字符的中缀表达式"""
    operators = [] # 除括号和单目外，优先级单调递增
    operands = []
    operands_str = []
    x = []
    xx = []
    xpower = []

    suffix_exp = [] # 放2元组(本体, 类型)罢了

    last_mono = 'ope'
    cur_operator = '' # 只放双目
    float_token = False
    decimal_token = False
    hex_token = False
    octal_token = False
    binary_token = False
    complex_token = False

    def binocular_calculate(f: str, op):
        A = op.pop()
        B = op.pop()
        op.append(binocular_calculate_map[f](B,A))
        print("bino calculated:", op[-1])
    def unary_calculate(f: str, op):
        A = op.pop()
        op.append(unary_calculate_map[f](A))
        print("unary calculated:", op[-1])
    def binocular_concate(f: str, op):
        A = op.pop()
        B = op.pop()
        op.append(f"({B}{f}{A})")
        print("bino concated:", op[-1])
    def unary_concate(f: str, op):
        A = op.pop()
        op.append(f"({f}{A})")
        print("unary concated:", op[-1])

    def handle_operand():
        nonlocal x, xx, suffix_exp, float_token, complex_token, last_mono, decimal_token, xpower
        nonlocal hex_token,octal_token,binary_token
        handled = ''.join(x)
        if float_token:
            handled += '.' + ''.join(xx)
        if decimal_token:
            handled += 'e' + ''.join(xpower)
        if complex_token:
            handled += 'j'
        if handled:
            print(f'Handled operand:{handled}')
            if hex_token:
                t = int(handled, 16)
            elif octal_token:
                t = int(handled, 8)
            elif binary_token:
                t = int(handled, 2)
            elif complex_token:
                t = complex(handled)
            elif float_token or decimal_token or len(handled) > 1000:
                t = float(handled)
            else:
                t = int(handled)
            suffix_exp.append((t, 'operand'))
            last_mono = 'num'
        float_token = False
        complex_token = False
        decimal_token = False
        hex_token = False
        octal_token = False
        binary_token = False
        x = []
        xx = []
        xpower = []


    def calculate_suffix_exp():
        nonlocal operands_str
        operands_str = copy.deepcopy(operands)
        for op, typ in suffix_exp:
            # op, typ = suffix_exp.pop()
            if typ == 'operand':
                operands.append(op)
            elif typ == 'unary':
                unary_calculate(op, operands)
                unary_concate(op, operands_str)
            else:
                binocular_calculate(op, operands)
                binocular_concate(op, operands_str)
    def maintain_stack():
        nonlocal cur_operator
        if cur_operator != '(':
            while operators:
                if operators[-1][1] == 'unary':
                    suffix_exp.append(operators.pop())
                else:
                    if GLOBAL.binocular_operators[operators[-1][0]] >= GLOBAL.binocular_operators[cur_operator]:
                        suffix_exp.append(operators.pop())
                    else:
                        break
        operators.append((cur_operator, 'binocular'))
        cur_operator = ''

    for c in exp:
        if c == '-' and decimal_token and not xpower:
            xpower.append(c)
        elif c == 'b' and x == ['0']:
            binary_token = True
            x.append(c)
        elif c == 'o' and x == ['0']:
            octal_token = True
            x.append(c)
        elif c == 'x' and x == ['0']:
            hex_token = True
            x.append(c)
        elif c in 'abcdefABCDEF' and hex_token:
            x.append(c)
        elif c in '.je' + string.digits:
            if cur_operator:
                maintain_stack()
                last_mono = 'ope'
            if c == '.':
                float_token = True
            elif c == 'j':
                complex_token = True
            elif c == 'e':
                decimal_token = True
            elif c in string.digits:
                if decimal_token:
                    xpower.append(c)
                elif float_token:
                    xx.append(c)
                else:
                    x.append(c)
        else:
            handle_operand()
            if c == ')':
                while operators[-1][0]!='(':
                    suffix_exp.append(operators.pop())
                operators.pop()
                last_mono = 'num'

            elif cur_operator in GLOBAL.binocular_operators and c in ('-', '~'):
                maintain_stack()
                operators.append((c, 'unary'))
                last_mono = 'ope'
            elif cur_operator in GLOBAL.binocular_operators and c == '(':
                maintain_stack()
                operators.append((c, 'binocular'))
                last_mono = 'ope'
            elif last_mono == 'ope' and c in ('-', '~'):
                operators.append((c, 'unary'))
            elif last_mono == 'ope' and c == '(':
                operators.append((c, 'binocular'))    
            elif cur_operator + c in GLOBAL.binocular_operators:
                cur_operator += c

    handle_operand()

    if cur_operator:
        maintain_stack()
        operators.append((cur_operator, 'binocular'))

    while operators:
        suffix_exp.append(operators.pop())
    print(suffix_exp)
    calculate_suffix_exp()
    return str(operands[0]) + '\n' + str(operands_str)


def getCredit(user: int):
    if not os.path.exists(f'credits/{user}'):        
        return 500
    else:
        with open(f'credits/{user}', 'r') as f:
            return int(f.read().strip())

def updateCredit(user: int, operator: str, val: int): # 危
    if operator not in GLOBAL.credit_operators: return False
    c = getCredit(user)
    # c = eval(f'{c}{operator}{int(val)}')
    c = evaluate_expression(f'{c}{operator}{int(val)}')
    with open(f'credits/{user}', 'w') as f:
        f.write(f'{c}')
    return True

def generateTmpFileName(pref='', ext='.png', **kwargs):
    return f'''tmp{pref}{randstr(GLOBAL.randomStrLength)}{ext}'''

async def compressMsg(l, extDict={}):
    """会把Plain对象展开，但同时也会打乱由图片，文字，回复等成分组成的混合消息链"""
    print(extDict)
    player = extDict.get("player",0)
    tc = chkcfg(player)
    
    nl = []
    others = []
    for i in l:
        if isinstance(i,Plain):
            nl.append(getPlainText(i))
        else:
            others.append(i)
    s = ''.join(nl)

    if ('-tts' in extDict or '-TTS' in extDict) and s:
        out = TTS(s, extDict['-tts'])
        byte = getFileBytes(out)
        voi = await GLOBAL.app.uploadVoice(byte)
        asyncio.ensure_future(MessageChainSpliter([voi], **extDict))

    if "-paste" in extDict and s:

        data = {
            "poster":"irori",
            "syntax": extDict.get("-syntax", "text"),
            "expiration":"day",
            "content":s
        }
        # asyncio.ensure_future(msgDistributer(list=[Plain(requests.post("https://paste.ubuntu.com/", data=data).url)], **extDict))
        l = [Plain(requests.post("https://paste.ubuntu.com/", data=data).url)] + others
    elif len(s) > tc.compress_threshold or "-force-image" in extDict or "-fi" in extDict:
        A = int(extDict.get("-A", 255))
        try:
            theme = extDict.get("-t", "0xFF")
            theme = extDict.get("-theme", theme)
            theme = int(theme, 16)
            R = (theme & 0xFF0000) >> 16
            G = (theme & 0x00FF00) >> 8
            B = theme & 0xFF
        except TypeError: pass
        except: traceback.print_exc()
        finally:
            theme = int(extDict.get("-t", 255))
            theme = int(extDict.get("-theme", theme))
            R = 255-theme
            G = 255-theme
            B = 255-theme
        offset = tc.font_size >> 1
        font = ImageFont.truetype('Assets/sarasa-gothic-ttf-0.12.5/sarasa-ui-tc-bold.ttf',GLOBAL.compressFontSize)
        sl = s.split('\n')
        height = len(sl)
        width = 0
        for i in sl:
            width = max(width,len(i))

        layer2 = PImage.new(
            'RGBA',
            (width * (GLOBAL.compressFontSize), (height) * (GLOBAL.compressFontSize +offset)),
            (R, G, B, A)
        )
        p = generateTmpFileName('ZIP')
        # PImage.alpha_composite(nyaSrc,layer2).save(p)
        draw = ImageDraw.Draw(layer2)

        for column,txt in enumerate(sl):
            draw.text((offset>>1,   column * ((offset)+GLOBAL.compressFontSize)), txt, (theme,theme,theme,255), font)
        layer2.save(p)
        asyncio.ensure_future(rmTmpFile(p))
        l = [generateImageFromFile(p)] + others
        
    
    if GLOBAL.py_mirai_version == 3:
        return l
    else:
        if "-voice" in extDict and "voices" in extDict: # 不能超过1M
            print(extDict['voices'])
            for i in extDict['voices']:
                fn = generateTmpFile(getFileBytes(i), fm=extDict.get('voices-fm', 'mp3'))
                limit_conf = {
                    'crop': limitAudioSizeByCut,
                    'quan': limitAudioSizeByBitrate,
                    'default': nolimitAudioSize
                }
                out = limit_conf[extDict.get('-lim', 'default')](fn)
                byte = getFileBytes(out)
                voi = await GLOBAL.app.uploadVoice(byte)
                # print(f"voi ===> {voi}")
                asyncio.ensure_future(MessageChainSpliter([voi], **extDict))
        if not l: return False
        return MessageChain.create(l).asSendable()

import shlex


def TTS(text, voice='slt') -> str:
    v = voice if voice in {
        'awb',
        'kal',
        'kal16',
        'rms',
        'slt'
    } else 'slt'
    dst = generateTmpFileName(ext='.amr')
    t = "" if "'" in text else "'"
    print(f'''ffmpeg -f lavfi -i flite=text={t}{shlex.quote(text)}{t}:voice={shlex.quote(v)} -codec amr_nb -ac 1 -ar 8000 {dst}''')
    os.system(f'''ffmpeg -f lavfi -i flite=text={t}{shlex.quote(text)}{t}:voice={shlex.quote(v)} -codec amr_nb -ac 1 -ar 8000 {dst}''')
    asyncio.ensure_future(rmTmpFile(dst))
    return dst

def generateTmpFile(b: bytes, fm='png') -> str:
    """生成一个30s后会删掉的临时文件"""
    fn = generateTmpFileName(ext=f'.{fm}')
    with open(fn, 'wb') as f:
        f.write(b)
    asyncio.ensure_future(rmTmpFile(fn))
    return fn
    
import platform


def nolimitAudioSize(src) -> str:
    dst = generateTmpFileName(ext='.amr')
    if src[-3:] == "mid" and platform.system() != 'Windows':
        os.system(f'timidity {src} -Ow -o - | ffmpeg -y -i - -codec amr_nb -ac 1 -ar 8000 {dst}')
    else:
        os.system(f'ffmpeg -y -i {src} -codec amr_nb -ac 1 -ar 8000 {dst}')
    asyncio.ensure_future(rmTmpFile(dst))
    return dst

def limitAudioSizeByBitrate(src) -> str:
    """依赖ffmpeg，生成一个临时文件，全 损 音 质"""
    # lim = 8 * 1024 # 即1MB，大于1M发不出去
    lim = 8000
    dst = generateTmpFileName(ext='.amr')
    dur = os.popen(f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {src}').read()
    dur = float(dur)
    print(dur)
    if src[-3:] == "mid" and platform.system() != 'Windows':
        os.system(f'timidity {src} -Ow -o - | ffmpeg -y -i - -codec amr_nb -ac 1 -ar 8000 -b:a {lim / dur}k {dst}')
    else:
        os.system(f'ffmpeg -y -i {src} -codec amr_nb -ac 1 -ar 8000 -b:a {lim / dur}k {dst}')
    asyncio.ensure_future(rmTmpFile(dst))
    return dst

def limitAudioSizeByCut(src) -> str:
    """超出部分会被剪掉"""
    dst = generateTmpFileName(ext='.amr')
    if src[-3:] == "mid" and platform.system() != 'Windows':
        os.system(f'timidity {src} -Ow -o - | ffmpeg -y - -codec amr_nb -ac 1 -ar 8000 -fs 1000K {dst}')
    else:
        os.system(f'ffmpeg -y -i {src} -codec amr_nb -ac 1 -ar 8000 -fs 1000K {dst}')
    asyncio.ensure_future(rmTmpFile(dst))
    return dst

def getFileBytes(s):
    if isinstance(s, bytes):
        return s
    elif s[:4] == 'http':
        ret = requests.get(s).content
        print(len(ret))
        return ret
    else:
        with open(s, 'rb') as f:
            return f.read()

def getPlayer(**kwargs) -> int:
    """根据不定字典拿player号"""
    if 'player' in kwargs: return int(kwargs['player'])
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
    return int(player)



def clearCFFuture(key,G,src):
    """
    第一个参数是比赛唯一标号，第二个是群组号用于在dict中确认
    第三个参数是来源函数，因为这个函数是在来源callback调用的，
    那么在这之前来源已经被执行完了，因此不用cancel，直接从dict中删去即可
    """
    CFNoticeQueue = GLOBAL.CFNoticeQueueGlobal.setdefault(G,{})
    try:print('清除成功',CFNoticeQueue.pop(key))
    except:
        traceback.print_exc()
        print(f'{key}中无比赛{G}的提醒日程')

def clearOTFuture(key,G,src):
    """
    第一个参数是比赛唯一标号，第二个是群组号用于在dict中确认
    第三个参数是来源函数，因为这个函数是在来源callback调用的，
    那么在这之前来源已经被执行完了，因此不用cancel，直接从dict中删去即可
    """
    t = GLOBAL.OTNoticeQueueGlobal.setdefault(G,{})
    try:print('清除成功',t.pop(key))
    except:
        traceback.print_exc()
        print(f'{key}中无比赛{G}的提醒日程')

def CFNoticeManager(j,**kwargs):
    try:
        gp = kwargs['gp'].id
    except:
        gp = kwargs['gp']
    fn = f"CF/{gp}"
    with open(fn,'r') as f:
        feat = f.readline().strip()
    CFNoticeQueue = GLOBAL.CFNoticeQueueGlobal.setdefault(gp,{})
    print(f"INITING {gp} FOR {CFNoticeQueue}")
    for k,v in j.items():
        timew = None
        if k not in CFNoticeQueue:
            if 'routine' in v:
                timew = v['routine'] - tnow() - datetime.timedelta(hours=1)
                asy = asyncio.ensure_future(contestsBeginNotice(gp,v['title'],timew.total_seconds()))
                CFNoticeQueue[k] = asy
                asy.add_done_callback(functools.partial(clearCFFuture,k,gp))
        if timew and feat == 'R' and k + 'RDR' not in CFNoticeQueue:
            asyR = asyncio.ensure_future(CFProblemRender(gp,k,timew.total_seconds()+3640))
            CFNoticeQueue[k + 'RDR']=asyR
            asyR.add_done_callback(functools.partial(clearCFFuture,k + 'RDR',gp))
        elif feat == 'Y' and k + 'RDR' in CFNoticeQueue:
            t = CFNoticeQueue.pop(k + 'RDR')
            t.cancel()

def OTNoticeManager(j,**kwargs):
    try:
        gp = kwargs['gp'].id
    except:
        gp = kwargs['gp']
    OtherOJNoticeQueue = GLOBAL.OTNoticeQueueGlobal.setdefault(gp,{})
    for k in j:
        if k['title'] not in OtherOJNoticeQueue:
            timew = k['begin'] - tnow() - datetime.timedelta(hours=1)
            asy = asyncio.ensure_future(contestsBeginNotice(gp,k['title'],timew.total_seconds()))
            OtherOJNoticeQueue[k['title']] = asy
            asy.add_done_callback(functools.partial(clearOTFuture,k['title'],gp))
    print(OtherOJNoticeQueue)




async def renderHtml(dst_lnk, na) -> str:
    """渲染dst_lnk的网页，保存为na，返回网页标题"""
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
    scroll_width = driver.execute_script(
        'return document.body.parentNode.scrollWidth')
    scroll_height = driver.execute_script(
        'return document.body.parentNode.scrollHeight')
    if scroll_height*scroll_width > GLOBAL.webPngLimit:
        if scroll_width >= GLOBAL.webPngLimit:
            driver.quit()
            ostr.append(Plain(text='我画不了这么鬼畜的页面OxO'))
            return ostr
        else:
            if 'codeforces' in dst_lnk:
                scroll_height = min(GLOBAL.webPngLimit*10 //
                                    scroll_width, scroll_height)
            else:
                scroll_height = GLOBAL.webPngLimit//scroll_width
    if 'moegirl' in dst_lnk:
        driver.execute_script(
            '''var o=document.querySelectorAll('.heimu');for(var i=0;i<o.length;i++){o[i].style.color="#FFF"}''')
        driver.execute_script(
            '''var o=document.querySelectorAll('a');for(var i=0;i<o.length;i++){o[i].style.color="#0AF"}''')
    driver.set_window_size(scroll_width, scroll_height)
    driver.get_screenshot_as_file(na)
    driver.quit()
    return ostr

import warnings

# def uploadToChaoXing(fn: Union[bytes,str]) -> str:
#     warnings.warn("超星网盘现在要登录了", DeprecationWarning)
#     lnk = 'https://notice.chaoxing.com/pc/files/uploadNoticeFile'
#     if isinstance(fn,bytes):
#         r = requests.post(lnk,files = {'attrFile':fn})
#     else:
#         with open(fn,'rb') as f:
#             r = requests.post(lnk,files = {'attrFile':f})
#     j = json.loads(r.text)
#     return j['att_file']['att_clouddisk']['downPath']

# 数论相关

def comb(n,b):
    res = 1
    b = min(b,n-b)
    for i in range(b):
        res=res*(n-i)//(i+1)
    return res

def quickpow(x,p,m = -1):
    res = 1
    if m == -1:
        while p:
            if p&1:
                res = res * x
            x = x * x
            p>>=1
    else:
        while p:
            if p&1:
                res = res * x % m
            x = x * x % m
            p>>=1
    return res

def A000110_list(m, mod=0): # 集合的划分数
    mod = int(mod)
    A = [0 for i in range(m)]
    # m -= 1
    A[0] = 1
    # R = [1, 1]
    for n in range(1, m):
        A[n] = A[0]
        for k in range(n, 0, -1):
            A[k-1] += A[k]
            if mod: A[k-1] %= mod
        # R.append(A[0])
    # return R
    return A[0]

def exgcd(a,b):
    if not b:
        return 1,0
    y,x = exgcd(b,a%b)
    y -= a//b * x
    return x,y

def getinv(a,m):
    x,y = exgcd(a,m)
    return -1 if x==1 else x%m
    
# 树巨结垢相关

def lowbit(x:int): return x&-x

def treearray_update(pos:int,x:int,array:list):
    while pos < len(array):
        array[pos] += x
        pos += lowbit(pos)

def treearray_getsum(pos:int,array:list) -> int:
    ans = 0
    while pos > 0:
        ans += array[pos]
        pos -= lowbit(pos)
    return ans

def calcinvs(array:list):
    d = {}
    for k,v in enumerate(sorted(array)):
        d[v] = k+1
    treearray = [0 for i in range(1+len(array))]
    invs = 0
    for i in array:
        invs += treearray_getsum(len(treearray)-1, treearray) - treearray_getsum(d[i], treearray)
        treearray_update(d[i],1,treearray)
    return invs


