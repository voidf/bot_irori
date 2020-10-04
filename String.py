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

def BVCoder(*attrs,**kwargs):
    def dec(x):
        r=0
        for i in range(6):
            r+=tr[x[s[i]]]*58**i
        return (r-add)^xor

    def enc(x):
        x=(x^xor)+add
        r=list('BV1  4 1 7  ')
        for i in range(6):
            r[s[i]]=table[x//58**i%58]
        return ''.join(r)
    table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr={}
    for i in range(58):
        tr[table[i]]=i
    s=[11,10,3,8,4,6]
    xor=177451812
    add=8728348608
    try:
        try:
            ostr = [Plain(text=enc(int(i))+'\n') for i in attrs]
        except:
            ostr = [Plain(text='av'+str(dec(i))+'\n') for i in attrs]
    except Exception as e:
        ostr = [Plain(text=str(e))]
    return ostr
        
def 编码base64(*attrs,**kwargs):
    try:
        return [Plain(text=str(base64.b64encode(bytes(i,'utf-8')))+'\n') for i in attrs]
    except Exception as e:
        return [Plain(text=str(e))]

def 解码base64(*attrs,**kwargs):
    try:
        return [Plain(text=str(base64.b64decode(i))+'\n') for i in attrs]
    except Exception as e:
        return [Plain(text=str(e))]

def rot_13(*attrs,**kwargs):
    upperdict = {'A': 'N', 'B': 'O', 'C': 'P', 'D': 'Q', 'E': 'R', 'F': 'S', 'G': 'T', 'H': 'U', 'I': 'V', 'J': 'W', 'K': 'X', 'L': 'Y',
			 'M': 'Z', 'N': 'A', 'O': 'B', 'P': 'C', 'Q': 'D', 'R': 'E', 'S': 'F', 'T': 'G', 'U': 'H', 'V': 'I', 'W': 'J', 'X': 'K', 'Y': 'L', 'Z': 'M'}

    lowerdict = {'a': 'n', 'b': 'o', 'c': 'p', 'd': 'q', 'e': 'r', 'f': 's', 'g': 't', 'h': 'u', 'i': 'v', 'j': 'w', 'k': 'x', 'l': 'y',
                'm': 'z', 'n': 'a', 'o': 'b', 'p': 'c', 'q': 'd', 'r': 'e', 's': 'f', 't': 'g', 'u': 'h', 'v': 'i', 'w': 'j', 'x': 'k', 'y': 'l', 'z': 'm'}
    ostr = []
    for j in attrs:
        dst=[]
        for i in j:
            if i in upperdict:
                dst.append(upperdict[i])
            elif i in lowerdict:
                dst.append(lowerdict[i])
            else:
                dst.append(i)
        ostr.append(Plain(text=''.join(dst)+'\n'))
    return ostr

def 字符串反转(*attrs,**kwargs):return [Plain(' '.join(attrs)[::-1])]

def 二维码生成器(*attrs,**kwargs):
    s = ' '.join(attrs)
    q = qrcode.make(s)
    fn = randstr(GLOBAL.randomStrLength)+'tmpqrcode'+str(kwargs['mem'].id)
    q.save(fn)
    #threading.Thread(target=rmTmpFile).start()
    asyncio.ensure_future(rmTmpFile(fn),loop=None)
    return [generateImageFromFile(fn)]

def 字符串签名(*attrs,**kwargs):
    if 'pic' in kwargs and kwargs['pic']:
        src = requests.get(kwargs['pic'].url).content
    elif attrs:
        src = bytes(' '.join(attrs),'utf-8')
    else:
        return [Plain('没法处理空串哦！')]
    return [
        Plain(f"MD5:{hashlib.md5(src).hexdigest()}\n"),
        Plain(f"SHA1:{hashlib.sha1(src).hexdigest()}\n"),
        Plain(f"SHA256:{hashlib.sha256(src).hexdigest()}\n"),
        Plain(f"CRC32:{hex(zlib.crc32(src))}\n")
        ]
    
with open('Assets/zh2morse.json','r') as f:
    z2m = json.load(f)

with open('Assets/morse2zh.json','r') as f:
    m2z = json.load(f)

k1 = """ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.:,;?='/!-_"()$&@"""
k2 = """.- -... -.-. -..
. ..-. --. ....
.. .--- -.- .-..
-- -. --- .--.
--.- .-. ... -
..- ...- .-- -..-
-.-- --..
----- .---- ..--- ...--
....- ..... -.... --...
---.. ----.
.-.-.- ---... --..-- -.-.-.
..--.. -...- .----. -..-.
-.-.-- -....- ..--.- .-..-.
-.--. -.--.-
...-..- .-... .--.-."""

a2m = dict(zip(k1,k2.split()))
m2a = dict(zip(k2.split(),k1))

def 转电码(*attrs,**kwargs):
    global z2m,a2m
    msg = ' '.join(attrs).upper()

    conf = re.findall('''SPLIT=(.*?) ''',msg)
    split_symbol = '/'
    print(conf)
    if not conf:
        conf = re.findall('''SPLIT=(.*?)$''',msg)
        print(conf)
        if conf:
            split_symbol = conf[0]
            for i in conf:
                msg = msg.replace(f'''SPLIT={i}''','')
    else:
        split_symbol = conf[0]
        for i in conf:
            msg = msg.replace(f'''SPLIT={i}''','')

    msg = msg.replace(' ','_')
    ans = []
    cmsg = msg
    for i in msg:
        if i in z2m:
            cmsg = cmsg.replace(i,'_'+z2m[i]+'_')
        elif i not in z2m and i not in a2m:
            return [Plain(f'不合法的字符：{i}')]
    # while '  ' in cmsg:
    #     cmsg = cmsg.replace('  ',' ')

    for i in cmsg:
        ans.append(a2m[i])
    
    return [Plain(split_symbol.join(ans))]

def 译电码(*attrs,**kwargs):
    global m2a
    msg = ' '.join(attrs).upper()

    conf = re.findall('''SPLIT=(.*?) ''',msg)
    split_symbol = '/'
    print(conf)
    if not conf:
        conf = re.findall('''SPLIT=(.*?)$''',msg)
        print(conf)
        if conf:
            split_symbol = conf[0]
            for i in conf:
                msg = msg.replace(f'''SPLIT={i}''','')
    else:
        split_symbol = conf[0]
        for i in conf:
            msg = msg.replace(f'''SPLIT={i}''','')
    
    msg = msg.replace(' ','')
    ans = []
    for i in msg.split(split_symbol):
        if i not in m2a:
            return [Plain(f'不合法的电码：{i}')]
        ans.append(m2a[i])
    return [Plain(''.join(ans))]

def 译中文电码(*attrs,**kwargs):
    global m2z
    msg = ' '.join(attrs).upper()

    conf = re.findall('''SPLIT=(.*?) ''',msg)
    split_symbol = '_'
    print(conf)
    if not conf:
        conf = re.findall('''SPLIT=(.*?)$''',msg)
        print(conf)
        if conf:
            split_symbol = conf[0]
            for i in conf:
                msg = msg.replace(f'''SPLIT={i}''','')
    else:
        split_symbol = conf[0]
        for i in conf:
            msg = msg.replace(f'''SPLIT={i}''','')
    
    msg = msg.replace(' ','')
    ans = []
    for i in msg.split(split_symbol):
        if i:
            if i not in m2z:
                ans.append(i)
            else:
                ans.append(m2z[i])
    return [Plain(''.join(ans))]


book_of_answers = [
    '鬼知道','我不知道','希腊奶','?你再问一遍我没听清楚','百度啊','咕狗啊','bing啊',

    '优质解答：我不知道',

    '你可长点心吧',

    '问问爷爷','问问公公','问问44','问问ss','问问fufu',

    '不要这样，妈妈怕',

    '冲，冲tmd',

    '下次一定','别吧','又不是不能用','人不能，至少不应该',

    '進み続け',

    '这合理吗？','哈哈哈，就这？','不会吧不会吧','听不见！这么小声还想问答案？',

    '我谔谔','爬','屁咧',

    '消除恐惧的最好办法就是面对恐惧!',

    '坚持,就是胜利!加油!奥利给!',

    '？你以为我会说是吗？',

    "需要一个相当大的努力",
    "从现在开始 一年也没有关系",
    "绝对不是",
    "接受改变你的日常行为",
    "似乎已经是真实的了",
    "采用一个冒险的态度",
    "允许你选择先休息一下",
    "小心谨慎的靠近",
    "你还是问问爸爸吧",
    "你还是问问妈妈吧",
    "援助会让你成功进步",
    "避免第一个解决方案",
    "被人肯定",
    "更慷慨",
    "耐心点",
    "实际一点吧",
    "打赌",
    "耐心的等待",
    "合作将会是关键",
    "考虑一下这个机会",
    "数到10；再问",
    "以后处理",
    "当然",
    "早点做到这一点",
    "在这个时候不要问太多了",
    "不要担心",
    "不要迫于压力太快",
    "别傻了",
    "不要赌",
    "不用怀疑了",
    "不要忘记有乐趣",
    "不要陷入你的感情",
    "不要犹豫",
    "不要忽视显而易见的",
    "不要过分",
    "不要等待",
    "别浪费时间了",
    "怀疑",
    "尽情体验",
    "要解决",
    "探讨其俏皮的好奇心",
    "完成其他事情的第一",
    "专注你的家庭生活",
    "遵循别人的引导",
    "遵循专家的建议",
    "履行你自己的义务",
    "按照你的意愿",
    "温柔的坚持就是胜利",
    "获得更清晰的视野",
    "把它写下来",
    "给它你的一切",
    "如果是，做的很好；如果不是，就不要这么做；",
    "如果你按我说的做",
    "如果你不反抗",
    "调查研究，然后享受它！",
    "这不可能失败",
    "这可能是特别的",
    "这是肯定的",
    "这不是重要的",
    "这是非常重要",
    "这是你不会忘记的",
    "这肯定会让事情变得有趣",
    "这是不确定的",
    "是值得的麻烦",
    "这可能已经是木已成舟",
    "这可能很难，但你会发现它的价值",
    "这个似乎放心",
    "这将影响别人看你",
    "这将是一种享受",
    "这会带来好运",
    "这将会创造一个扰乱",
    "这仍然是不可预测的",
    "它会支持你的",
    "这将更好地专注于自己的工作",
    "这是不明智的",
    "它会让你付出代价",
    "这是一个不错的时间安排",
    "会很棒的",
    "这是不值得的斗争",
    "是你走的时候",
    "保持开放的心态",
    "不要让别人知道",
    "笑一下",
    "离开旧的解决方案",
    "过去的事就让它过去吧",
    "仔细聆听；那么你就会知道",
    "为什么不列出原因",
    "也许",
    "不幸的是极有可能的",
    "继续前行",
    "从来没有",
    "没有",
    "不管是什么",
    "如果你不孤单",
    "现在你可以",
    "只做一次",
    "其他人将取决于你的选择",
    "注重细节",
    "也许，当你老了",
    "为突发事件做好准备",
    "按下关闭",
    "须以较宽松的步伐",
    "有时候选择太多，就代表着无从选择！",
    "重新考虑你的方法",
    "相关的问题可能的浮出水面",
    "保持灵活",
    "删除你自己的障碍物",
    "重新确定优先次序什么是重要的",
    "尊重规则",
    "保存你的精力",
    "寻找更多的选择",
    "设定优先等级是一个必要的过程！",
    "很快就会解决它",
    "转移你的焦点",
    "说出来吧",
    "令人震惊的事件可能发生的",
    "冒险一试",
    "负责",
    "花更多的时间来决定",
    "告诉别人它对你意味着什么",
    "那将是浪费钱",
    "那是脱离你的控制",
    "答案就在你的后院",
    "答案可能会在另一种语言",
    "最好的解决办法可能不是明显的",
    "机会不会很快再来",
    "情况将很快发生改变",
    "结果会是好的",
    "情况不明",
    "与另一种情况有潜在的联系",
    "有充分的理由保持乐观",
    "没有保证",
    "会有障碍要克服",
    "这是一个很好的时机，来制定新计划",
    "为了确保能作出最佳决策，需要保持冷静",
    "相信自己的直觉",
    "相信你的原始思想",
    "尝试一种更不太可能的解决方案",
    "不宜在这个时候",
    "毫无疑问",
    "无论如何你可以提升",
    "运用你的想象力",
    "等一等",
    "等待一个更好的机会",
    "看看会发生什么",
    "注意你的节奏",
    "不管你做什么，结果将持久",
    "可以",
    "是的，但不要强迫",
    "你一定有支持",
    "你太近的看了",
    "你可能觉得自己无法妥协",
    "你真的不在乎",
    "你知道现在比以前更好",
    "你可能会反对",
    "你可能会放弃其他的东西",
    "你必须",
    "你现在必须行动",
    "你会发现一切你需要知道的",
    "你将需要适应",
    "你不会失望的",
    "你会很高兴你做了",
    "你会得到最后的决定",
    "你将不得不妥协",
    "你将不得不补回来",
    "您需要了解更多信息",
    "你需要考虑其他办法",
    "你需要主动出击",
    "你会后悔的",
    "你的行动将会改善",


    "找个人给你意见",
    "算了吧",
    "请教你的妈妈",
    "当然咯",

    "谁说得准呢，先观望着",
    "千万别傻",
    "保持你的好奇心，去挖掘真相",
    "把心揣怀里",
    "答案在镜子里",
    "不",
    "这事儿不靠谱",
    "天上要掉馅饼了",
    "有好运",
    "要有耐心",
    "你需要知道真相",
    "还有另一种情况",
    "观望",
    "别让它影响到你",
    "是",
    "信任",
    "列个清单",
    "时机不对",
    "照你想的那样去做",
    "量力而行",
    "但行好事，莫问前程",
    "抛弃首选方案",
    "走容易走的路",
    "最佳方案不一定可行",
    "不会作就不会死",
    "试试卖萌",
    "借助他人的经验",
    "再多考虑",
    "注意细节",
    "说出来吧",
    "机会稍纵即逝",
    "制订了一个新计划",
    "GO",
    "谁都不能保证",
    "情况很快就会发生变化",
    "不要陷得太深",
    "转移你的注意力",
    "转移你的焦点",
    "至关重要",
    "告诉自己什么是最重要的",
    "为什么不",
    "别傻等了",
    "不要忘记",
    "为什么不呢",
    "只做一次",
    "去解决",
    "寻找更多的选择",
    "上帝为你关一扇门，必定会为你打开一扇窗",
    "随波逐流未必是好事",
    "问天问大地，不如问自己",
    "你就是答案",
    "你可能会反对",
    "去争取机会",
    "改变不了世界，改变自己",
    "主动一点，人生会大不相同",
    "学会妥协",
    "掌握更多信息",
    "相信你最初的想法",
    "勿忘初心，放得始终",
    "扫除障碍",
    "把重心放在工作上",
    "把重心放在学习上",
    "培养一项新的爱好",
    "对他人慷慨",
    "不放赌一把",
    "去做其他的事情",
    "观察形势",
    "休息，休息一会",
    "这是你最后的机会",
    "再考虑一下",
    "并不明智",
    "等待更好的",
    "很快就能解决",
    "重要",
    "是的",
    "采取行动",
    "去做",
    "不要过火",
    "事情开始变得有趣了",
    "保存你的实力",
    "这是一定的",
    "不确定的因素有点多",
    "结果不错",
    "你可能不得不放弃其他东西",
    "不需要",
    "去倾诉",
    "告诉别人这对你意味着什么",
    "无论你做何种选择，结果都是对的",
    "保持头脑清醒",
    "制定计划",
    "很麻烦",
    "克服困难",
    "实际一点",
    "你需要一点帮助",
    "协作",
    "需找更多的选择",
    "负责",
    "阻止",
    "你必须现在就行动",
    "遵守规则",
    "坚持",
    "需要花费点时间",
    "不要迫于压力而改变初衷",
    "显而易见",
    "不雅忽略身边的人",
    "抗拒",
    "不值得斗争",
    "玩得开心就好",
    "毋庸置疑",
    "你也许会失望",
    "去改变",
    "一个强有力的承诺会换回更好的结果",
    "也许有更好的解决方案",
    "不要害怕",
    "想法太多，选择太少",
    "是的",
    "一笑而过",
    "取决于你的选择",
    "随TA去",
    "一年后就不那么重要了",
    "醒醒吧，别做梦了",
    "意义非凡",
    "默数十秒再问我",
    "去行动",
    "发挥你的想象力",
    "对的",
    "为了确保最好的结果，保持冷静",
    "等待",
    "你必须弥补这个缺点",
    "现在比以往任何时候的情况都要好",
    "相信你的直觉",
    "这是一个机会",
    "去问你爸爸",
    "从来没有",
    "寻找一个指路人",
    "去尝试",
    "没有",
    "错的",
    "别不自量力",
    "荒谬",
    "不赌",
    "不值得冒险",
    "不妥协",
    "关注你的家庭生活",
    "肯定",
    "不可预测",
    "绝对不",
    "我确定",
    "尽早完成",
    "令人期待的事情马上要发生",
    "你需要适应",
    "表示怀疑",
    "它会带来好运",
    "要有耐心",
    "记录下来",
    "不宜在这个时候",
    "决定了就去做",
    "别要求太多",
    "放弃第一个方案",
    "HOLD不住",
    "谨慎小心",
    "注意细节",
    "注意身后",
    "继续前进",
    "情况很快就会发生改变",
    "不要被情绪左右",
    "转移注意力",
    "着眼未来",
    "问自己什么是最重要的",
    "不要等了",
    "保持乐观",
    "没有更好的选择",
    "列出原因",
    "改变自己",
    "你需要主动",
    "妥协",
    "有比这更重要的东西",
    "你需要掌握更多的信息",
    "删除记忆",
    "能让你快乐的那个决定",
    "你需要考虑其他方面",
    "相信自己的直觉",
    "这是一个机会",
    "形势不明",
    "先让自己休息",
    "重新考虑",
    "不明智",
    "抓住机会",
    "等待机会",
    "不要做得太过分",
    "保持现状",
    "不要忧虑",
    "有意料之外的事会发生，不妨等待",
    "你会失望的",
    "花更多的时间来决定",
    "你开心就好"
]

book_of_answers = list(set(book_of_answers))

book_of_answers_en = [
    "A Substantial Effort Will Be Required",
    "A Year From Now It Won't Matter",
    "Absolutely Not",
    "Accept A Change To Your Routine",
    "Act As Though It Is Already Real",
    "Adopt An Adventurous Attitude",
    "Allow Yoursele To Rest First",
    "Approach Cautiously",
    "Ask Your Father",
    "Ask Your Mother",
    "Assistance Would Make Your Progress A Success",
    "Avoid The First Solution",
    "Be Delightfully Sure Of It",
    "Be More Generous",
    "Be Patient",
    "Be Practical",
    "Bet On It",
    "Better To Wait",
    "Collaboration Will Be The Key",
    "Consider It An Opportunity",
    "Count To 10; Ask Again",
    "Deal With It Later",
    "Definitely",
    "Do It Early",
    "Don't Ask For Any More At This Time",
    "Don't Be Concerned",
    "Don't Be Pressured Into Acting Too Quickly",
    "Don't Be Ridiculous",
    "Don't Bet On It",
    "Don't Doubt It",
    "Don't Forget To Have Fun",
    "Don't Get Caught Up In Your Emotions",
    "Don't Hesitate",
    "Don't Ignore The Obvious",
    "Don't Overdo It",
    "Don't Wait",
    "Don't Waste Your Time",
    "Doubt It",
    "Enjoy The Experience",
    "Expect To Settle",
    "Explore It With Playful Curiosity",
    "Finish Something Else First",
    "Focus On Your Home Life",
    "Follow Someone Else's Lead",
    "Follow The Advice Of Experts",
    "Follow Through On Your Obligations",
    "Follow Through With Your Good Intentions",
    "Gentle Persistence Will Pay Off",
    "Get A Clearer View",
    "Get It In Writing",
    "Give It All You've Got",
    "If It's Done Well; If Not, Don't Do It At All",
    "If You Do As You're Told",
    "If You Don't Resist",
    "Investigate And Then Enjoy It",
    "It Cannot Fail",
    "It Could Be Extraordinary",
    "It Is Certain",
    "It Is Not Significant",
    "It Is Significant",
    "It Is Something You Won't Forget",
    "It Is Sure To Make Things Interesting",
    "It Is Uncertain",
    "It Is Worth The Trouble",
    "It May Already Be A Done Deal",
    "It May Be Difficult But You Will Find Value In It",
    "It Seems Assured",
    "It Will Affect How Others See You",
    "It Will Be A Pleasure",
    "It Will Bring Good Luck",
    "It Will Create A Stir",
    "It Will Remain Unpredictable",
    "It Will Sustain You",
    "It Would Be Better To Focus On Your Work",
    "It Would Be Inadvisable",
    "It'll Cost You",
    "It's A Good Time To Make Plans",
    "It's Gonna Be Great",
    "It's Not Worth A Struggle",
    "It's Time For You To Go",
    "Keep An Open Mind",
    "Keep It To Yourself",
    "Laugh About It",
    "Leave Behind Old Solutions",
    "Let It Go",
    "Listen More Carefully; Then You Will Know",
    "Make A List Of Why",
    "Make A List Of Why Not",
    "Maybe",
    "Mishaps Are Highly Probable",
    "Move On",
    "Never",
    "No",
    "No Matter What",
    "Not If You're Alone",
    "Now You Can",
    "Only Do It Once",
    "Others Will Depend On Your Choices",
    "Pay Attention To The Details",
    "Perhaps, When You're Older",
    "Prepare For The Unexpected",
    "Press For Closure",
    "Proceed At A More Relaxed Pace",
    "Realize That Too Many Choices Is As Difficult As Too Few",
    "Reconsider Your Approach",
    "Related Issues May Surface",
    "Remain Flexible",
    "Remove Your Own Obstacles",
    "Reprioritize What Is Important",
    "Respect The Rules",
    "Save Your Energy",
    "Seek Out More Options",
    "Setting Priorities Will Be A Necessary Part Of The Process",
    "Settle It Soon",
    "Shift Your Focus",
    "Speak Up About It",
    "Startling Events May Occur As A Result",
    "Take A Chance",
    "Take Charge",
    "Take More Time To Decide",
    "Tell Someone What It Means To You",
    "That Would Be A Waste Of Money",
    "That's Out Of Your Control",
    "The Answer Is In Your Backyard",
    "The Answer May Come To You In Another Language",
    "The Best Solution May Not Be The Obvious One",
    "The Chance Will Not Come Again Soon",
    "The Circumstances Will Change Very Quickly",
    "The Outcome Will Be Positive",
    "The Situation Is Unclear",
    "There Is A Substantial Link To Another Situation",
    "There Is Good Reason To Be Optimistic",
    "There Is No Guarantee",
    "There Will Be Obstacles To Overcome",
    "This Is A Good Time To Make A New Plan",
    "To Ensure The Best Decision, Be Calm",
    "Trust Your Intuition",
    "Trust Your Original Thought",
    "Try A More Unlikely Solution",
    "Unfavorable At This Time",
    "Unquestionably",
    "Upgrade Any Way You Can",
    "Use Your Imagination",
    "Wait",
    "Wait For A Better Offer",
    "Watch And See What Happens",
    "Watch Your Step As You Go",
    "Whatever You Do The Results Will Be Lasting",
    "Yes",
    "Yes,But Don't Force It",
    "You Are Sure To Have Support",
    "You Are Too Close To See",
    "You Could Find Yourself Unable To Compromise",
    "You Don't Really Care",
    "You Know Better Now Than Ever Before",
    "You May Have Opposition",
    "You May Have To Drop Other Things",
    "You Must",
    "You Must Act Now",
    "You Will Find Out Everything You'll Need To Know",
    "You Will Need To Accommodate",
    "You Will Not Be Disappointed",
    "You'll Be Happy You Did",
    "You'll Get The Final Word",
    "You'll Have To Compromise",
    "You'll Have To Make It Up As You Go",
    "You'll Need More Information",
    "You'll Need To Consider Other Ways",
    "You'll Need To Take The Initiative",
    "You'll Regret It",
    "Your Actions Will Improve Thin"
]

book_of_answers_en = list(set(book_of_answers_en))

def 答案之书(*attrs,**kwargs):
    player = getPlayer(**kwargs)
    if attrs:
        if attrs[-1] in ('sub','sniff'):
            overwriteSniffer(player,'#为什么',r'\?')
            appendSniffer(player,'#为什么',r'\？')
            appendSniffer(player,'#为什么',r'¿')
            appendSniffer(player,'#为什么',r'吗')
            appendSniffer(player,'#为什么',r'怎么')
            appendSniffer(player,'#为什么',r'如何')
            appendSniffer(player,'#为什么',r'为什么')
            return [Plain('【答案之书】sniff模式')]
        elif attrs[-1] in GLOBAL.unsubscribes:
            removeSniffer(player,'#为什么')
            return [Plain('【答案之书】禁用sniffer')]

    ans = random.choice(book_of_answers)
    return [Plain(ans.strip())]

def 答案之书en(*attrs,**kwargs):
    player = getPlayer(**kwargs)
    if attrs:
        if attrs[-1] in ('sub','sniff'):
            overwriteSniffer(player,'#为什么e',r'\?')
            appendSniffer(player,'#为什么e',r'\？')
            appendSniffer(player,'#为什么e',r'¿')
            appendSniffer(player,'#为什么e',r'吗')
            appendSniffer(player,'#为什么e',r'怎么')
            appendSniffer(player,'#为什么e',r'如何')
            appendSniffer(player,'#为什么e',r'为什么')
            return [Plain('【book of answers】sniff mode on')]
        elif attrs[-1] in GLOBAL.unsubscribes:
            removeSniffer(player,'#为什么e')
            return [Plain('【book of answers】sniff mode off')]

    ans = random.choice(book_of_answers_en)
    return [Plain(ans.strip())]

def KMP(*attrs,**kwargs):
    pat,s = ' '.join(attrs).split(',')
    fail = [-1]
    fval = [-1]
    p1 = 0 
    p2 = -1
    while p1<len(pat):
        if p2==-1 or pat[p1] == pat[p2]:
            p1+=1
            p2+=1
            fail.append(p2)
        else:
            p2 = fail[p2]

    for i in range(1,len(pat)):
        if pat[i] == pat[fail[i]]:
            fval.append(fval[fail[i]])
        else:
            fval.append(fail[i])

    EX_next = [len(pat)]
    EX_extent = []

    a = 0
    k = 0

    for i in range(1,len(pat)):
        if i >= k or i + EX_next[i - a] >= k:
            k = max(k,i)
            while k < len(pat) and pat[k] == pat[k - i]:
                k+=1
            EX_next.append(k - i)
            a = i
        else:
            EX_next.append(EX_next[i - a])

    a = 0
    k = 0

    for i in range(len(s)):
        if i >= k or i + EX_next[i-a]>=k:
            k = max(k,i)
            while k < len(s) and k - i < len(pat) and s[k] == pat[k-i]:
                k+=1
            EX_extent.append(k - i)
            a = i
        else:
            EX_extent.append(EX_next[i - a])

    return [Plain(f'KMP-Fail:{fail}\nKMP-Fval:{fval}\nEXKMP-next:{EX_next}\nEXKMP-extent:{EX_extent}')]


StringMap = {
    '#BV':BVCoder,
    '#b64e':编码base64,
    '#b64d':解码base64,
    '#rot13':rot_13,
    '#rev':字符串反转,
    '#qr':二维码生成器,
    '#digest':字符串签名,
    '#a2m':转电码,
    '#m2a':译电码,
    '#m2z':译中文电码,
    '#为什么':答案之书,
    '#为什么e':答案之书en,
    '#KMP':KMP
}

StringShort = {
    '#ans':'#为什么',
    '#why':'#为什么',
    '#wsm':'#为什么',
    '#anse':'#为什么e',
    '#whye':'#为什么e',
    '#wsme':'#为什么e'
}

StringDescript = {
    '#b64e':'base64编码,例：#b64e mirai',
    '#b64d':'base64解码,例：#b64d 114514==',
    '#rot13':'rot_13编码转换（仅大小写ascii字母）',
    '#qr':'将输入字符串专为二维码,例:#qr mirai',
    '#rev':'字符串反转，例:#rev mirai',
    '#digest':'传入字符串则计算字符串的md5，sha1，sha256，crc32，如传入图片则只处理第一张图片，例:#digest 1145141919810',
    '#BV':
'''
格式：
    #BV <BV号，需带BV两个字>
    即返回av号
    #BV <av号,纯数字，不带av两个字>
    即返回BV号
''',
    '#a2m':
'''
将输入字符转为morse电码
如存在中文则依据《标准电码本》转换成四位数字编码
空格会被转换成下划线
可以指定分隔符,用例:
    #a2m 1145141919810 931 split=?
    使用问号作为字符串"1145141919810 931"的morse电码分隔符
''',
    '#m2a':
'''
将输入morse电码转换成明文
可以指定分隔符,用例:
    #m2a -.--/---/..-/-.-/---/.../--- split=/
    使用/作为电码"-.--/---/..-/-.-/---/.../---"的分隔符
''',
    '#m2z':
'''
将输入数字电码转换成中文
可以指定分隔符,用例:
    #m2z _7093__2448__5530__5358_ split=_
    使用_作为电码"_7093__2448__5530__5358_"的分隔符
''',
    '#为什么':'向答案之书提问（答非所问（问就是自己解决（不会真的有人认为答案之书有用吧？不会吧不会吧？',
    '#为什么e':'向答案之书（英文）提问（答非所问（问就是自己解决（不会真的有人认为答案之书有用吧？不会吧不会吧？',
    '#KMP':
'''
生成KMP算法的fail数组和EXKMP的next和extent数组
格式:
    #KMP <模式串>,<原串>
例：
    #KMP iiyo,koiyo
    #KMP ababaab,aabbbabababaabababaabababaababb
'''}
