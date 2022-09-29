"""信用点类"""
import math
import os
import sys

from bs4 import BeautifulSoup
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

# if __name__ == '__main__':
    # os.chdir('..')
# print(os.listdir('.'))
# print(__name__)
import basicutils.CONST as C
import random
import copy
import traceback
import datetime
from basicutils.algorithms import *
from basicutils.network import *
from basicutils.database import *
from basicutils.chain import *
from basicutils.task import *
# print(MessageChain)
from loguru import logger
# import sys
# print(sys.path)

# print(sys.path)
# print(os.getcwd())

from fapi.models.Player import *
# sys.path.append(os.getcwd())

宜 = {
    # 洛谷每日求签手动整理
    "出行": "一路顺风",
    "上课": "100%消化",
    "搞基": "友谊地久天长",
    "丧葬": "灵魂得到安息",
    "睡觉": "养足精力，明日再战",
    "考试": "学的全会，蒙的全对",
    "装弱": "被识破",
    "吃饭": "人是铁饭是钢",
    "刷题": "成为虐题狂魔",
    "纳财": "要到好多money",
    "开电脑": "电脑的状态也很好",
    "写作文":  "非常有文采",
    "泡妹子": "说不定可以牵手",
    "参加CSP": "祝你rp++",
    "发朋友圈": "分享是种美德",
    "学习珂学": "珂朵莉太可爱了",
    "背诵课文": "看一遍就背下来了",
    "参加模拟赛": "可以AK虐全场",
    "继续完成WA的题": "下一次就可以AC了",
    "扶老奶奶过马路": "增加RP",
    "打chunithm": "您虹了",
    "打sdvx":"您暴了",
    "打maimai":"机厅没有人 和阴兵爷爷拼机",
    # 日常
    ## 今日人品迁移
    "开车": "逮虾户",
    "看番": "我草这番不看血亏",
    "抽卡": "阳寿加持",
    "摸鱼": "心情UP",
    "吹水": "女人是水做的（？）",
    "打钱": "Shut up and take my money",
    "看书": "这书就不该这个价卖给你",
    "开封菜": "所有属性大幅提升，效果持续1天",
    "金拱门": "快乐！",
    "华莱士": "门店和食物意外的干净",
    "冲": "回来告诉我浓的还是稀的",
    "买嘢": "plus会员-114514，史低，这不冲？",
    "白嫖": "你好我是学生请倒贴200块生活费送我",
    "拼车": "完美避开交警抓带人",
    "表白": "说不定能把人家推倒",
    "沟通": "三句话，让学校白送我1919810软妹币",
    "抓虫": "秋风扫落叶",
    "和irori聊天": "她真的没成精吗？",
    ##
    "起稿": "我觉得这可以搞",
    "对线": "没有人比我更懂***",
    "复习": "把知识刻进DNA里",
    "作曲": "梦中作曲不愧是我",
    "理财": "你不理财，财不理你",
    "水群": "没有人比我更懂龙王",
    "骑自行车": "风驰电掣，从不翻车",
    "飙车": "老车神了",
    "去图书馆": "博览群书，下笔有神",
    "去空教室": "真正的自习室！yyds！",
    "睡个午觉": "HP回满了！",
    "拆快递": "哇！金色传说！",
    "寄快递": "运费六折芜湖！",
    "听首新歌": "好歌，加单了",
    "听首老歌": "我又觉得我行了",
    "洗个热水澡": "精神焕发",
    "洗个冷水澡": "太刺激了",
    "整理笔记": "头脑风暴走起",
    "撸猫": "太香了",
    "刷B站": "好多鸽子归巢了",
    "投稿": "叔叔还需要垃圾吗",
    "吃宵夜": "打着饱嗝入梦乡",
    "喝杯咖啡": "活过来了",
    "赶论文": "抢救成功了万岁！",
    "添衣": "看上去真暖和",
    "减衣": "看上去真凉快",
    "夜骑": "带上手电，去哪都行！",
    "夜跑": "健康生活的好选择",
    "晨跑": "一口气三公里轻轻松松",
    "唱歌": "好！很有精神！",
    "来把FPS": "直接拉出去哒哒哒全秒了不好看吗",
    "约个洗衣机": "久违的机械代替人力",
    "出黑板报": "评上了一等奖真不错",
    "剁手": "买都可以买",
    "准备pre": "妙语连珠",
    "分析案例": "有理有据，思路清晰",
    "做志愿": "分多活少高补贴",
    "打白工": "劳动最光荣",
    "网友见面": "《线上游戏的队友不可能是女生》",
    "和大佬贴贴": "届到了！",
    # CS
    "折腾": "今天整好了以后都不用管了",
    # xp类
    "击剑": "女人只会影响我拔剑的速度.jpg",
    "同床竞技": "您就是时间管理带师",
    "推旮": "会说话的纸片女人真是太香了",
    # 私货
    "作文":"学非文学类专业救不了中国人",
    "参赛": "拿牌",
    "给i宝修锅": "她好像变得更人了"
}

# 万事皆宜

忌 = {
    # 洛谷每日求签手动整理
    "熬夜": "爆肝",
    "装弱": "被看穿",
    "刷题": "容易WA",
    "搞基": "会被掰弯",
    "考试": "作弊会被抓",
    "吃饭": "小心变胖啊",
    "纳财": "然而今天并没有财运",
    "睡觉": "翻来覆去睡不着",
    "洗澡": "小心着凉",
    "写作文":  "可能会离题",
    "开电脑": "意外的死机故障不可避",
    "写作业": "上课讲了这些了吗",
    "泡妹子": "一定会被拒绝",
    "扶老奶奶过马路": "会被讹",
    "重构代码": "越改越乱",
    "膜拜大神": "被大神鄙视",
    "发朋友圈": "会被当做卖面膜的",
    "背诵课文": "记忆力只有50Byte",
    "体育锻炼": "消耗的能量全吃回来了",
    "打sdvx": "今天状态不好",
    "学习珂学": "珂朵莉不知干啥不理你",
    "参加模拟赛": "注意爆零",
    "继续完成WA的题": "然而变成了TLE",
    "打maimai": "怎么洗衣房变成洗脚房了？",
    # 日常
    ## 今日人品迁移
    "看番": "正版受害者是吧",
    "抽卡": "你就直接卖给我母猪石得了",
    "开车": "小心明天上灵车频道",
    "摸鱼": "被BOSS发现",
    "吹水": "被识破而社死",
    "打钱": "日你妈！退钱！",
    "看书": "这书也配卖钱？",
    "开封菜": "第二块鸡必腻",
    "金拱门": "他们还是滚回鬼畜区做唱片比较好",
    "华莱士": "在课上脱出来的话，学生生涯就结束了nari！",
    "冲": "别勉强自己冲",
    "买嘢": "哈哈你个憨批今天的价格比入的时候低20%",
    "白嫖": "闲鱼提醒您：请勿做梦",
    "拼车": "喂喂你想把我带去哪里啊.torrent",
    "表白": "赏了个德式拱桥摔",
    "沟通": "交涉失败，准备动手",
    "抓虫": "别在我代码里面繁殖啊！！！",
    "和irori聊天": "Traceback (most recent call last):",
    ## 
    "起稿": "过于放飞自我",
    "对线": "脸被打得稀烂",
    "复习": "看两行就困了",
    "理财": "永远别想从资本家的饼里挑出芝麻",
    "作曲": "你第二小节必撞车",
    "水群": "你知道自己有多ky吗",
    "骑自行车": "当心机械故障",
    "飙车": "道路千万条，安全第一条",
    "去图书馆": "好像都坐满了淦",
    "去空教室": "先后被排课赶来赶去人都傻了",
    "睡个午觉": "睡过头了，下午的课是不是点名了？",
    "拆快递": "哇！普通！",
    "寄快递": "提防暴力物流",
    "听首新歌": "这安利给我的是什么玩意",
    "听首老歌": "怎么又被下架了",
    "洗热水澡": "煞笔水龙头没烫死我",
    "洗冷水澡": "感冒预订",
    "整理笔记": "啥啥啥这写的都是啥",
    "撸猫": "被猫揍了还得去打疫苗",
    "刷B站": "一言难尽",
    "投稿": "成为黑历史",
    "吃宵夜": "太撑了根本睡不着",
    "使用公共微波炉": "薛定谔下了咒你根本不知道它是否在工作",
    "喝咖啡": "是真的难喝",
    "赶论文": "被程序已停止工作狠狠制裁了",
    "添衣": "怕不是要被热死",
    "减衣": "怕不是要被冻死",
    "夜骑": "你永远不知道影子里有什么等着你",
    "夜跑": "平地摔",
    "晨跑": "困死了",
    "唱歌": "这么小声还想开军舰？！",
    "打FPS": "WDNMD",
    "约洗衣机": "谁又把餐巾纸丢洗衣机里洗了？",
    "出黑板报": "画的这是什么玩意",
    "剁手": "把米留着它不香吗",
    "准备pre": "毫无头绪",
    "分析案例": "审不动了都死刑吧",
    "做志愿": "社恐老病又犯了",
    "打白工": "我们ICU见",
    "网友见面": "两只社恐谁都不敢认谁.jpg",
    "和大佬贴贴": "什么？这你都不会？",
    # CS
    "折腾": "我该听CSDN，博客园还是Stack Overflow？",
    # xp类
    "击剑": "华山论剑，小心碰头",
    "同床竞技": "杰哥不要啊（",
    "推旮": "小 心 系 统 音 量",
    # 私货
    "作文":"当代鲁迅一个字也发不出去",
    "参赛": "坐牢",
    "给i宝修锅": "mht的马和mirai总得有一个炸了"
}

运势 = ('特大吉', '大吉', '中吉', '小吉', '中平', '寄', '大寄', '危')
# 运势 = ('特大吉\n元旦快乐！', '特大吉\n新年快乐！')


# 诸事不宜


import requests
import copy


# def 信用点命令更新订阅姬(ent: CoreEntity):
#     """#信用点情报 []
#     查看今天用什么命令会对信用点产生影响
#     """
#     attrs = ent.chain.tostr().split(' ')
#     # arg = copy.deepcopy(ent)
#     ent.chain = MessageChain.get_empty()
#     if attrs and attrs[0] in C.unsubscribes:
#         # CreditSubscribe.chk(player).delete()
#         resp = requests.delete(
#             server_api('/worker/routiner'),
#             json={"ents": ent.json()}
#         )
#         if resp.status_code != 200:
#             return traceback.format_exc()
#         return [Plain('取消信用点命令更新订阅')]
#     ent.meta['call'] = 'info'
#     ent.meta['routiner'] = 'CreditInfoRoutiner'
#     resp = requests.options(
#         server_api('/worker/routiner'),
#         json={"ents": ent.json()}
#     ).json()

#     ret = [f'今天使用{resp["res"]}这些命令会有惊喜哦（']
#     if attrs and attrs[0] in C.subscribes:
#         resp = requests.post(
#             server_api('/worker/routiner'),
#             json={"ents": ent.json()}
#         )
#         if resp.status_code != 200:
#             return traceback.format_exc()
#         ret.append('订阅信用点命令更新')
#     return [Plain('\n'.join(ret))]

crdmap = [
    (-1000, ('全民公敌', '耗子尾汁')),
    (-500, ('在逃通缉', '联网自动追踪')),
    (-200, ('死刑立即执行', '点击预约行刑队')),
    (0, ('大祸患', '拯救一下')),
    (100, ('高危份子', '抢救一下')),
    (200, ('危险份子', '补救一下')),
    (300, ('贱民', '紧急涨分')),
    (500, ('市民一阶', '去涨分')),
    (600, ('市民二阶', '去涨分')),
    (700, ('市民三阶', '去涨分')),
    (800, ('优秀市民', '去涨分')),
    (900, ('模范市民', '去参加公务员考试')),
    (1000, ('二级科员', '去涨分')),
    (1500, ('一级科员', '去参加干部竞选')),
    (2000, ('副乡二十四级', '去涨分')),
    (2200, ('副乡二十三级', '去涨分')),
    (2300, ('副乡二十二级', '去涨分')),
    (2400, ('副乡二十一级', '去申请转正')),
    (2500, ('正乡二十级', '去涨分')),
    (2700, ('正乡十九级', '去涨分')),
    (2900, ('正乡十八级', '去涨分')),
    (3100, ('正乡十七级', '去申请晋级')),
    (3300, ('副县十六级', '去涨分')),
    (3600, ('副县十五级', '去申请转正')),
    (4000, ('正县十四级', '去涨分')),
    (4500, ('正县十三级', '去申请晋级')),
    (5000, ('副厅十二级', '去涨分')),
    (5600, ('副厅十一级', '去申请转正')),
    (6400, ('正厅十级', '去涨分')),
    (7300, ('正厅九级', '去申请晋级')),
    (8300, ('副省八级', '去涨分')),
    (9500, ('副省七级', '去申请转正')),
    (11000, ('正省六级', '去涨分')),
    (13000, ('正省五级', '去申请晋级')),
    (16000, ('副国四级', '去涨分')),
    (20000, ('副国三级', '去涨分')),
    (30000, ('副国二级', '去申请转正')),
    (50000, ('正国级', '去管理信用系统'))
]

def 评价(crd):
    if crd == 114514:
        return ('大 先 辈', '去造福社会')
    elif crd < -1000:
        return ('死刑立即执行', '点击预约行刑队')
    l = 0
    r = len(crdmap) - 1
    mid = (l + r + 1) >> 1
    while l < r:
        if crd >= crdmap[mid][0]: l = mid
        else: r = mid - 1
        mid = (l + r + 1) >> 1
    return crdmap[l][1]

def 成分查询(ent: CoreEntity):
    """#成分查询 []
    对群友的成分感到怀疑了？
    :param user: 群友的qq号
    :return:     群友的信用点和头衔
    """
    attrs = ent.chain.tostr().split(' ')
    user = attrs[0]
    crd = Player.chk(user).items.get('credit', 500)
    ret = [f'用户{user}现在拥有信用点{crd}点，评价：']
    ret.extend(评价(crd))
    return [Plain('\n'.join(ret))]

def 信用点查询(ent: CoreEntity):
    """#信用点查询 []
    查询你的信用点情况
    """
    user = ent.member
    player = Player.chk(user)
    # CreditLog.sync()
    # crd = CreditLog.get(player)
    crd = player.items.setdefault('credit', 500)
    # player.save()
    ret = [f'您现在拥有信用点{crd}点，评价：']
    ret.extend(评价(crd))
    return [Plain('\n'.join(ret))]



from mongoengine import *

class DailySignLog(RefPlayerBase, Document):
    combo = IntField(default=0)
    fortune = FloatField()
    y = ListField(StringField())
    j = ListField(StringField())
    remake_count = IntField()
    info = StringField()
    last_sign = DateTimeField()

class DailySignBackUP(Document):
    player = ReferenceField(Player)
    combo = IntField(default=0)
    info = StringField()
    last_sign = DateTimeField()

from collections import namedtuple

SignLog = namedtuple('SignLog', ('fortune', 'y', 'j', 'msg', 'rp'))

def gen_fortune(rp: float):
    d = len(运势)
    f = 100 / d
    for p, i in enumerate(运势):
        if 100 - (p+1) * f < rp:
           return i

def generate_sign_log(fortune_word_count: int) -> SignLog:
    rp = random.random() * 101
    fortune = gen_fortune(rp)

    # fortune = random.choice(运势)
    y = random.sample(宜.items(),fortune_word_count)
    t忌 = copy.deepcopy(忌)
    for yi in y: t忌.pop(yi[0],(0,False))
    j = random.sample(t忌.items(),fortune_word_count) # 防重
    if fortune in ('大吉','特大吉'): j = [('万事皆宜','')]
    if fortune in ('大凶','危'): y = [('诸事不宜','')]
    for p,i in enumerate(y): y[p] ='\t' + '\t'.join(i)
    for p,i in enumerate(j): j[p] ='\t' + '\t'.join(i)
    ans = f"{fortune} (运: {rp:.3f}%)\n\n宜:\n{chr(10).join(y)}\n\n忌:\n{chr(10).join(j)}\n\n"
    rep = SignLog(
        fortune=fortune,
        y=y,
        j=j,
        msg=ans,
        rp=rp,
    )
    return rep

def 改运(ent: CoreEntity):
    """#改运 []
    消耗信用点可以重新抽取今日运势，每日第一次消耗64点，之后每次费用加倍
    至于信不信就是你的事了
    用法：
        #改运 <抽取词条数=rand(2~5)>
    """
    mem = ent.member
    player = Player.chk(mem)

    sign = DailySignLog.chk(player)
    if not sign.last_sign or sign.last_sign.strftime('%Y-%m-%d') != datetime.datetime.now().strftime('%Y-%m-%d'):
        return '您今日还没求过签！'
    attrs = ent.chain.tostr()

    credit = player.items.setdefault('credit', 500)
    remake_cnt = sign.remake_count if sign.remake_count else 0
    cost = 64 << remake_cnt
    
    if cost > credit:
        return f'您的信用点不足以改运！{credit}/{cost}'
    ato = credit - cost
    player.items['credit'] = ato

    if attrs:
        cnt = int(attrs)
    else:
        cnt = random.randint(2, 5)
    
    rep = generate_sign_log(cnt)
    rp, ans = rep.rp, rep.msg
    sign.fortune = rp
    sign.remake_count = remake_cnt + 1
    sign.info = ans

    player.save()
    sign.save()
    return ans + f'\n消费了{cost}信用点，剩余{ato}点'




def 仿洛谷每日签到(ent: CoreEntity):
    """#求签 []
    用来获得你的今日运势（从洛谷收集的语料（别迷信了，真的
    """
    attrs = ent.chain.tostr().split(' ')
    fortune_word_count = random.randint(2,5)
    # print(kwargs['mem'])
    # print(dir(kwargs['mem']))
    mem = ent.member
    player = Player.chk(mem)
    entity = DailySignLog.chk(player)
    

    def to_datetime(s): return datetime.datetime.strptime(s, '%Y-%m-%d')
    is_dup = False
    # print('A', entity.last_sign.strftime('%Y-%m-%d'))
    # print('B', datetime.datetime.now().strftime('%Y-%m-%d'))
    if not entity.last_sign or entity.last_sign.strftime('%Y-%m-%d') != datetime.datetime.now().strftime('%Y-%m-%d'):
        if not entity.last_sign or entity.last_sign.strftime('%Y-%m-%d') != (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'):
            entity['combo'] = 0
        entity['combo'] += 1

        rep = generate_sign_log(fortune_word_count)

        rp, ans = rep.rp, rep.msg

        cd = math.ceil(rp/10) * entity['combo']
        bonus_hint = f"您已连续求签{entity['combo']}天\n\n今日奖励：信用点{cd}点"

        
        player.upd_credit('+', cd)
        entity['y'] = rep.y
        entity['j'] = rep.j
        entity['info'] = ans + bonus_hint
        entity['last_sign'] = datetime.datetime.now()
        entity['fortune'] = rp
        entity['remake_count'] = 0
        entity.save()
        DailySignBackUP(player=player, combo=entity.combo, info=entity.info, last_sign=entity.last_sign).save()

    else: 
        is_dup = True
        entity['info'] = '您今天已经求过签啦！以下是求签结果：\n' + entity['info']

    if '-render' in ent.meta: # 图片模块
        from PIL import Image as PImage
        from PIL import ImageDraw, ImageFont
        from basicutils.media import pimg_base64
        from fapi.models.Routiner import imaseconds
        import re
        def disassemble_msg(token: str, msg):
            t = re.search(token + r'\n(.*?)\n\n', msg, re.M | re.DOTALL).group(1)
            logger.debug(t)
            return t.split('\n')

        logger.debug(entity.to_mongo())
        rep = SignLog(
            fortune=gen_fortune(entity['fortune']),
            y=entity['y'] if 'y' in entity and entity['y'] else disassemble_msg('宜:', entity['info']),
            j=entity['j'] if 'j' in entity and entity['j'] else disassemble_msg('忌:', entity['info']),
            rp=entity['fortune'],
            msg='',
        )
        logger.debug(rep)


        tegaki_zatsu = 'Assets/851tegaki_zatsu_normal_0883.ttf'
        seto_font = 'Assets/setofont.ttf'

        font_tegaki = ImageFont.truetype(tegaki_zatsu, 24)

        fortune_size = 80
        font_fortune = ImageFont.truetype(seto_font, fortune_size)
        rp_size = 20
        font_rp = ImageFont.truetype(seto_font, rp_size)

        font_yj = ImageFont.truetype(seto_font, 40)

        emotion_type = 'B' if rep.rp >= 62.5 else ('C' if rep.rp <= 37.5 else 'N')
        time_now = imaseconds()
        time_period = 'light' if time_now > 6 * 3600 else ('normal' if 19*3600 > time_now > 12*3600 else 'dark')

        template = PImage.open(f'Assets/sign/alpha/small/{emotion_type}{time_period}.png').convert('RGBA')

        if '-color' in ent.meta:
            backgroundRGB = ent.meta['-color']
            if ',' in backgroundRGB:
                backgroundRGB = (int(i) for i in backgroundRGB.split(','))
            if '#' == backgroundRGB[:1]:
                backgroundRGB = (int(i, 16) for i in (backgroundRGB[x:x+2] for x in range(len(backgroundRGB)>>1)))
            while len(backgroundRGB) < 4:
                backgroundRGB += (255,)
        else:
            backgroundRGB = random.randint(0,255), random.randint(0,255), random.randint(0,255), 255
        background_grey = backgroundRGB[0] * 0.299 + backgroundRGB[1] * 0.587 + backgroundRGB[2] * 0.114

        layer3 = PImage.new('RGBA',template.size,backgroundRGB) # 上底色
        w, h = template.size

        font_color = (255, 255, 255, 255) if background_grey < 128 else (0, 0, 0, 255)

        template = PImage.alpha_composite(layer3,template,)

        layer2 = PImage.new('RGBA',template.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer2)

        fortune = gen_fortune(rep.rp)

        def write_center(text, font, height, percentage=0.5):
            lines = text.split('\n')
            W = max(font.getsize(tx)[0] for tx in lines)
            draw.text(((w-W)*percentage , height), text, fill=font_color, font=font)

        write_center(fortune, font_fortune, h * 0.04)
        write_center(f"{rep.rp:.3f}%", font_rp, h * 0.115)
        write_center("宜", font_yj, h * 0.142, 0.5)
        write_center("忌", font_yj, h * 0.310, 0.5)

        def write_yj_items(li: List[str], font, begin_height):
            H = font.getsize(li[0])[1]
            for i in li:
                C = i.strip().split('\t')
                if len(C) == 2:
                    A, B = C
                    draw.text((w * 0.05 , begin_height), A, fill=font_color, font=font)
                    draw.text((w * 0.95 , begin_height), B, fill=font_color, font=font, anchor='ra')
                else:
                    write_center(C[0], font, begin_height)
                begin_height += H

        write_yj_items(rep.y, font_tegaki, h*0.183)
        write_yj_items(rep.j, font_tegaki, h*0.351)

        # PImage.alpha_composite(template,layer2)

        return [Image(base64=pimg_base64(PImage.alpha_composite(template,layer2)))]


    return [Plain(entity['info'])]

def get_cryptocurrencies():
    r = requests.get(
        f'''https://www.nasdaq.com/market-activity/cryptocurrency''',
        headers={
            "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding":"gzip, deflate, br",
            "accept-language":"zh-CN,zh;q=0.9",
            "cache-control":"no-cache",
            "dnt":"1",
            "pragma":"no-cache",
            "sec-fetch-mode":"navigate",
            "sec-fetch-site":"none",
            "sec-fetch-user":"?1",
            "upgrade-insecure-requests":"1",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }
    )
    res = r.text
        # print(res)
    b = BeautifulSoup(res, 'html.parser')
    ccs = [i['data-symbol'] for i in b('tr', attrs={'data-asset-class':'cryptocurrency'})]
    # print(ccs)
    return ccs

def fetch_cryptocurrency_info(typ: str = 'BTC'):
    lnk = f'https://api.nasdaq.com/api/quote/{typ}/info?assetclass=crypto'
    r = requests.get(lnk, headers={
        "accept":"application/json, text/plain, */*",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"zh-CN,zh;q=0.9",
        "cache-control":"no-cache",
        "dnt":"1",
        "origin":"https://www.nasdaq.com",
        "pragma":"no-cache",
        "referer":"https://www.nasdaq.com/market-activity/cryptocurrency/btc",
        "sec-fetch-dest":"empty",
        "sec-fetch-mode":"cors",
        "sec-fetch-site":"same-site",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    })
    j = json.loads(r.text)
    report = (f"币种：{j['data']['companyName']}\n"
    # f"今日最高：{j['data']['keyStats']['High']['value']}\n"
    # f"今日最低：{j['data']['keyStats']['Low']['value']}\n"
    f"现在价格：{j['data']['primaryData']['lastSalePrice']}\n"
    f"刷新时间：{j['data']['primaryData']['lastTradeTimestamp']}\n"
    f"变动幅度：{j['data']['primaryData']['percentageChange']}")

    return report, j

def 炒币模拟器(ent: CoreEntity):
    """#炒币 [#超笔]
    谨以此功能纪念20年末矿潮，向想炒币但没钱也不想花钱的用户提供。
    本功能所有数据以nasdaq为依据。
    用法：
        #炒币 typ
            查看支持的币种列表
        #炒币 info <币种>
            查看对应币种的行情
        #炒币 buy <币种> $<信用点数>
            购买相当于这么多信用点的币
        #炒币 buy <币种> <币个数>
            购买这么多个币
        #炒币 sell <币种> $<信用点数>
            卖出相当于这么多信用点的币（税前）
        #炒币 sell <币种> <币个数>
            卖出这么多币
        #炒币 my
            查看您拥有币的数量

    """
    attrs = ent.chain.tostr().split(' ')

    if not any(attrs):
        return '请使用"#h #炒币"查看具体用法'
    else:
        cmd, *args = attrs
        if cmd == 'typ':
            return "支持的币种列表：['BTC', 'ETH', 'XRP', 'BCH', 'ADA', 'LTC', 'XEM', 'XLM', 'EOS', 'NEO', 'MIOTA', 'DASH', 'XMR', 'TRX', 'XTZ', 'DOGE', 'ETC', 'VEN', 'USDT', 'BNB']"
            # li = get_cryptocurrencies()
            # logger.debug(li)
            # return ['支持的币种列表：'] + li
        elif cmd == 'info':
            return fetch_cryptocurrency_info(args[0])[0]
        elif cmd == 'buy':
            typ, qty, *ato = args
            typ = typ.upper()
            player = Player.chk(ent.member)
            rate = float(fetch_cryptocurrency_info(typ)[1]['data']['primaryData']['lastSalePrice'][1:])
            if '$' in qty:
                qty = float(qty.replace('$', ''))
                cnt = qty / rate
            else:
                cnt = float(qty)
                qty = float(qty) * rate
            credit = player.items.setdefault('credit', 500)
            if credit < qty:
                return f'您的信用点不足，仍需另外{qty-credit}点才能买入'
            credit -= qty
            player.items.setdefault('cryptocurrency', {})
            player.items['cryptocurrency'][typ] = player.items['cryptocurrency'].get(typ, 0) + cnt
            player.items['credit'] = credit
            player.save()
            return f'购买成功：花费{qty}信用点，买入{cnt}单位的{typ}。'
        elif cmd == 'sell':
            typ, qty, *ato = args
            typ = typ.upper()
            player = Player.chk(ent.member)
            rate = float(fetch_cryptocurrency_info(typ)[1]['data']['primaryData']['lastSalePrice'][1:])

            if '$' in qty:
                qty = float(qty.replace('$', ''))
                cnt = qty / rate
            else:
                cnt = float(qty)
                qty = float(qty) * rate
            player.items.setdefault('credit', 500)
            player.items.setdefault('cryptocurrency', {})
            cc = player.items['cryptocurrency'].setdefault(typ, 0)
            if cc < cnt:
                return f'您的{typ}不足，还需{cnt - cc}才能卖出您期望的信用点（手续费前）'
            cc -= cnt
            tax = qty * 0.01
            qty *= 0.99
            player.items['credit'] += qty
            player.items['cryptocurrency'][typ] = cc
            player.save()
            return f"卖出成功：卖出{typ}共{cnt}单位，获得{qty}信用点，系统收取手续费{tax}(1%)。"
        elif cmd == 'my':
            player = Player.chk(ent.member)
            player.items.setdefault('credit', 500)
            ret = []
            # player.
            for k, v in player.items.setdefault('cryptocurrency', {}).items():
                ret.append(f'{k}: {v}')
            if not ret:
                return '您没有币！'
            else:
                return '\n'.join(['您拥有的币如下：', '币种   数量'] + ret)

            # return
        else:
            return '请使用"#h #炒币"查看具体用法'

