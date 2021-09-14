from asyncio.tasks import ensure_future
from basicutils.applications.File import ddl通知姬
from time import sleep
from typing import Union
from loguru import logger

from mido.messages.messages import Message
from mongoengine.fields import DateTimeField, IntField, StringField
from basicutils import chain
import fapi.G

from fapi.models.Base import *
from mongoengine import *
import aiohttp
import asyncio
import math
import datetime
from basicutils.network import CoreEntity
from mongoengine import *
from fapi.models.Auth import *

routiner_namemap = {} # 根据名字查找Routinuer用

class Routiner(Base, Document):
    meta = {'allow_inheritance': True}
    adapter = ReferenceField(Adapter)
    player = ReferenceField(Player)

    @classmethod
    async def recover_routiners(cls, aid: str):
        """总恢复入口，不能被重载"""
        for sc in cls.__subclasses__():
            logger.info(f'{sc} is initializing...')
            await sc.resume(aid)
            routiner_namemap[sc.__name__] = sc

    @classmethod
    async def resume(cls, aid: str):
        """启动入口，可以放点静态的东西，最好得包括一个future_map"""
        raise NotImplementedError
    
    @classmethod
    async def cancel(cls, aid: str, pid: str, meta: dict={}):
        """取消订阅接口"""
        raise NotImplementedError
    
    @classmethod
    async def add(cls, aid: str, pid: str, meta: dict={}):
        """添加订阅接口"""
        raise NotImplementedError

    # @classmethod
    # async def mainloop(cls, aid: str):
    #     raise NotImplementedError

class CodeforcesRoutinuer(Routiner):
    mode = StringField(default='Y')

    @staticmethod
    async def spider():
        ses: aiohttp.ClientSession
        async with aiohttp.ClientSession() as ses:
            resp: aiohttp.ClientResponse
            li = []
            async with ses.get('https://codeforces.com/api/contest.list', timeout=30) as resp:
                j = (await resp.json())['result']
                for i in j:
                    if i['phase'] == 'FINISHED':
                        break
                    li.append(i)
                    """
                    可用属性：
                    id                  比赛id
                    name                比赛名
                    startTimeSeconds    开始时间戳
                    relativeTimeSeconds 为负数时表示还差多少秒开始
                    durationSeconds     时长

                    """
                    
        return li

    @classmethod
    async def notify(cls, contest: dict):
        # if isinstance(player, Player):
        #     player = str(player.pid)
        if contest['relativeTimeSeconds'] < 3600:
            return
        await asyncio.sleep(contest['relativeTimeSeconds'] - 3600)
        q = cls.objects()
        # if q:
        for subs in q:
            if str(subs.adapter) in fapi.G.adapters:
                await fapi.G.adapters[str(subs.adapter)].upload(
                    CoreEntity(
                        player=str(subs.player),
                        chain=chain.MessageChain.auto_make(
                            f"比赛【{contest['name']}】还有不到1小时就要开始了...\n" + 
                            f"注册链接：https://codeforces.com/contestRegistration/{contest['id']}"
                        ),
                        source='',
                        meta={}
                    )
                )

    @classmethod
    async def update_futures(cls):
        # q = cls.objects(adapter=Adapter.trychk(aid))
        # if q:
        li = await CodeforcesRoutinuer.spider()
            # for subscribers in q:
                # mp = cls.contest_futures.setdefault(str(aid), {}).setdefault(str(subscribers.player), {})
        mp =  cls.contest_futures
        for contest in li:
            if contest['id'] in mp:
                mp[contest['id']].cancel()
            mp[contest['id']] = asyncio.ensure_future(
                cls.notify(contest)
            )

    @classmethod
    async def resume(cls, aid: str):
        if not fapi.G.initialized:
            cls.contest_futures = {}
            await cls.update_futures()
            asyncio.ensure_future(cls.mainloop())


    @classmethod
    async def mainloop(cls):
        cycle = 86400
        offset = 3600 * 8 # UTC+8, 24 - 8 = 16
        while 1:
            tosleep = cycle - (datetime.datetime.now().timestamp() + offset) % cycle
            await asyncio.sleep(tosleep)
            await cls.update_futures()

    @classmethod
    async def cancel(cls, aid: str, pid: str, meta: dict={}):
        cls.objects(adapter=Adapter.trychk(aid), player=Player.chk(pid)).delete()

    @classmethod
    async def add(cls, aid: str, pid: str, meta: dict={}):
        cls(
            player=Player.chk(pid),
            adapter=Adapter.trychk(aid),
            mode='Y',
        ).save()
        # await cls.update_futures(aid)

import random
import basicutils.CONST as CONST
from Worker import import_applications
class CreditInfoRoutinuer(Routiner):
    @classmethod
    async def info(cls, meta: dict={}):
        return ','.join(list(cls.credit_cmds.keys()))
    @classmethod
    async def resume(cls, aid: str):
        logger.debug(f'{cls} resume called')
        # cls.future_map = {}
        if not fapi.G.initialized:
            cls.call_map = {
                'info': cls.info
            }
            cls.credit_cmds = {}
            # print(cls)
            # print(cls.call_map)

            await cls.update_futures()
            asyncio.ensure_future(cls.mainloop())
            logger.info(f'{cls} initialized')


    @classmethod
    async def mainloop(cls):
        cycle = 86400
        offset = 3600 * 8 # UTC+8, 24 - 8 = 16
        while 1:
            tosleep = cycle - (datetime.datetime.now().timestamp() + offset) % cycle
            await asyncio.sleep(tosleep)
            await cls.update_futures()

    @classmethod
    async def update_futures(cls):
        logger.info('重置可用信用点命令...')
        app_fun, app_doc, tot_funcs, tot_alias = import_applications()
        tot = len(tot_funcs)
        ctr = random.randint(min(3, tot), min(9, tot))
        fs = random.sample(tot_funcs.keys(), k=ctr)
        op = random.choices(CONST.credit_operators, CONST.credit_operators_weight, k=ctr)
        vl = random.choices(range(1,5), k=ctr)
        cls.credit_cmds = {k:v for k, *v in zip(fs, op, vl)}
        q = cls.objects()
        # if q:
        for subs in q:
            await fapi.G.adapters[str(subs.adapter)].upload(
                CoreEntity(
                    player=str(subs.player),
                    chain=chain.MessageChain.auto_make(
                        f'今天使用{await cls.info()}这些命令会有惊喜哦（'
                    ),
                    source='',
                    meta={}
                )
            )

    @classmethod
    async def cancel(cls, aid: str, pid: str, meta: dict={}):
        cls.objects(adapter=Adapter.trychk(aid), player=Player.chk(pid)).delete()

    @classmethod
    async def add(cls, aid: str, pid: str, meta: dict={}):
        cls(
            player=Player.chk(pid),
            adapter=Adapter.trychk(aid)
        ).save()


from basicutils.chain import *
class DDLNoticeRoutiner(Routiner):
    ddl = DateTimeField()
    title = StringField()
    mem = IntField()
    @classmethod
    async def info(cls, meta: dict={}):
        aid = meta['aid']
        pid = meta['pid']
        li = []
        for subs in cls.objects(adapter=Adapter.chk(aid), player=Player.chk(pid)):
            li.append(f"{str(subs.ddl)}    {subs.title}")
        return '\n'.join(li)
    @classmethod
    async def resume(cls, aid: str):
        logger.debug(f'{cls} resume called')
        cls.call_map = {
            'info': cls.info
        }
        cls.future_map = {}
        aid = Adapter.trychk(aid)
        for subs in cls.objects(adapter=aid):
            await cls.routine(aid, subs)
        # asyncio.ensure_future(cls.mainloop())
        logger.info(f'{cls} initialized')


    @classmethod
    async def noticer(cls, aid: Union[Adapter, str], player: Union[Player, str], mem: int, message: str, delay: float):
        if delay <= 0:
            return
        await asyncio.sleep(delay)
        await fapi.G.adapters[str(aid)].upload(
            CoreEntity(
                player=str(player),
                chain=chain.MessageChain.auto_make([At(target=int(mem)), Plain(text=message)] if int(player)!=int(mem) else message),
                source='',
                meta={}
            )
        )
    
    @classmethod
    async def deleter(cls, obj: "DDLNoticeRoutiner", delay: float):
        await asyncio.sleep(delay)
        obj.delete()

    @classmethod
    async def routine(cls, aid: Union[Adapter, str], subs: "DDLNoticeRoutiner"):
        ETA = subs.ddl.timestamp() - datetime.datetime.now().timestamp()
        cls.future_map[
            (str(aid), str(subs.player), subs.title) # 优化考虑化为前两个键做一个map，title做子map键
        ] = [
            asyncio.ensure_future(
                cls.noticer(
                    str(aid), 
                    subs.player, 
                    subs.mem,
                    f"{subs.title}还有约1天迎来ddl...",
                    ETA - 86400
                )
            ),
            asyncio.ensure_future(
                cls.noticer(
                    str(aid), 
                    subs.player, 
                    subs.mem,
                    f"{subs.title}将在1h后ddl...",
                    ETA - 3600
                )
            ),
            asyncio.ensure_future(
                cls.noticer(
                    str(aid), 
                    subs.player, 
                    subs.mem,
                    f"10分钟后，{subs.title}即会触碰万劫不复的ddl",
                    ETA - 600
                )
            ),
            asyncio.ensure_future(
                cls.noticer(
                    str(aid), 
                    subs.player, 
                    subs.mem,
                    f"{subs.title}已经终结。",
                    ETA - 0
                )
            )
        ]
        asyncio.ensure_future(cls.deleter(subs, ETA))
            


    @classmethod
    async def cancel(cls, aid: str, pid: str, meta: dict={}):
        q = cls.objects(adapter=Adapter.trychk(aid), player=Player.chk(pid))
        if q:
            q.delete()
            for i in cls.future_map[
                    (str(aid), str(pid), meta['title'])
                ]:
                i.cancel()
            return True
        else:
            return False

    @classmethod
    async def add(cls, aid: str, pid: str, meta: dict={}):
        if cls.objects(
            player=Player.chk(pid),
            adapter=Adapter.trychk(aid),
            title=meta['title']
        ):
            return False
        subs = cls(
            player=Player.chk(pid),
            adapter=Adapter.trychk(aid),
            ddl=datetime.datetime.fromtimestamp(float(meta['ts'])),
            title=meta['title'],
            mem=int(meta['mem'])
        ).save()
        await cls.routine(aid, subs)
        return True
