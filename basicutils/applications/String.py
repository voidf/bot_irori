"""字符串处理类"""
import os
import sys
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

import basicutils.CONST as GLOBAL
# if __name__ == '__main__':
#     os.chdir('..')
import re
import asyncio
import requests
import json
import random
import os
import base64
import qrcode
import hashlib
import zlib
from urllib.parse import quote
from basicutils.database import *
from basicutils.chain import *
from basicutils.network import *
# from Utils import *

async def BVCoder(*attrs,kwargs={}):
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
        
async def 编码base64(*attrs,kwargs={}):
    try:
        return [Plain(text=str(base64.b64encode(bytes(i,'utf-8')))+'\n') for i in attrs]
    except Exception as e:
        return [Plain(text=str(e))]

async def 解码base64(*attrs,kwargs={}):
    try:
        return [Plain(text=str(base64.b64decode(i))+'\n') for i in attrs]
    except Exception as e:
        return [Plain(text=str(e))]

async def rot_13(*attrs,kwargs={}):
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

async def 字符串反转(*attrs,kwargs={}):return [Plain(' '.join(attrs)[::-1])]

async def 二维码生成器(*attrs,kwargs={}):
    s = ' '.join(attrs)
    q = qrcode.make(s)
    fn = 'tmpqrcode'+randstr(GLOBAL.randomStrLength)
    q.save(fn)
    #threading.Thread(target=rmTmpFile).start()
    asyncio.ensure_future(rmTmpFile(fn),loop=None)
    return [generateImageFromFile(fn)]

async def 字符串签名(*attrs,kwargs={}):
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
    
async def 復讀(*attrs,kwargs={}):return [Plain(' '.join(attrs))]

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

async def 转电码(*attrs,kwargs={}):
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

async def 译电码(*attrs,kwargs={}):
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
    
    
    ans = []
    if len(attrs) > 3:
        for i in msg.split():
            if i not in m2a:
                return [Plain(f'不合法的电码：{i}')]
            ans.append(m2a[i])
    else:
        msg = msg.replace(' ','')
        for i in msg.split(split_symbol):
            if i not in m2a:
                return [Plain(f'不合法的电码：{i}')]
            ans.append(m2a[i])
    return [Plain(''.join(ans))]

async def 译中文电码(*attrs,kwargs={}):
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

    '你寄吧谁啊?',

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
    "这不重要",
    "这非常重要",
    "搞清楚主要矛盾和次要矛盾",
    "这肯定会让事情变得有趣",
    "这我不确定",
    "挺麻烦，但可做",
    "木已成舟，你爬吧",
    "难，但是值得搞",
    "放心啦",
    "这将影响别人怎么看你",
    "这是一种享受",
    "这会带来好运",
    "这大概会烦死你",
    "这挺不靠谱的",
    "有人会支持你的",
    "这对你专心干活有帮助",
    "救命啊，你是猪吗？",
    "快跑啊",
    "它会让你付出代价",
    "这是一个不错的安排",
    "会很棒的",
    "这不值得奋斗",
    "这你都不会？",
    "保持开放的心态",
    "不要让别人知道",
    "笑一下",
    "别用旧的方案搞新问题",
    "过去的事就让它过去吧",
    "听听别人怎么整吧",
    "为什么不列出原因",
    "也许",
    "很不幸地告诉宁，这是极有可能的",
    "冲！",
    "从来没有",
    "没有",
    "不管是什么",
    "如果有人跟你一起",
    "现在你做得到",
    "只做一次",
    "其他人将取决于你的选择",
    "注重细节",
    "不要在意那些细节（",
    "可能要等到你老去",
    "为突发事件做好准备",
    "小心猝死",
    "右上角关闭谢谢",
    "须以较宽松的步伐",
    "我觉得你用用random比较好",
    "重新考虑你的方法",
    "相关的问题可能会越来越多",
    "保持灵活",
    "克服你自己的障碍",
    "重新确定什么比较重要",
    "请遵守规则",
    "保存你的精力",
    "你省省吧",
    "寻找更多的选择",
    "这重要吗？",
    "很快就能搞掂",
    "转移你的焦点",
    "讲啊",
    "震惊！",
    "冒险一试",
    "试试就逝世",
    "你得负责",
    "多花点时间想想罢",
    "浪费钱",
    "可能不会像你想的那么顺利",
    "答案就在你的后院",
    "答案就在你的后庭",
    "答案可能不是用中文能描述的",
    "最好的解决办法不大明显",
    "机会不可能再来",
    "情况将很快发生改变",
    "结果会是好的",
    "情况不明",
    "有充分的理由保持乐观",
    "没有保证",
    "会有障碍要克服",
    "考虑用别的方法吧",
    "冷静。",
    "相信自己的直觉",
    "坚持你的初心",
    "尝试一种更离谱的解决方案",
    "离大谱",
    "别在这个时候",
    "毫无疑问",
    "运用你的想象力",
    "等一等",
    "等待一个更好的机会",
    "看看会发生什么",
    "注意你的节奏",
    "不管你做什么结果都一样",
    "可以",
    "是的，但不要死缠烂打",
    "一定有人支持你",
    "你再问就不灵了",
    "你不觉得问我是在浪费时间吗？",
    "反正不管我怎么说你都不在乎",
    "你知道我说啥都不会改变你的情况",
    "你会反对",
    "你可能会得放弃其他的东西",
    "你必须",
    "你现在必须行动",
    "你将需要适应",
    "你不会失望的",
    "之后你会很高兴你做了",
    "你会得到最后的决定",
    "你将不得不妥协",
    "你将不得不补回来",
    "您需要了解更多信息",
    "你需要考虑其他办法",
    "你需要主动出击",
    "你会后悔的",


    "找个人给你意见",
    "算了吧",
    "别了吧",
    "请教你的妈妈",
    "当然咯",

    "谁说得准呢，先观望着",
    "建议你当回等等党",
    "千万别傻",
    "保持你的好奇心，去挖掘真相",
    "先掂量掂量自己几斤几两",
    "答案在镜子里，反正不在我这里",
    "不",
    "这事儿不靠谱",
    "天上要掉馅饼了",
    "有好运",
    "要有耐心",
    "你需要知道真相",
    "分类讨论好吧",
    "观望",
    "别让它影响到你",
    "是",
    "信任",
    "时机不对",
    "照你想的那样去做",
    "量力而行",
    "但行好事，莫问前程",
    "贼你妈离谱儿",
    "走容易走的路",
    "最佳方案不一定可行",
    "不会作就不会死",
    "试试卖萌",
    "喵喵喵？",
    "借助他人的经验",
    "再多考虑",
    "注意细节",
    "机会稍纵即逝",
    "GO",
    "谁都不能保证",
    "情况很快就会发生变化",
    "不要陷得太深",
    "我们换个问题行吗？",
    "我们换个问题不好吗？",
    "至关重要",
    "为什么不",
    "别傻等了",
    "不要忘记",
    "为什么不呢",
    "只做一次",
    "去解决",
    "寻找更多的选择",
    "上帝为你关一扇门，必定会为你打开一扇窗",
    "上帝为你关一扇门，必定会为你再关一扇窗",
    "随波逐流未必是好事",
    "问天问大地，不如问自己",
    "我懂个屁",
    "你懂个屁",
    "你就是答案",
    "你可能会反对",
    "我不想回答",
    "去争取机会",
    "改变不了世界，改变自己",
    "主动一点，人生会大不相同",
    "学会妥协",
    "掌握更多信息",
    "相信你最初的想法",
    "勿忘初心，方得始终",
    "扫除障碍",
    "把重心放在工作上",
    "把重心放在学习上",
    "培养一项新的爱好",
    "对他人慷慨",
    "不妨赌一把",
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
    # 组内语料
    "怎么你群老有人说话一股女厕所味啊",
    "笑死",
    "我真的笑死",
    "他居然还没死",
    "救命",
    "差点死掉就是说",
    "我也想谈恋爱",
    "草",
    "一般",
    "有点爽",
    "你好，有的",
    "没见过欸",
    "破案了",
    "花钱有点多",
    "狗都不干",
    "啥玩意儿",
    "那没事了",
    "好有道理",
    "不错",
    "谁杏玉来",
    "这个真的不行",
    "我真的救大命..",
    "可能不可以",
    "至少我不会",
    "我真的会笑",
    "还不错",
    "我去 牛逼",
    "大无语",
    "终极无语事件",
    "好可怕",
    "快跳车快跳车快跳车",
    "爆笑了",
    "笑得想死",
    "好讨厌",
    "对啊就是说",
    "我该回什么",
    "有没有懂的",
    "同问",
    "？",
    "¿",
    "不愿再笑",
    "芜湖",
    "好惨啊啊啊",
    "啊什么意思",
    "=_=||",
    # 组内语料完
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
    "快停下啊啊啊啊",
    "你必须现在就行动",
    "坚持",
    "需要花费点时间",
    "不要迫于压力而改变初衷",
    "显而易见",
    "别忽略身边的人",
    "抗拒",
    "不值得斗争",
    "玩得开心就好",
    "你开心就好",
    "毋庸置疑",
    "你也许会失望",
    "去改变",
    "也许有更好的解决方案",
    "不要害怕",
    "想法太多，选择太少",
    "一笑而过",
    "取决于你的选择",
    "随TA去",
    "醒醒吧，别做梦了",
    "意义非凡",
    "默数十秒再问我",
    "去行动",
    "发挥你的想象力",
    "对的",
    "为了确保最好的结果，保持冷静",
    "等待",
    "现在比以往任何时候的情况都要好",
    "时代变啦",
    "快醒醒",
    "相信你的直觉",
    "这是一个机会",
    "去问你爸爸",
    "寻找一个指路人",
    "去尝试",
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
    "记录下来",
    "不宜在这个时候",
    "决定了就去做",
    "别要求太多",
    "放弃第一个方案",
    "HOLD不住",
    "谨慎小心",
    "继续前进",
    "你自己的锅你自己修",
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
    "形势不明",
    "先歇会",
    "歇逼吧您",
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

def 答案之书(ent: CoreEntity):
    '''#答案之书 [#why, #wsm, #ans]
    向答案之书提问（答非所问（问就是自己解决（不会真的有人认为答案之书有用吧？不会吧不会吧？
    '''
    player = ent.player
    attrs = ent.chain.tostr().split(' ')
    if attrs:
        if attrs[-1] in ('sub','sniff'):
            Sniffer.overwrite(player,'#答案之书',r'\?')
            Sniffer.append(player,'#答案之书',r'\？')
            Sniffer.append(player,'#答案之书',r'¿')
            Sniffer.append(player,'#答案之书',r'吗')
            Sniffer.append(player,'#答案之书',r'啥')
            Sniffer.append(player,'#答案之书',r'怎么')
            Sniffer.append(player,'#答案之书',r'如何')
            Sniffer.append(player,'#答案之书',r'为什么')
            return [Plain('【答案之书】sniff模式')]
        elif attrs[-1] in GLOBAL.unsubscribes:
            Sniffer.remove(player,'#答案之书')
            return [Plain('【答案之书】禁用sniffer')]
    dynamic_answers = [f"http://iwo.im/?q={quote(' '.join(attrs))}"]
    ans = random.choice(book_of_answers+dynamic_answers)
    return [Plain(ans.strip())]

def 答案之书en(ent: CoreEntity):
    '''#答案之书en [#whye, #wsme, #anse]
    向答案之书(英文)提问（答非所问（问就是自己解决（不会真的有人认为答案之书有用吧？不会吧不会吧？
    '''
    player = ent.player
    attrs = ent.chain.tostr().split(' ')
    if attrs:
        if attrs[-1] in ('sub','sniff'):
            Sniffer.overwrite(player,'#答案之书en',r'\?')
            Sniffer.append(player,'#答案之书en',r'\？')
            Sniffer.append(player,'#答案之书en',r'¿')
            Sniffer.append(player,'#答案之书en',r'吗')
            Sniffer.append(player,'#答案之书en',r'怎么')
            Sniffer.append(player,'#答案之书en',r'如何')
            Sniffer.append(player,'#答案之书en',r'为什么')
            return [Plain('【book of answers】sniff mode on')]
        elif attrs[-1] in GLOBAL.unsubscribes:
            Sniffer.remove(player,'#答案之书en')
            return [Plain('【book of answers】sniff mode off')]
    dynamic_answers = [f"http://iwo.im/?q={quote(' '.join(attrs))}"]
    ans = random.choice(book_of_answers_en+dynamic_answers)
    return [Plain(ans.strip())]

async def KMP(*attrs,kwargs={}):
    pat, s = attrs[0], attrs[1]
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


functionMap = {
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
    '#repeat':復讀,
    '#KMP':KMP
}

shortMap = {
    # '#ans':'#答案之书',
    # '#why':'#答案之书',
    # '#wsm':'#答案之书',
    # '#anse':'#答案之书en',
    # '#whye':'#答案之书en',
    # '#wsme':'#答案之书en'
}

functionDescript = {
    '#repeat':'復讀消息，測試用',
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
    '#KMP':
'''
生成KMP算法的fail数组和EXKMP的next和extent数组
格式:
    #KMP <模式串>,<原串>
例：
    #KMP iiyo,koiyo
    #KMP ababaab,aabbbabababaabababaabababaababb
'''}
