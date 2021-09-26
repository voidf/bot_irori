"""异步与文件读写类(修复完毕)"""
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

# async def 中药(*attrs, kwargs={}):
#     """群友贡献的中药笔记整理
#     按名称查询某个中药信息：
#     #中药 [药名]
#     搜索中药信息：
#     #中药 搜索 [搜索关键字]"""
#     renderli = [] # int
#     premsg = ''
#     def _render():
#         out = []
#         ks = GLOBAL.中药title
#         for i in renderli:
#             cur = GLOBAL.中药[i].split('^^')
#             for p, j in enumerate(ks):
#                 out.append(f"{j}:{cur[p]}")
#             out.append("\n")
#         return premsg + '\t'.join(out)

#     def _scan(keyword):
#         for p, i in enumerate(GLOBAL.中药):
#             if re.search(keyword, i, re.S):
#                 renderli.append(p)

#     if attrs[0] in ("搜索", "scan", "search"):
#         _scan(attrs[1])
#         premsg = f"检索结果：{len(renderli)}条：\n"
        
#     else:
#         if attrs[0] in GLOBAL.中药名索引:
#             renderli.append(GLOBAL.中药名索引[attrs[0]])
#         else:
#             _scan(attrs[0])
#             premsg = "没有这种药，您可能在找：\n"
#     return [Plain(_render())]

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
    crd = CreditLog.get(user)
    ret = [f'用户{user}现在拥有信用点{crd}点，评价：']
    ret.extend(评价(crd))
    return [Plain('\n'.join(ret))]

def 信用点查询(ent: CoreEntity):
    """#信用点查询 []
    查询你的信用点情况
    """
    user = ent.member
    player = Player.chk(user, ent.source)
    crd = CreditLog.get(player)
    ret = [f'您现在拥有信用点{crd}点，评价：']
    ret.extend(评价(crd))
    return [Plain('\n'.join(ret))]

from mongoengine import *

# async def 投票姬(*attrs, kwargs={}):
#     mem = str(getattr(kwargs['mem'],'id',kwargs['mem']))
#     gp = str(getattr(kwargs['mem'],'id',kwargs['mem']))
#     l = list(attrs)

#     player = get_player(**kwargs)
    
#     j = Vote.chk(player)
   
#     ostr = []
#     if len(l) == 1:
#         if l[0] == 'chk':
#             for k,v in j.items.items():
#                 ostr.append(Plain(text=f'{k}:\t{len(v)}票\n'))
#             return ostr
#         elif l[0] == 'my':
#             ostr.append(Plain(text='宁投给了：'))
#             for i in j.memberChoices.get(mem,[]):
#                 ostr.append(Plain(text=f'{i} '))
#             return ostr
            
#     if l[0] == 'new':
#         newItem = ' '.join(l[1:])
#         if newItem in j.items:
#             return [Plain(text='创建失败：已存在此条目')]
#         else:
#             j.items[newItem] = []
#             ostr.append(Plain(text=f'''添加成功,现有条目数:{len(j.items)}\n'''))
#     elif l[0] in ('limit','lim'):
#         j.limit = int(l[1])
#         if j.limit < 1:
#             raise NameError('只能设置限票数为正整数')
#         ostr.append(Plain(text=f'''现在每人可以投{j.limit}票'''))

#     elif l[0] in ('del','rm'):
#         sel = ' '.join(l[1:])
#         if sel not in j.items:
#             return [Plain(text='删除失败：不存在此条目')]
#         else:
#             del j.items[sel]
#             for i in j.memberChoices:
#                 try:
#                     j['memberChoices'][i].remove(sel)
#                     print('有选择的用户:',i)
#                 except:
#                     pass
#             ostr.append(Plain(text='''删除成功'''))
#     elif l[0] == '-*/clear/*-':
#         j.delete()
#         ostr.append(Plain(text='''清空成功'''))
#     else:
#         selectedItem = ' '.join(l)
#         if selectedItem not in j['items']:
#             return [Plain(text='投票失败：不存在此条目')]
#         if selectedItem in j['memberChoices'].get(mem,[]):
#             return [Plain(text='投票失败：您已投过此条目')]
#         else:
#             try:
#                 if mem not in j['memberChoices']:
#                     j['memberChoices'][mem] = [selectedItem]
#                     j['items'][selectedItem].append(mem)
#                 elif len(j['memberChoices'][mem]) < j['limit']:
#                     j['memberChoices'][mem].append(selectedItem)
#                     j['items'][selectedItem].append(mem)
#                 else:
#                     j['memberChoices'][mem].append(selectedItem)
#                     j['items'][selectedItem].append(mem)
#                     while len(j['memberChoices'][mem]) > j['limit']:
#                         j['items'][j['memberChoices'][mem][0]].remove(mem)
#                         del j['memberChoices'][mem][0]
#             except Exception as e:
#                 return [Plain(text=str(e))]
#             ostr.append(Plain(text=f'''投票成功，条目{selectedItem}当前已有{len(j['items'][selectedItem])}票\n'''))
#     j.save()
#     return ostr

def ddl通知姬(ent: CoreEntity):
    """#ddl []
    防侠提醒器，可用参数：
        new <事件名称> <到期时间[年,][月,][日,][时,][分,]<秒>>（新建事件）
        del <事件名称>（删除事件）
        ls（列出事件）
        now (噢我的上帝看看现在都几点了(公会战)(公会战)(公会战)(公会战)(公会战)(公会战).jpg)
        使用new时注意需传入时间，格式年,月,日,时,分,秒；秒必填，其余不填则按照现在的时间自动补齐
    例:
        #ddl new 打pcr 10,00,00
        即在今天10点设置提醒
    """

    attrs = ent.chain.tostr().split(' ')
    ent.chain.__root__.clear()
    ent.meta['routiner'] = 'DDLNoticeRoutiner'


    ostr = []
    try:
        if len(attrs):
            if attrs[0] == 'new':
                s = attrs[1]
                # if s in entity.content:
                cp = datetime.datetime.now()
                st = ' '.join(attrs[2:])

                ss = [__ for __ in st.split(',')]
                if len(ss) == 0:
                    return [Plain('未输入时间')]
                elif len(ss)>6:
                    return [Plain('我不会算这种时间格式(闭眼)')]
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
                    ent.meta['ts'] = t.timestamp()
                    ent.meta['title'] = s
                    resp = requests.post(
                        server_api('/worker/routiner'),
                        json={'ents': ent.json()}
                    )
                    if resp.status_code != 200:
                        return resp.text
                    elif resp.json()['res'] == False:
                        return [Plain('日程表里有了相同的东西，考虑换个名？')]
                else:
                    return [Plain(random.choice(['你的日程真的没问题喵（？','噔 噔 咚！这件事已经过期了']))]
                ostr.append(Plain(random.choice(['好啦好啦会提醒你了啦','防侠提醒加入成功...TO BE CONTINUE ==>','不是，调个闹钟不比我香吗¿'])))
            elif attrs[0] in ('rm','del'):
                s = attrs[1]
                ent.meta['title'] = s
                resp = requests.delete(
                    server_api('/worker/routiner'),
                    json={'ents': ent.json()}
                )
                if resp.status_code != 200:
                    return resp.text
                logger.info(resp.json())
                if resp.json()['res'] == False:
                    return [Plain('没有事先设定过这样的日程哦！')]
                ostr.append(Plain(s+'被我干♀掉了'))
            elif attrs[0] in ('ls','chk'):
                ent.meta['call'] = 'info'
                # ent.meta
                resp = requests.options(
                    server_api('/worker/routiner'),
                    json={'ents': ent.json()}
                )
                if resp.status_code != 200:
                    return resp.text

                ostr.append(Plain(text=f'日程表:\n{resp.json()["res"] if resp.json()["res"] else "空的！"}'))
            elif attrs[0] in ('t','time','now'):
                ostr.append(Plain(f'{datetime.datetime.now()}'))
    except Exception as e:
        logger.error(traceback.format_exc())
        ostr.append(Plain('\n【出错】'+str(e)))
    return ostr
    
# async def 数电笔记(*attrs, kwargs={}):
#     ins = ' '.join(attrs)
#     if ins == 'ls':
#         return [Plain('\n'.join(GLOBAL.DEKnowledge.keys()))]
#     elif ins == 'reload':
#         ret_msg = [Plain('知识库已更新,现有词条：\n')]
#         for i in os.listdir('DigitalElectronicsTech'):
#             if i[-6:]=='.json5':
#                 with open('DigitalElectronicsTech/'+i,'r') as f: 
#                     j = json5.load(f)
#                 for k,v in j.items():
#                     ret_msg.append(Plain('\t- '+k+'\n'))
#                     GLOBAL.DEKnowledge[k] = [Plain(f'''{k}\n别名:{v['AN']}\n{v['desc']}''')]
#                     if 'img' in v:
#                         for vi in v['img']:
#                             GLOBAL.DEKnowledge[k].append(generateImageFromFile('DigitalElectronicsTech/img/'+vi))
#                     for an in v['AN']:
#                         GLOBAL.DEKnowledge[an] = GLOBAL.DEKnowledge[k]
#         return ret_msg
#     elif ins in GLOBAL.DEKnowledge:
#         return GLOBAL.DEKnowledge[ins]
#     else:
#         return [Plain('不存在此条目')]
import base64
def 在线P歌(ent: CoreEntity):
    """#P歌 [#P]
    传入音符，合成midi
    例：
        #P歌 C5 C5 G5 G5 A6 A6 G5
    TODO:
        加入音长，音量设置
    """
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

    for i in ent.chain.tostr().split():
        if i and i != '0':
            note = note_map[i[:-1]]+int(i[-1])*12
            t.append(mido.Message('note_on', note=note, velocity=120, time=0))
            t.append(mido.Message('note_off', note=note, velocity=120, time=480))
        else:
            t.append(mido.Message('note_on', note=60, velocity=0, time=0))
            t.append(mido.Message('note_off', note=60, velocity=0, time=480))
    # fn = f'tmp{randstr(4)}.mid'
    # m.save(fn)
    bio = BytesIO()
    m.save(file=bio)
    bio.seek(0)
    b64 = base64.b64encode(bio.read()).decode('utf-8')
    
    # with open(fn, 'rb') as f:
        # bts = f.read()
    # v = Voice(url=convert_file_to_amr('mid', fn))
    v = Voice(base64=b64)
    # asyncio.ensure_future(rmTmpFile(fn))
    # kwargs['-voice'] = True
    # kwargs['voices'] = [fn]
    # kwargs['voices-fm'] = 'mid'
    # os.remove(fn)
    return [v]

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
        print(CreditLog.upd(player, '+', cd))
        entity['info'] = ans
        entity['last_sign'] = datetime.datetime.now()
        entity.save()
        DailySignBackUP(player=player, combo=entity.combo, info=entity.info, last_sign=entity.last_sign).save()

    else: entity['info'] = '您今天已经求过签啦！以下是求签结果：\n' + entity['info']
    return [Plain(entity['info'])]

functionMap = {
    # '#vote':投票姬,
    # '#i电':数电笔记,
    # '#求签':仿洛谷每日签到,
    # '#信用点查询': 信用点查询,
    # '#信用点情报': 信用点命令更新订阅姬
}

shortMap = {
    # '#iee':'#i电',
}

functionDescript = {
    # '#信用点情报':'',
    # '#信用点查询':'',
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
    
    '#i电':
"""
查查某些集成电路的手册（自己整理的
可用参数:
    reload (热重载知识库)
用例:
    #i电 74283
""",

}