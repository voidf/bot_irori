"""信用点类"""
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
    "参赛": "坐牢",
    "给i宝修锅": "mht的马和mirai总得有一个炸了"
}

运势 = ('特大吉', '大吉', '中吉', '小吉', '中平', '凶', '大凶', '危')
# 运势 = ('特大吉\n元旦快乐！', '特大吉\n新年快乐！')


# 诸事不宜


import requests
import copy


def 信用点命令更新订阅姬(ent: CoreEntity):
    """#信用点情报 []
    查看今天用什么命令会对信用点产生影响
    """
    attrs = ent.chain.tostr().split(' ')
    # arg = copy.deepcopy(ent)
    ent.chain = MessageChain.get_empty()
    if attrs and attrs[0] in C.unsubscribes:
        # CreditSubscribe.chk(player).delete()
        resp = requests.delete(
            server_api('/worker/routiner'),
            json={"ents": ent.json()}
        )
        if resp.status_code != 200:
            return traceback.format_exc()
        return [Plain('取消信用点命令更新订阅')]
    ent.meta['call'] = 'info'
    ent.meta['routiner'] = 'CreditInfoRoutinuer'
    resp = requests.options(
        server_api('/worker/routiner'),
        json={"ents": ent.json()}
    ).json()

    ret = [f'今天使用{resp["res"]}这些命令会有惊喜哦（']
    if attrs and attrs[0] in C.subscribes:
        resp = requests.post(
            server_api('/worker/routiner'),
            json={"ents": ent.json()}
        )
        if resp.status_code != 200:
            return traceback.format_exc()
        ret.append('订阅信用点命令更新')
    return [Plain('\n'.join(ret))]

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
    crd = Player.chk(user, ent.source).items.get('credit', 500)
    ret = [f'用户{user}现在拥有信用点{crd}点，评价：']
    ret.extend(评价(crd))
    return [Plain('\n'.join(ret))]

def 信用点查询(ent: CoreEntity):
    """#信用点查询 []
    查询你的信用点情况
    """
    user = ent.member
    player = Player.chk(user, ent.source)
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
    info = StringField()
    last_sign = DateTimeField()

class DailySignBackUP(Document):
    player = ReferenceField(Player)
    combo = IntField(default=0)
    info = StringField()
    last_sign = DateTimeField()

def 仿洛谷每日签到(ent: CoreEntity):
    """#求签 []
    用来获得你的今日运势（从洛谷收集的语料（别迷信了，真的
    """
    attrs = ent.chain.tostr().split(' ')
    generate_key_count = random.randint(2,5)
    # print(kwargs['mem'])
    # print(dir(kwargs['mem']))
    mem = ent.member
    player = Player.chk(mem, ent.source)
    entity = DailySignLog.chk(player)
    

    def to_datetime(s): return datetime.datetime.strptime(s, '%Y-%m-%d')
    # print('A', entity.last_sign.strftime('%Y-%m-%d'))
    # print('B', datetime.datetime.now().strftime('%Y-%m-%d'))
    if not entity.last_sign or entity.last_sign.strftime('%Y-%m-%d') != datetime.datetime.now().strftime('%Y-%m-%d'):
        if not entity.last_sign or entity.last_sign.strftime('%Y-%m-%d') != (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'):
            entity['combo'] = 0
        entity['combo'] += 1

        rp = random.random() * 100
        d = len(运势)
        f = 100 / d
        for p, i in enumerate(运势):
            if 100 - (p+1) * f < rp:
                fortune = i
                break

        # fortune = random.choice(运势)
        y = random.sample(宜.items(),generate_key_count)
        t忌 = copy.deepcopy(忌)
        for yi in y: t忌.pop(yi[0],(0,False))
        j = random.sample(t忌.items(),generate_key_count) # 防重
        if fortune in ('大吉','特大吉'): j = [('万事皆宜','')]
        if fortune in ('大凶','危'): y = [('诸事不宜','')]
        for p,i in enumerate(y): y[p] ='\t' + '\t'.join(i)
        for p,i in enumerate(j): j[p] ='\t' + '\t'.join(i)
        cd = random.randint(1,8) * entity['combo']
        ans = f"{fortune} (运: {rp:.3f}%)\n\n宜:\n{chr(10).join(y)}\n\n忌:\n{chr(10).join(j)}\n\n您已连续求签{entity['combo']}天\n\n今日奖励：信用点{cd}点"
        player.upd_credit('+', cd)
        entity['info'] = ans
        entity['last_sign'] = datetime.datetime.now()
        entity.save()
        DailySignBackUP(player=player, combo=entity.combo, info=entity.info, last_sign=entity.last_sign).save()

    else: entity['info'] = '您今天已经求过签啦！以下是求签结果：\n' + entity['info']
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
    f"今日最高：{j['data']['keyStats']['High']['value']}\n"
    f"今日最低：{j['data']['keyStats']['Low']['value']}\n"
    f"现在价格：{j['data']['primaryData']['lastSalePrice']}\n"
    f"刷新时间：{j['data']['primaryData']['lastTradeTimestamp']}\n"
    f"变动幅度：{j['data']['primaryData']['percentageChange']}")

    return report, j

def 炒币模拟器(ent: CoreEntity):
    """#炒币 []
    谨以此功能纪念20年末矿潮，向想炒币但没钱也不想花钱的用户提供。

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
            player = Player.chk(ent.member, ent.source)
            rate = float(fetch_cryptocurrency_info(typ)[1]['data']['primaryData']['lastSalePrice'][1:])
            if '$' in qty:
                qty = float(qty.replace('$', ''))
                cnt = qty / rate
            else:
                cnt = qty
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
            player = Player.chk(ent.member, ent.source)
            rate = float(fetch_cryptocurrency_info(typ)[1]['data']['primaryData']['lastSalePrice'][1:])

            if '$' in qty:
                qty = float(qty.replace('$', ''))
                cnt = qty / rate
            else:
                cnt = qty
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
            player = Player.chk(ent.member, ent.source)
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

