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