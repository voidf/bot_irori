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
from GLOBAL import (At, Face, Image,
                    MessageChain, Plain, QQFaces,
                    importMirai)

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


def chkcfg(player):
    player = int(player)
    return GLOBAL.cfgs.setdefault(player,SessionConfigures(player))

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


async def contestsBeginNotice(g,contest,ti):
    if ti < 0:
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
用例：
    await msgDistributer(msg="https://i.pximg.net/img-original/img/2020/09/27/19/46/09/84651430_p0.jpg",typ="I",player=114514)
异步发送用例：
    asyncio.ensure_future(msgDistributer(msg="https://i.pximg.net/img-original/img/2020/09/27/19/46/09/84651430_p0.jpg",typ="I",player=114514))
也可以直接扔扔消息元素列表或者消息链(list)进来
用例：
    await msgDistributer(player=g,list=[At(mb),Plain(tit+'大限已至，我扔掉了。')])
    """
    def chkempty(seq):
        isempty = True
        # print(seq)
        # print(dir(seq))
        for ii in seq:
            print(ii)

            # for i in ii[1]:
            if isinstance(ii, Plain):
                if ii.text:
                    return False
            else:
                return False
        return True
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
        if chkempty(seq): return
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





def getCredit(user: int) -> int:
    """"获取给定用户的信用点
参数：
    [int]user(QQ号)
返回：
    [int]用户的信用点"""
    return CreditLog.chk(user).credit

def updateCredit(user: int, operator: str, val: int) -> bool: # 危
    """修改用户的信用点
参数：
    [int]user(QQ号)
    [str]operator(操作符)
    [int]val(操作数)
返回：
    [bool]是否操作成功
用例：
    updateCredit(114514, '+', 1) # 让
    """
    if operator not in GLOBAL.credit_operators: return False
    c = getCredit(user)
    c, c2 = evaluate_expression(f'{c}{operator}{int(val)}')
    c2 = c2.strip()
    CreditLog.chk(user).update(credit=int(c2))
    return True

def generateTmpFileName(pref='', ext='.png', **kwargs):
    """生成一个临时文件名"""
    return f'''tmp{pref}{randstr(GLOBAL.randomStrLength)}{ext}'''

async def compressMsg(l, extDict={}):
    """会把Plain对象展开，但同时也会打乱由图片，文字，回复等成分组成的混合消息链"""
    print(extDict)
    player = int(extDict.get("player",0))
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
        extDict['voices'] = [BaiduTTS(s)]
        extDict['-voice'] = True

    elif ('-fltts' in extDict or '-FLTTS' in extDict) and s:
        out = FLTTS(s, extDict['-fltts'])
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

def BaiduTTS(text: str) -> str:
    """拿百度TTS的链接"""
    return f'http://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&spd=5&text={text}'


def FLTTS(text, voice='slt') -> str:
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

from database_utils import *

def CFNoticeManager(j, feat:str, **kwargs):
    try:
        gp = kwargs['gp'].id
    except:
        gp = kwargs['gp']
    CFNoticeQueue = GLOBAL.CFNoticeQueueGlobal.setdefault(gp, {})
    print(f"INITING {gp} FOR {CFNoticeQueue}")
    for k,v in j.items():
        timew = None
        if k not in CFNoticeQueue:
            if 'routine' in v:
                timew = v['routine'] - tnow() - datetime.timedelta(hours=1)
                asy = asyncio.ensure_future(contestsBeginNotice(gp,v['title'],timew.total_seconds()))
                CFNoticeQueue[k] = asy
                asy.add_done_callback(functools.partial(clearCFFuture,k,gp))
        if timew and feat == 'R' and f"{k}RDR" not in CFNoticeQueue:
            asyR = asyncio.ensure_future(CFProblemRender(gp,k,timew.total_seconds()+3640))
            CFNoticeQueue[f"{k}RDR"]=asyR
            asyR.add_done_callback(functools.partial(clearCFFuture,f"{k}RDR",gp))
        elif feat == 'Y' and f"{k}RDR" in CFNoticeQueue:
            t = CFNoticeQueue.pop(f"{k}RDR")
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

# import warnings

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
