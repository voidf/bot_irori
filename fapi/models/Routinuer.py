from time import sleep
from loguru import logger

from mido.messages.messages import Message
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
    async def cancel(cls, aid: str, pid: str):
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
    async def cancel(cls, aid: str, pid: str):
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
    async def cancel(cls, aid: str, pid: str):
        cls.objects(adapter=Adapter.trychk(aid), player=Player.chk(pid)).delete()

    @classmethod
    async def add(cls, aid: str, pid: str, meta: dict={}):
        cls(
            player=Player.chk(pid),
            adapter=Adapter.trychk(aid)
        ).save()

# class DDLNoticeRoutiner(Routiner):
