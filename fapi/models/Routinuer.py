from mongoengine.errors import DoesNotExist
from basicutils.task import *
from basicutils.media import *
from time import sleep
from typing import Union
from loguru import logger

from mongoengine.fields import DateTimeField, IntField, ListField, StringField
from basicutils import chain
import fapi.G

from fapi.models.Base import *
from mongoengine import *
import aiohttp
import asyncio
import datetime
from basicutils.network import CoreEntity
from mongoengine import *
from fapi.models.Auth import *
from fapi.models.Player import *

routiner_namemap = {} # 根据名字查找Routinuer用

class Routiner(Base, Document):
    meta = {'allow_inheritance': True}
    # adapter = ReferenceField(Adapter)
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
    async def cancel(cls, ent: CoreEntity):
        """取消订阅接口"""
        raise NotImplementedError
    
    @classmethod
    async def add(cls, ent: CoreEntity):
        """添加订阅接口"""
        raise NotImplementedError

    # @classmethod
    # async def mainloop(cls, aid: str):
    #     raise NotImplementedError

# (现在的时间戳 + 8*3600) % 86400 才能获得东八区现在是一天的第几秒

class CodeforcesRoutinuer(Routiner):
    # mode = StringField(default='Y')

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
        ofs = 900
        contest['relativeTimeSeconds'] = abs(contest['relativeTimeSeconds'])
        logger.critical('{}在{}s后开始', contest['name'], contest['relativeTimeSeconds'] - ofs)
        if contest['relativeTimeSeconds'] < ofs:
            logger.critical('returned')
            return
        await asyncio.sleep(contest['relativeTimeSeconds'] - ofs)
        q = cls.objects()
        # if q:
        logger.critical(q)
        try:
            for subs in q:
                try:
                    # logger.critical('通知{}中...', subs.get_base_info())
                    logger.critical(fapi.G.adapters)
                    # plr = Player.chk(subs.player)
                    logger.critical(str(subs.player.aid))
                    logger.critical(str(subs.player.aid) in fapi.G.adapters)
                    # logger.critical('\n')
                except DoesNotExist:
                    subs.delete()
                    logger.critical('delete illegal file {}', subs.pk)
                except:
                    logger.error(traceback.format_exc())
                    if str(subs.player.aid) in fapi.G.adapters:

                        await fapi.G.adapters[str(subs.player.aid)].upload(
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
                        logger.critical(subs.player.get_base_info())
        except:
            logger.error(traceback.format_exc())
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
    async def cancel(cls, ent: CoreEntity):
        cls.objects(player=Player.chk(ent.player, ent.source)).delete()

    @classmethod
    async def add(cls, ent: CoreEntity):
        cls(
            player=Player.chk(ent.player, ent.source)
        ).save()

import basicutils.CONST as C
from bs4 import BeautifulSoup
class AtcoderRoutinuer(Routiner):
    # mode = StringField(default='Y')

    @staticmethod
    async def spider():
        ses: aiohttp.ClientSession
        async with aiohttp.ClientSession() as ses:
            resp: aiohttp.ClientResponse
            li = []
            async with ses.get(
                'https://atcoder.jp/contests/',
                headers=C.AtCoderHeaders,
                timeout=30
            ) as resp:
                s = BeautifulSoup(await resp.text(), 'html.parser')
                try:
                    for p, i in enumerate(s.find('h3', string='Active Contests').next_sibling.next_sibling('tr')):
                        if p:
                            begintime = datetime.datetime.strptime(i('a')[0].text, "%Y-%m-%d %H:%M:%S+0900") - datetime.timedelta(hours=1)
                            li.append({
                                'id': i('a')[1]['href'],
                                'name': i('a')[1].text,
                                'relativeTimeSeconds': (datetime.datetime.now() - begintime).total_seconds()
                            })
                except:
                    pass
                for p, i in enumerate(s.find('h3', string='Upcoming Contests').next_sibling.next_sibling('tr')):
                    if p:
                        begintime = datetime.datetime.strptime(i('a')[0].text, "%Y-%m-%d %H:%M:%S+0900") - datetime.timedelta(hours=1)
                        li.append({
                            'id': i('a')[1]['href'],
                            'name': i('a')[1].text,
                            'relativeTimeSeconds': (datetime.datetime.now() - begintime).total_seconds()
                        })
                # for i in j:
                #     if i['phase'] == 'FINISHED':
                #         break
                #     li.append(i)
                #     """
                #     可用属性：
                #     id                  比赛id
                #     name                比赛名
                #     relativeTimeSeconds 为负数时表示还差多少秒开始
                #     """
                    
        return li

    @classmethod
    async def notify(cls, contest: dict):
        # if isinstance(player, Player):
        #     player = str(player.pid)
        contest['relativeTimeSeconds'] = abs(contest['relativeTimeSeconds'])
        if contest['relativeTimeSeconds'] < 3600:
            return
        await asyncio.sleep(contest['relativeTimeSeconds'] - 3600)
        q = cls.objects()
        # if q:
        for subs in q:
            if str(subs.player.aid) in fapi.G.adapters:
                await fapi.G.adapters[str(subs.player.aid)].upload(
                    CoreEntity(
                        player=str(subs.player),
                        chain=chain.MessageChain.auto_make(
                            f"比赛【{contest['name']}】还有不到1小时就要开始了...\n" + 
                            f"注册链接：https://atcoder.jp{contest['id']}"
                        ),
                        source='',
                        meta={}
                    )
                )

    @classmethod
    async def update_futures(cls):
        # q = cls.objects(adapter=Adapter.trychk(aid))
        # if q:
        li = await AtcoderRoutinuer.spider()
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
    async def cancel(cls, ent: CoreEntity):
        cls.objects(player=Player.chk(ent.player, ent.source)).delete()

    @classmethod
    async def add(cls, ent: CoreEntity):
        cls(
            player=Player.chk(ent.player, ent.source)
        ).save()

import random
import basicutils.CONST as CONST
from Worker import import_applications
class CreditInfoRoutinuer(Routiner):
    @classmethod
    async def info(cls, ent: CoreEntity):
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
            await fapi.G.adapters[str(subs.player.aid)].upload(
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
    async def cancel(cls, ent: CoreEntity):
        cls.objects(player=Player.chk(ent.player, ent.source)).delete()

    @classmethod
    async def add(cls, ent: CoreEntity):
        cls(
            player=Player.chk(ent.player, ent.source),
        ).save()


from basicutils.chain import *
class DDLNoticeRoutiner(Routiner):
    ddl = DateTimeField()
    title = StringField()
    mem = IntField()
    @classmethod
    async def info(cls, ent: CoreEntity):
        li = []
        for subs in cls.objects(player=Player.chk(ent.player, ent.source)):
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
        for subs in cls.objects():
            await cls.routine(aid, subs)
        # asyncio.ensure_future(cls.mainloop())
        logger.info(f'{cls} initialized')


    @classmethod
    async def noticer(cls, aid: Union[Adapter, str], player: Union[Player, str], mem: int, message: str, delay: float):
        if delay <= 0:
            return
        logger.debug('delay for {}', delay)
        await asyncio.sleep(delay)
        await fapi.G.adapters[str(aid)].upload(
            CoreEntity(
                player=str(player),
                chain=chain.MessageChain.auto_make([At(target=int(mem)), Plain(text=message)] if player.pid!=mem else message),
                source='',
                meta={}
            )
        )
    
    @classmethod
    async def deleter(cls, obj: "DDLNoticeRoutiner", delay: float, nkey: tuple):
        await asyncio.sleep(delay)
        logger.debug('{} 已完成',cls.future_map.pop(nkey))
        obj.delete()

    @classmethod
    async def routine(cls, subs: "DDLNoticeRoutiner"):
        ETA = subs.ddl.timestamp() - datetime.datetime.now().timestamp()
        aid = subs.player.aid
        nkey = (str(aid), str(subs.player), subs.title) # 优化考虑化为前两个键做一个map，title做子map键
        cls.future_map[
            nkey
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
        asyncio.ensure_future(cls.deleter(subs, ETA, nkey))
        logger.debug(cls.future_map)
            


    @classmethod
    async def cancel(cls, ent: CoreEntity):
        q = cls.objects(player=Player.chk(ent.player, ent.source))
        if q:
            q.delete()
            for i in cls.future_map[
                    (str(ent.source), str(ent.player), ent.meta['title'])
                ]:
                logger.warning(i.cancel())
            logger.warning(cls.future_map)
            return True
        else:
            logger.debug('No such routine')
            return False

    @classmethod
    async def add(cls, ent: CoreEntity):
        if cls.objects(
            player=Player.chk(ent.player, ent.source),
            # adapter=Adapter.trychk(ent.source),
            title=ent.meta['title']
        ):
            return False
        subs = cls(
            player=Player.chk(ent.player, ent.source),
            # adapter=Adapter.trychk(ent.source),
            ddl=datetime.datetime.fromtimestamp(float(ent.meta['ts'])),
            title=ent.meta['title'],
            mem=int(ent.member)
        ).save()
        await cls.routine(subs)
        return True

from bs4 import BeautifulSoup
import traceback
class WeatherReportRoutinuer(Routiner):
    city = ListField(StringField())
    @classmethod
    async def resume(cls, aid: str):
        cls.youbi = {
            1:'月曜日',
            2:'火曜日',
            3:'水曜日',
            4:'木曜日',
            5:'金曜日',
            6:'土曜日',
            7:'日曜日',
        }

        logger.debug(f'{cls} resume called')
        # cls.future_map = {}
        if not fapi.G.initialized:
            asyncio.ensure_future(cls.mainloop())
            logger.info(f'{cls} initialized')


    @classmethod
    async def mainloop(cls):
        cycle = 86400
        offset = 3600 * 8 - 5 # 0点过5秒
        ses = aiohttp.ClientSession()
        while 1:
            tosleep = cycle - (datetime.datetime.now().timestamp() + offset) % cycle
            await asyncio.sleep(tosleep)
            await cls.update_futures(ses)

    @classmethod
    async def update_futures(cls, ses: aiohttp.ClientSession):
        q = cls.objects()
        # if q:s
        dt = datetime.datetime.now()
        ans = [f'今天是{dt.year}年{dt.month}月{dt.day}日，{cls.youbi[dt.isoweekday()]}']
        try:
            async with ses.get('https://wannianrili.51240.com/') as resp:
                bs = BeautifulSoup(await resp.text(), 'html.parser')
            res = bs('div',attrs={'id':'jie_guo'})
            ans.append('农历'+res[0].contents[0].contents[dt.day]('div',attrs={'class':"wnrl_k_you_id_wnrl_nongli"})[0].string)
            ans.append(res[0].contents[dt.day]('span',string='节气')[0].nextSibling.string)
        except:
            ans.append('我忘了今天农历几号了')
            print(traceback.format_exc())

        if random.randint(0,3):
            ans.append(random.choice(['还在盯着屏幕吗？','还不睡？等死吧','别摸了别摸了快点上床吧','白天再说.jpg','邀请你同床竞技']))

        done = set()

        for subs in q:
            output = list(ans)

            # output = [] if subs.player.pk in done else list(ans)
            # done.add(subs.player.pk)
            for city in subs.city:
                async with ses.get('http://toy1.weather.com.cn/search?cityname=' + city) as resp:
                    j = json.loads((await resp.text())[1:-1])[0]['ref'].split('~')



                output.append(f'{j[2]}的天气数据:')
                async with ses.get(f'http://www.weather.com.cn/weather/{j[0]}.shtml') as resp:
                    b = BeautifulSoup(await resp.content.read(), 'html.parser')
                ctr = 0
                pos = 10
                for p, i in enumerate(b('li')):
                    if i.text.find('今天') != -1:
                        ctr += 1
                        if ctr >= 2:
                            pos = p
                            break
                for i in b('li')[pos:pos+7]:
                    t = i('p')
                    output.append(
                        f'{i.h1.text} {t[0].text} {t[1].text.strip()} {t[2].span["title"]}{t[2].text.strip()}')
            await fapi.G.adapters[str(subs.player.aid)].upload(
                CoreEntity(
                    player=str(subs.player),
                    chain=chain.MessageChain.auto_make(
                        '\n'.join(output)
                    ),
                    source='',
                    meta={}
                )
            )

    @classmethod
    async def cancel(cls, ent: CoreEntity):
        cls.objects(player=Player.chk(ent.player, ent.source)).delete()

    @classmethod
    async def add(cls, ent: CoreEntity):
        c = cls.objects(
            player=Player.chk(ent.player, ent.source)
        ).first()
        if not c:
            c = cls(
            player=Player.chk(ent.player, ent.source),
            city=[]
        )
        c.city.append(ent.meta['city'])
        c.save()

class DailySentenceRoutinuer(Routiner):
    @classmethod
    async def resume(cls, aid: str):
        logger.debug(f'{cls} resume called')
        # cls.future_map = {}
        if not fapi.G.initialized:
            asyncio.ensure_future(cls.mainloop())
            logger.info(f'{cls} initialized')

    @classmethod
    async def update_futures(cls, ses: aiohttp.ClientSession):
        async with ses.get(
            f'http://sentence.iciba.com/index.php?c=dailysentence&m=getTodaySentence&_={int(datetime.datetime.now().timestamp()*1000)}'
        ) as resp:
            j = await resp.json()
        # amr = server_api('/worker/oss/' + (await to_amr('mp3', lnk=j['tts']))['url'])
        amr = j['tts']
        ent = CoreEntity(
            player='',
            chain=MessageChain.auto_make(
                [Plain(j['content']+'\n'+j['note']), Image(url=j['picture']), Voice(url=amr)]
            ),
            source='',
            meta={}
        )
        for subs in cls.objects():
            ent.player=str(subs.player)
            await fapi.G.adapters[str(subs.player.aid)].upload(
                ent
            )


    @classmethod
    async def mainloop(cls):
        cycle = 86400
        offset = 3600 * 17 # 0点过5秒
        ses = aiohttp.ClientSession()
        while 1:
            tosleep = cycle - (datetime.datetime.now().timestamp() + 8*3600 - offset) % cycle
            await asyncio.sleep(tosleep)
            await cls.update_futures(ses)

    

    @classmethod
    async def cancel(cls, ent: CoreEntity):
        cls.objects(player=Player.chk(ent.player, ent.source)).delete()

    @classmethod
    async def add(cls, ent: CoreEntity):
        c = cls.objects(
            player=Player.chk(ent.player, ent.source)
        ).first()
        if not c:
            c = cls(
            player=Player.chk(ent.player, ent.source)
        )
        c.save()
