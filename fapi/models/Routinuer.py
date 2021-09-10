from time import sleep

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
class Routiner(RefPlayerBase, Document):
    meta = {'allow_inheritance': True}
    adapterid = StringField()
    # cycle = FloatField()
    # offset = FloatField()

    @classmethod
    async def recover_routiners(cls, aid: str, ses: aiohttp.ClientSession):
        """总恢复入口，不能被重载"""
        for sc in cls.__subclasses__():
            asyncio.ensure_future(sc.resume(aid, ses))

    @classmethod
    async def resume(cls, aid: str, ses: aiohttp.ClientSession):
        """启动入口，可以放点静态的东西，最好得包括一个future_map"""
        raise NotImplementedError
    
    @classmethod
    async def cancel(cls, aid: str):
        """取消订阅接口"""
        raise NotImplementedError
    
    # @classmethod
    # async def mainloop(cls, aid: str, ses: aiohttp.ClientSession):
    #     raise NotImplementedError

class CodeforcesRoutinuer(Routiner):
    mode = StringField(default='Y')

    @staticmethod
    async def spider(ses: aiohttp.ClientSession):
        resp: aiohttp.ClientResponse
        li = []
        async with ses.get('https://codeforces.com/api/contest.list', timeout=30) as resp:
            resp.json()
            j = await resp.json()['result']
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

    @staticmethod
    async def notify(aid: str, player: int, contest: dict):
        if contest['countdown'] < 3600:
            return
        await asyncio.sleep(contest['countdown'] - 3600)
        await fapi.G.adapters[aid].upload(
            CoreEntity(
                player=str(player),
                chain=chain.MessageChain.auto_make(
                    f"比赛【{contest['name']}】还有不到1小时就要开始了...\n" + 
                    f"注册链接：https://codeforces.com/contestRegistration/{contest['id']}"
                ),
                source='',
                meta={}
            )
        )

    @classmethod
    async def update_futures(cls, aid: str, ses: aiohttp.ClientSession):
        li = CodeforcesRoutinuer.spider(ses)
        for subscribers in q:
            mp = cls.future_map.setdefault(aid, {})
            for contest in li:
                if contest['id'] in mp:
                    mp[contest['id']].cancel()
                mp[contest['id']] = asyncio.ensure_future(
                    CodeforcesRoutinuer.notify(aid, subscribers.player, contest)
                )
    
    @classmethod
    async def resume(cls, aid: str, ses: aiohttp.ClientSession):
        cls.future_map = {}
        q = cls.objects(adapterid=aid)
        if q:
            await cls.update_futures(aid, ses)
        await cls.mainloop(aid, ses)


    @classmethod
    async def mainloop(cls, aid: str, ses: aiohttp.ClientSession):
        cycle = 86400
        offset = 3600 * 8 # UTC+8, 24 - 8 = 16
        while 1:
            tosleep = cycle - (datetime.datetime.now() + offset) % cycle
            await asyncio.sleep(tosleep)
            await cls.update_futures(aid, ses)

        
