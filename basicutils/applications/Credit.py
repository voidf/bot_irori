"""信用点类"""
import os
import sys
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

# if __name__ == '__main__':
    # os.chdir('..')
# print(os.listdir('.'))
# print(__name__)
import basicutils.CONST as GLOBAL
import asyncio
import random
import copy
import traceback
import datetime
import mido
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
from Assets.签到语料 import 宜, 忌, 运势
import requests
import copy


def 信用点命令更新订阅姬(ent: CoreEntity):
    """#信用点情报 []
    查看今天用什么命令会对信用点产生影响
    """
    attrs = ent.chain.tostr().split(' ')
    # arg = copy.deepcopy(ent)
    ent.chain = MessageChain.get_empty()
    if attrs and attrs[0] in GLOBAL.unsubscribes:
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
    if attrs and attrs[0] in GLOBAL.subscribes:
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
    elif crd < 0:
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
        fortune = random.choice(运势)
        y = random.sample(宜.items(),generate_key_count)
        t忌 = copy.deepcopy(忌)
        for yi in y: t忌.pop(yi[0],(0,False))
        j = random.sample(t忌.items(),generate_key_count) # 防重
        if fortune in ('大吉','特大吉'): j = [('万事皆宜','')]
        if fortune in ('大凶','危'): y = [('诸事不宜','')]
        for p,i in enumerate(y): y[p] ='\t' + '\t'.join(i)
        for p,i in enumerate(j): j[p] ='\t' + '\t'.join(i)
        cd = random.randint(1,8) * entity['combo']
        ans = f"{fortune}\n\n宜:\n{chr(10).join(y)}\n\n忌:\n{chr(10).join(j)}\n\n您已连续求签{entity['combo']}天\n\n今日奖励：信用点{cd}点"
        player.upd_credit('+', cd)
        entity['info'] = ans
        entity['last_sign'] = datetime.datetime.now()
        entity.save()
        DailySignBackUP(player=player, combo=entity.combo, info=entity.info, last_sign=entity.last_sign).save()

    else: entity['info'] = '您今天已经求过签啦！以下是求签结果：\n' + entity['info']
    return [Plain(entity['info'])]

