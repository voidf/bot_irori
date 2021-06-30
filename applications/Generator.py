"""生成器类"""
import os
if __name__ == '__main__':
    os.chdir('..')
import GLOBAL
from bs4 import BeautifulSoup
from PIL import ImageFont,ImageDraw
from PIL import Image as PImage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.parse import quote
import re
import asyncio
import requests
import json5
import json
import numpy
import random
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
import GLOBAL
from Utils import *
importMirai()

async def 不会吧(*attrs,kwargs={}):
    return [Plain(f'不会真的有人{" ".join(attrs)}吧？不会吧不会吧？')]

async def 营销生成器(*attrs,kwargs={}):
    try:
        subject = attrs[0]
        event = attrs[1]
        event2 = attrs[2]
        synthesis = f'''{subject}{event}是怎么回事呢？{subject}相信大家都很熟悉，但是{subject}{event}是怎么回事呢，下面就让小编带大家一起了解吧。\r\n{subject}{event}，其实就是{event2}，大家可能会很惊讶{subject}怎么会{event}呢？但事实就是这样，小编也感到非常惊讶。\r\n这就是关于{subject}{event}的事情了，大家有什么想法呢，欢迎在评论区告诉小编一起讨论哦！'''
        return [Plain(synthesis)]
    except Exception as e:
        return [Plain(str(e))]

async def 同学你好生成器(*attrs,kwargs={}):
    try:
        if len(attrs)==1:
            ato = attrs[0]
            subject = '直播学习'
        elif len(attrs)>1:
            subject = attrs[0]
            ato = ' '.join(attrs[1:])
        else:
            return [Plain('参数不足，用法：【可选的群名】 【必选的教什么东西】')]
        pattern1 = ['同学你好','你好呀']
        synthesis = f'''{random.choice(pattern1)}，就是我建了个{subject}群，教{ato}等滴不用拉人和宣传，有兴趣学下的话给你群号阔以吧？'''
        return [Plain(synthesis)]
    except Exception as e:
        return [Plain(str(e))]

async def 这么臭的函数有必要定义吗(*attrs,kwargs={}):

    def 最小(数):
        左 = 0
        右 = len(GLOBAL.恶臭键值)-1
        中 = (左+右+1) >> 1
        while 左<右:
            if 数>=GLOBAL.恶臭键值[中]:
                左 = 中
            else:
                右 = 中-1
            中 = (左+右+1) >> 1
        return GLOBAL.恶臭键值[左]

    def 恶臭递归(恶臭数):
        if 恶臭数<0:
            return '-'+恶臭递归(-恶臭数)
        恶臭串 = str(恶臭数)
        正则 = re.compile(r'''\.\d+''')
        if re.search(正则,恶臭串) is not None:
            长 = re.search(正则,恶臭串).span()
            长 = 长[1] - 长[0] - 1
            return '('+恶臭递归(int(恶臭数*10**长)) + ')/('+恶臭递归(10**长) +')'
            
        if 恶臭数 in GLOBAL.恶臭字典:
            return GLOBAL.恶臭字典[恶臭数]
        除 = 最小(恶臭数)
        print('num=>',恶臭数,'\t','div=>',除)
        
        return str(f'({GLOBAL.恶臭字典[除]}*{恶臭递归(恶臭数//除)}+{恶臭递归(恶臭数%除)})')

    try:
        try:
            待证数 = int(attrs[0])
        except:
            待证数 = float(attrs[0])
            if 待证数 == 1e114514:
                raise NameError('粪味溢出')
        return [Plain(恶臭递归(待证数))]
    except Exception as e:
        print(e)
        return [Plain('这么恶臭的字串有必要论证吗')]

async def 猫图生成器(*attrs, kwargs={}):
    font = ImageFont.truetype('Assets/sarasa-gothic-ttf-0.12.5/sarasa-ui-tc-bold.ttf',18)
    nyaSrc = PImage.open('Assets/nya.png').convert('RGBA')
    layer2 = PImage.new('RGBA',nyaSrc.size,(255,255,255,0))
    draw = ImageDraw.Draw(layer2)
    
    text = ' '.join(attrs)
    beginPixel = (34-len(text)*9,55)

    draw.text(beginPixel,text,fill=(0,0,0,255),font=font)
    p = generateTmpFileName('Nya')

    PImage.alpha_composite(nyaSrc,layer2).save(p)
    asyncio.ensure_future(rmTmpFile(p),loop=None)
    return [generateImageFromFile(p)]

async def 优质解答生成器(*attrs, kwargs={}):
    font = ImageFont.truetype('Assets/sarasa-gothic-ttf-0.12.5/sarasa-ui-tc-bold.ttf',25)
    nyaSrc = PImage.open('Assets/answer.jpg').convert('RGBA')
    layer2 = PImage.new('RGBA',nyaSrc.size,(255,255,255,0))
    draw = ImageDraw.Draw(layer2)
    
    text = ' '.join(attrs)
    beginPixel = (50,120)

    draw.text(beginPixel,text,fill=(0,0,0,255),font=font)
    p = generateTmpFileName('Ans')

    PImage.alpha_composite(nyaSrc,layer2).save(p)
    asyncio.ensure_future(rmTmpFile(p),loop=None)
    return [generateImageFromFile(p)]

async def 自己不會百度嗎(*attrs, kwargs={}): return [Plain(f"http://iwo.im/?q={quote(' '.join(attrs))}")]

async def IPlay生成器(*attrs, kwargs={}):
    font = ImageFont.truetype('Assets/sarasa-gothic-ttf-0.12.5/sarasa-ui-tc-bold.ttf',25)
    Src = PImage.open('Assets/IPlayRhythmGame.png').convert('RGBA')
    layer2 = PImage.new('RGBA',Src.size,(255,255,255,0))
    draw = ImageDraw.Draw(layer2)
    
    text = ' '.join(attrs)
    beginPixel = (308,1004)

    draw.text(beginPixel,text,fill=(255,255,255,255),font=font)
    p = generateTmpFileName('IPlay')

    PImage.alpha_composite(Src,layer2).save(p)
    asyncio.ensure_future(rmTmpFile(p))
    return [generateImageFromFile(p)]
    
async def 希望没事生成器(*attrs, kwargs={}):
    font = ImageFont.truetype('Assets/sarasa-gothic-ttf-0.12.5/sarasa-ui-tc-bold.ttf',100)
    nyaSrc = PImage.open('Assets/wish.png').convert('RGBA')
    layer2 = PImage.new('RGBA', nyaSrc.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(layer2)
    
    text = attrs[0]
    beginPixel = (640-len(text)*50,600)
    if len(attrs)>1:
        r = int(attrs[1][:2],16)
        g = int(attrs[1][2:4],16)
        b = int(attrs[1][4:],16)
        draw.text(beginPixel,text,fill=(r,g,b,255),font=font)
    else:
        draw.text(beginPixel,text,fill=(255,255,255,255),font=font)
    p = generateTmpFileName('Wish2')

    PImage.alpha_composite(nyaSrc,layer2).save(p)
    asyncio.ensure_future(rmTmpFile(p),loop=None)
    return [generateImageFromFile(p)]

async def 希望工程(*attrs, kwargs={}):
    font = ImageFont.truetype('Assets/sarasa-gothic-ttf-0.12.5/sarasa-ui-tc-bold.ttf',100)
    nyaSrc = PImage.open('Assets/wish.jpg').convert('RGBA')
    layer2 = PImage.new('RGBA', nyaSrc.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(layer2)
    
    text = attrs[0]
    beginPixel = (540-len(text)*50,900)
    if len(attrs)>1:
        r = int(attrs[1][:2],16)
        g = int(attrs[1][2:4],16)
        b = int(attrs[1][4:],16)
        draw.text(beginPixel,text,fill=(r,g,b,255),font=font)
    else:
        draw.text(beginPixel,text,fill=(0,0,0,255),font=font)
    p = generateTmpFileName('Wish')

    PImage.alpha_composite(nyaSrc,layer2).save(p)
    asyncio.ensure_future(rmTmpFile(p),loop=None)
    return [generateImageFromFile(p)]

async def 打拳姬(*attrs, kwargs={}): return [Plain(f'''看到这句话我气得浑身发抖，大热天的全身冷汗手脚冰凉，这个社会还能不能好了，{attrs[0]}你们才满意，眼泪不争气的流了下来，这个国到处充斥着对{attrs[1]}的压迫，{attrs[1]}何时才能真正的站起来。''')]

async def 懂的都懂(*attrs, kwargs={}): return [Plain('这种事情见得多了，我只想说懂的都懂，不懂的我也不多解释，毕竟自己知道就好，细细品吧。你们也别来问我怎么了，利益牵扯太大，说了对你我都没好处，当不知道就行了，其余的我只能说这里面水很深，牵扯到很多东西。详细情况你们自己是很难找的，网上大部分已经删除干净了，所以我只能说懂的都懂。懂的人已经基本都获利上岸了，不懂的人永远不懂，关键懂的人都是自己悟的，你也不知道谁是懂的人也没法请教，大家都藏着掖着生怕别人知道自己懂的事，所以不懂的你甚至都不知道自己不懂。在有些时候，某些人对某些事情不懂装懂，还以为别人不懂。其实自己才是不懂的，别人懂的够多了，不仅懂，还懂的超越了这个范围，但是某些不懂的人让懂的人完全教不懂，所以不懂的人永远不懂，只能不懂装懂，别人说懂的都懂，只要点点头就行了。其实你我都懂，不懂没必要装懂，毕竟里面牵扯到很多懂不了的事，懂的人觉得没必要说出来，不懂的人看见又来问七问八，最后跟他说了他也不一定能懂，就算懂了以后也对他不好，毕竟懂的太多了不是好。懂了吗？')]

async def 舔狗生成器(*attrs, kwargs={}):
    pat = ['太太','画','手','图']
    for i in range(min(len(attrs),len(pat))):
        pat[i] = attrs[i]
    construct = [
        {"msg":f"您太会{pat[1]}了我跪下来给您用免洗洗{pat[2]}液洗{pat[2]}"},
        {"msg":f"太会{pat[1]}了"},
        {"msg":f"什么{pat[2]}，怎么长的"},
        {"msg":f"太神了"},
        {"msg":f"塞纳河畔的水我的泪"},
        {"msg":f"我嚎到邻居跟我一起嚎kamisama"},
        {"msg":f"整个小区声控灯被我嚎碎"},
        {"msg":f"{pat[0]}您太会{pat[1]}了"},
        {"msg":f"太会了"},
        {"msg":f"神仙下凡普渡众生"},
        {"msg":f"中西结合融会贯通的大善心"},
        {"msg":f"您太会了"},
        {"msg":f"绝了"},
        {"msg":f"绝炸了"},
        {"msg":f"我首当其冲放烟花"},
        {"msg":f"您太会了"},
        {"msg":f"我晚上看到{pat[3]}从床上蹦起落下三百六十度头骨错位大喊"},
        {"msg":f"您太会了！！！！！！！！！"},
        {"msg":f"我拿起手机一看，头骨瞬间回位"},
        {"msg":f"您简直神了"},
        {"msg":f"这是什么神仙连{pat[1]}都能包治百病"},
        {"msg":f"{pat[1]}医双修神仙"},
        {"msg":f"绝了"},
        {"msg":f"您这种神仙活该位列仙班"},
        {"msg":f"仙班的甲子班"},
        {"msg":f"您不是kami就没有神仙了"},
        {"msg":f"简直绝了"},
        {"msg":f"神仙的菜想必也是极好吃的"},
        {"msg":f"不仅物理炒菜"},
        {"msg":f"精神上还喂饱了好多人"},
        {"msg":f"简直活佛济世"},
        {"msg":f"不行我要再去看看"},
        {"msg":f"太神了"},
        {"msg":f"神迹"},
        {"msg":f"未来滚滚历史长河中名{pat[1]}必有您一份"},
        {"msg":f"难道你就觉得它只是{pat[1]}"},
        {"msg":f"难道你又不更远一点想到，那神仙下凡拯救众生的善心"},
        # 这里有几句话太难通用：
        # > 那个炸毛毛毛
        # > 绝了
        # > 灵活的姿态，准确的用色，美丽的线条
        # > 绝了
        {"msg":f"我透过手机屏幕感受到了直击心灵的震撼"},
        {"msg":f"我每个细胞带着我全身尖叫活性爆发整个人获得了超凡的能量就因为您的{pat[1]}"},
        {"msg":f"我激情落泪"},
        {"msg":f"我把我自己耳朵都嚎聋了"},
        {"msg":f"恨不得摆上一车喇叭歌颂您的光辉事迹"}
    ]
    asyncio.ensure_future(msgSerializer(construct,**kwargs))
    return [Plain(f"!{pat[0]}!!!!!!")]

async def 川普生成器(*attrs, kwargs={}):
    s = ' '.join(attrs) if attrs else '中国'
    pat = f"{chr(128588)}没有人\n{chr(128080)}比我\n{chr(128076)}更懂\n{chr(9757)}{s}"
    return [Plain(pat)]

async def 骰子(*attrs, kwargs={}):
    if(len(attrs)>=2):
        x,y=(int(i) for i in attrs[:2])
        return [Plain(f"{random.randint(min(x,y),max(x,y))}")]
    else:
        return [Plain("我要怎么给你Roll哦")]

async def 军舰(*attrs, kwargs={}):
    try:
        return [Plain(random.choice(["那么小声还想开军舰？","听不见！"]))]
    except Exception as e:
        return [Plain(str(e))]

async def 今日人品(*attrs,kwargs={}):
    player_id=kwargs['mem'].id
    if player_id not in GLOBAL.JRRP_map: #已经存在信息直接读取，否则生成新数字
        temp_rpval=random.randint(0,100)
        GLOBAL.JRRP_map[player_id]=[temp_rpval]
        #随机抽取字典值
        b=list(GLOBAL.JRRP_words)
        random.shuffle(b)
        if temp_rpval==100:
            GLOBAL.JRRP_map[player_id].extend([['诸事皆宜'],['-']])
        elif 80<=temp_rpval<=99:
            GLOBAL.JRRP_map[player_id].extend([b[0:5],b[5:6]])
        elif 60<=temp_rpval:
            GLOBAL.JRRP_map[player_id].extend([b[0:4],b[4:6]])
        elif 40<=temp_rpval:
            GLOBAL.JRRP_map[player_id].extend([b[0:3],b[3:6]])
        elif 20<=temp_rpval:
            GLOBAL.JRRP_map[player_id].extend([b[0:2],b[2:6]])
        elif 1<=temp_rpval:
            GLOBAL.JRRP_map[player_id].extend([b[0:1],b[1:6]])
        elif temp_rpval==0:
            GLOBAL.JRRP_map[player_id].extend([['-'],['诸事不宜']])

    rp_val=GLOBAL.JRRP_map[player_id][0]
    print(rp_val)
    print(GLOBAL.JRRP_map[player_id])
    ans='你今天的人品为：'+str(rp_val)+'\n'
    ans+='宜：'+','.join(GLOBAL.JRRP_map[player_id][1])+'\n'
    ans+='忌：'+','.join(GLOBAL.JRRP_map[player_id][2])+'\n'

    return [Plain(ans)]
    #rp_val=GLOBAL.JRRP_map[player_id]
    #ans='你今天的人品为：'+str(rp_val)+'\n评价：'
    #if rp_val==100:
    #    ans+='心想事成'
    #elif 80<=rp_val<=99:
    #    ans+='万事如意'
    #elif 60<=rp_val<=79:
    #    ans+='修短随化'
    #elif 40<=rp_val<=59:
    #    ans+='因祸得福'
    #elif 20<=rp_val<=39:
    #    ans+='落魄不偶'
    #elif 1<=rp_val<=19:
    #    ans+='有命无运'
    #elif rp_val==0:
    #    ans+='危！'
    #return [Plain(ans)]

functionMap = {
    '#论证':这么臭的函数有必要定义吗,
    '#营销':营销生成器,
    '#舔':舔狗生成器,
    '#解答':优质解答生成器,
    '#希望':希望没事生成器,
    '#希望工程':希望工程,
    '#同学':同学你好生成器,
    '#不会吧':不会吧,
    '#拳':打拳姬,
    '#nya':猫图生成器,
    '#Trump':川普生成器,
    '#口罩':IPlay生成器,
    "#Roll":骰子,
    "#军舰":军舰,
    "#今日人品":今日人品,
    '#懂':懂的都懂,
    '#百度':自己不會百度嗎
}

shortMap = {
    '#pr':'#舔',
    '#trump':'#Trump',
    '#jj': "#军舰",
    "#jrrp": "#今日人品",
    '#baidu':'#百度'
}

functionDescript = {
    '#论证':'这么臭的功能有必要解释吗',
    '#百度':'自己不會百度嗎?那我來幫你百度一下',
    '#懂':'懂的都懂,不懂的我也不多解释',
    '#nya':'生成猫表情，目前大概最多放4个中文字，例:#nya 要命',
    '#解答':'生成优质解答图片,例:#解答 自分で百度しろ',
    '#希望':'希望人没事生成器（莲华）,例:#希望 人别死我家门口',
    '#希望工程':'希望人没事生成器（一般）,例:#希望 人别死我家门口',
    '#营销':'营销号生成器，格式：#营销 <主题> <事件> <另一种说法>',
    '#同学':'同学你好生成器，格式：#同学 <群名> <这个群教什么东西>',
    '#不会吧':'不会吧生成器，例：#不会吧 把浴霸关上',
    '#口罩':'自己试试效果吧，例:#口罩 I play BanG Dream!',
    '#Roll':'44的骰娘，返回指定区间的一个整数。用法:#Roll <左区间(包含)> <右区间(不包含)>',
    '#军舰':'重来！这么小声还想问"#军舰"怎么开?',
    "#今日人品":'取得你今天的人品值（0~100）',
    '#Trump':'No one knows Trump Generator better than me!',
    '#拳':
"""
轮到我出拳了！（
格式:
    #拳 <事件> <主体>
例:
    #拳 我们女孩子到底要怎么活着 女性
""",
    '#舔':
"""
稍微有点难用的舔狗生成器
用法:
    #舔 [人名] [动词,表示待舔人的技能] [待舔人用于施展技能的身体部位] [待舔人的技能产物]
没填的部分会用默认值填满。
默认值:
    #舔 太太 画 手 图
"""
}
