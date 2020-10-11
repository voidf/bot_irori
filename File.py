import GLOBAL
from bs4 import BeautifulSoup
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
import urllib
import mido
from Utils import *
importMirai()

def 投票姬(*attrs,**kwargs):
    mem = str(getattr(kwargs['mem'],'id',kwargs['mem']))
    gp = str(getattr(kwargs['mem'],'id',kwargs['mem']))
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
            await msgDistributer(player=g,list=[At(mb),Plain(kotoba)])
        else:
            await msgDistributer(player=g,list=[Plain(kotoba)])

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
                        await msgDistributer(player=g,list=[At(mb),Plain(tit+'大限已至，我扔掉了。')])
                    else:
                        await msgDistributer(player=g,list=[At(mb),Plain(tit+'变臭力，只能扔了（悲')])
                else:
                    if random.randint(0,4):
                        await msgDistributer(player=g,list=[Plain(tit+'大限已至，我扔掉了。')])
                    else:
                        await msgDistributer(player=g,list=[Plain(tit+'变臭力，只能扔了（悲')])
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

    if 'recover' in kwargs:
        ddlQueuer = GLOBAL.ddlQueuerGlobal.setdefault(kwargs['gp'],{})
        notice2(kwargs['gp'],kwargs['mb'],kwargs['tit'],kwargs['dtime'])
        return
    else:
        player = getPlayer(**kwargs)
        ddlQueuer = GLOBAL.ddlQueuerGlobal.setdefault(player,{})

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
                    j[s] = [','.join(ss),getattr(kwargs['mem'],'id',kwargs['mem'])]
                    notice2(player,getattr(kwargs['mem'],'id',kwargs['mem']),s,dt)
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
    
def 电笔记(*attrs,**kwargs):
    ins = ' '.join(attrs)
    if ins == 'reload':
        ret_msg = [Plain('知识库已更新,现有词条：\n')]
        for i in os.listdir('DigitalElectronicsTech'):
            if i[-6:]=='.json5':
                with open('DigitalElectronicsTech/'+i,'r') as f: 
                    j = json5.load(f)
                for k,v in j.items():
                    ret_msg.append(Plain('\t- '+k+'\n'))
                    GLOBAL.DEKnowledge[k] = [Plain(f'''{k}\n别名:{v['AN']}\n{v['desc']}''')]
                    if 'img' in v:
                        for vi in v['img']:
                            GLOBAL.DEKnowledge[k].append(generateImageFromFile('DigitalElectronicsTech/img/'+vi))
                    for an in v['AN']:
                        GLOBAL.DEKnowledge[an] = GLOBAL.DEKnowledge[k]
        return ret_msg
    elif ins in GLOBAL.DEKnowledge:
        return GLOBAL.DEKnowledge[ins]
    else:
        return [Plain('不存在此条目')]

def 在线P歌(*attrs,**kwargs):
    m = mido.MidiFile()
    t = mido.MidiTrack()
    m.tracks.append(t)

    note_map = {
        'C':0,
        'C#':1,
        'D':2,
        'D#':3,
        'E':4,
        'F':5,
        'F#':6,
        'G':7,
        'G#':8,
        'A':9,
        'A#':10,
        'B':11
    }

    t.append(mido.MetaMessage('set_tempo', tempo=500000, time=0)) #bpm=120
    t.append(mido.MetaMessage('track_name', name='Piano_1', time=0))

    #track.append(mido.Message('program_change', program=1, time=0)) 设置音色

    for i in '\n'.join(attrs).split('\n'):
        if i and i != '0':
            note = note_map[i[:-1]]+int(i[-1])*12
            t.append(mido.Message('note_on', note=note, velocity=120, time=0))
            t.append(mido.Message('note_off', note=note, velocity=120, time=480))
        else:
            t.append(mido.Message('note_on', note=60, velocity=0, time=0))
            t.append(mido.Message('note_off', note=60, velocity=0, time=480))
    fn = f'tmp{randstr(4)}.mid'
    m.save(fn)
    asyncio.ensure_future(rmTmpFile(fn))
    return [Plain(uploadToChaoXing(fn))]

def 仿洛谷每日签到(*attrs,**kwargs):
    print(kwargs['mem'])
    print(dir(kwargs['mem']))
    mem = getattr(kwargs['mem'],'id',int(kwargs['mem']))
    fn = f'DailySign/{mem}'
    from Assets.洛谷签到语料 import 宜, 忌, 运势
    if not os.path.exists('DailySign'): os.mkdir('DailySign')
    if not os.path.exists(fn): 
        with open(fn,'w') as f: json.dump({},f)
    with open(fn,'r') as f: current_user = json.load(f)
    def to_datetime(s): return datetime.datetime.strptime('%Y-%m-%d', s)
    if current_user.get('last_sign','1919-8-10') != datetime.datetime.now().strftime('%Y-%m-%d'):
        if to_datetime(current_user.get('last_sign','1919-8-10')) != to_datetime(datetime.datetime.now().strftime('%Y-%m-%d')) - datetime.timedelta(days=1):
            current_user['combo'] = 0
        current_user['combo'] = current_user.get('combo', 0) + 1
        fortune = random.choice(运势)
        y = random.sample(宜.items(),2)
        t忌 = copy.deepcopy(忌)
        t忌.pop(y[0][0],(0,False))
        t忌.pop(y[1][0],(0,False))
        j = random.sample(t忌,2) # 防重
        if fortune in ('大吉','特大吉'): j = [('万事皆宜')]
        if fortune in ('大凶'): y = [('诸事不宜')]
        for p,i in enumerate(y): y[p] = '\t'.join(i)
        for p,i in enumerate(j): j[p] = '\t'.join(i)
        ans = f"{fortune}\n\n宜:\n{chr(10).join(y)}\n\n忌:\n{chr(10).join(j)}\n\n您已连续求签{current_user['combo']}天"
        current_user['info'] = ans
        current_user['last_sign'] = datetime.datetime.now().strftime('%Y-%m-%d')
    return [Plain(current_user['info'])]

FileMap = {
    '#ddl':ddl通知姬,
    '#vote':投票姬,
    '#i电':电笔记,
    '#P歌':在线P歌,
    '#求签':仿洛谷每日签到
}

FileShort = {
    '#iee':'#i电',
    '#P':'#P歌'
}

FileDescript = {
    '#求签':'用来获得你的今日运势（从洛谷收集的语料（别迷信了，真的',
    '#vote':
"""
因为群投票限制15个选项所以整了这个计票姬
格式：
    #vote <对象名> （向指定的投票对象投票）
    #vote new <对象名> （新建指定名称的投票候选对象）
    #vote chk （检查目前的投票结果）
    #vote rm <对象名> （删除指定名称的投票对象）
    #vote limit <每人限票数> （设置每个人最多能投几票）
例：
    #vote 千与千寻
""",
    '#ddl':
"""
防侠提醒器，可用参数：
    new <事件名称> <到期时间[年,][月,][日,][时,][分,]<秒>>（新建事件）
    del <事件名称>（删除事件）
    ls（列出事件）
    使用new时注意需传入时间，格式年,月,日,时,分,秒；秒必填，其余不填则按照现在的时间自动补齐
例:
    #ddl new 打pcr 10,00,00
    即在今天10点设置提醒
""",
    '#i电':
"""
查查某些集成电路的手册（自己整理的
可用参数:
    reload (热重载知识库)
用例:
    #i电 74283
""",
    '#P歌':
"""
传入音符，合成midi
例：
    #P歌 C5 C5 G5 G5 A6 A6 G5
TODO:
    加入音长，音量设置
"""
}