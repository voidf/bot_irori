from fapi.Sessions import SessionManager
from basicutils.task import *
from basicutils.media import *
from typing import Union
from loguru import logger

from mongoengine.fields import DateTimeField, IntField, ListField, StringField
from basicutils import chain
from basicutils import make_banner
from fapi.models.Base import *
from mongoengine import *
import aiohttp
import asyncio
import datetime
from basicutils.network import CoreEntity
from mongoengine import *
from fapi.models.Auth import *
from fapi.models.Player import *

routiner_namemap = {} # 根据名字查找Routiner用
retries = 20 # 比赛订阅爬虫超时重试次数

def imaseconds(cycle: float=86400, timezoneoffset: float=8*3600):
    """现在是东八区每天的第几秒"""
    return (datetime.datetime.now().timestamp() + timezoneoffset) % cycle

def sleep2ashita(offset: float):
    """算睡到明天第几秒所需要延迟的时间秒数"""
    return (86400 - imaseconds()) % 86400 + offset % 86400

def sleep2(timepoint: float=0, cycle: float=86400):
    return (cycle - imaseconds(cycle) + timepoint) % cycle

class Routiner(Base, Document):
    meta = {'allow_inheritance': True}
    # adapter = ReferenceField(Adapter)
    player = ReferenceField(Player)

    @classmethod
    async def recover_routiners(cls):
        """总恢复入口，不能被重载"""
        for sc in cls.__subclasses__():
            logger.info(f'{sc} is initializing...')
            await sc.resume()
            routiner_namemap[sc.__name__] = sc

    @classmethod
    async def resume(cls):
        """启动入口，可以放点静态的东西，最好得包括一个future_map"""
        raise NotImplementedError
    
    @classmethod
    async def cancel(cls, ent: CoreEntity):
        cls.objects(player=Player.chk(ent.pid)).delete()
    
    @classmethod
    async def add(cls, ent: CoreEntity):
        plr = Player.chk(ent.pid)
        if not cls.objects(player=plr):
            cls(
                player=plr
            ).save()

    # @classmethod
    # async def mainloop(cls, aid: str):
    #     raise NotImplementedError

# (现在的时间戳 + 8*3600) % 86400 才能获得东八区现在是一天的第几秒

class CodeforcesRoutiner(Routiner):
    # mode = StringField(default='Y')

    @staticmethod
    async def spider()-> list:
        ses: aiohttp.ClientSession
        retry_time = retries
        async with aiohttp.ClientSession() as ses:
            while retry_time:
                retry_time -= 1
                try:
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
                except:
                    logger.warning(make_banner('Error occured when fetching codeforces'))
                    logger.warning(traceback.format_exc())
            logger.critical(make_banner('Error occured when fetching codeforces, max retries exceed.', '!'))
            return []

    @classmethod
    async def notify(cls, contest: dict):
        ofs = 3600
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
                pid = str(subs.player)
                for s in SessionManager.get_routiner_list(pid):
                    await s.upload(
                        CoreEntity(
                            pid=pid,
                            chain=chain.MessageChain.auto_make(
                                f"比赛【{contest['name']}】还有不到1小时就要开始了...\n" + 
                                f"注册链接：https://codeforces.com/contestRegistration/{contest['id']}"
                            ),
                            source='',
                            meta={}
                        )
                    )
                    logger.critical('upload done')
        except:
            logger.error(traceback.format_exc())
    @classmethod
    async def update_futures(cls):
        li = await CodeforcesRoutiner.spider()
        mp =  cls.contest_futures
        for contest in li:
            if contest['id'] in mp:
                mp[contest['id']].cancel()
            mp[contest['id']] = asyncio.ensure_future(
                cls.notify(contest)
            )

    @classmethod
    async def resume(cls):
        cls.contest_futures = {}
        await cls.update_futures()
        asyncio.ensure_future(cls.mainloop())


    @classmethod
    async def mainloop(cls):
        while 1:
            await asyncio.sleep(sleep2(0))
            logger.debug('updating codeforces routiner...')
            await cls.update_futures()


import basicutils.CONST as C
from bs4 import BeautifulSoup
class AtcoderRoutiner(Routiner):
    @staticmethod
    async def spider() -> list:
        ses: aiohttp.ClientSession
        async with aiohttp.ClientSession() as ses:
            resp: aiohttp.ClientResponse
            retry_time = retries
            while retry_time:
                retry_time -= 1
                try:
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
                except:
                    logger.warning(make_banner('Error occured when fetching atcoder'))
                    logger.warning(traceback.format_exc())
            logger.critical(make_banner('Error occured when fetching atcoder, max retries exceed.', '!'))
            return []

    @classmethod
    async def notify(cls, contest: dict):
        contest['relativeTimeSeconds'] = abs(contest['relativeTimeSeconds'])
        if contest['relativeTimeSeconds'] < 3600:
            return
        await asyncio.sleep(contest['relativeTimeSeconds'] - 3600)
        q = cls.objects()
        
        try:
            for subs in q:
                pid = str(subs.player)
                for s in SessionManager.get_routiner_list(pid):
                    await s.upload(
                        CoreEntity(
                            pid=pid,
                            chain=chain.MessageChain.auto_make(
                                f"比赛【{contest['name']}】还有不到1小时就要开始了...\n" + 
                                f"注册链接：https://atcoder.jp{contest['id']}"
                            ),
                            source='',
                            meta={}
                        )
                    )
        except:
            logger.error(traceback.format_exc())

    @classmethod
    async def update_futures(cls):
        li = await AtcoderRoutiner.spider()
        mp = cls.contest_futures
        for contest in li:
            if contest['id'] in mp:
                mp[contest['id']].cancel()
            mp[contest['id']] = asyncio.ensure_future(
                cls.notify(contest)
            )

    @classmethod
    async def resume(cls):
        cls.contest_futures = {}
        await cls.update_futures()
        asyncio.ensure_future(cls.mainloop())


    @classmethod
    async def mainloop(cls):
        while 1:
            await asyncio.sleep(sleep2(0))
            logger.debug('updating atcoder routiner...')
            await cls.update_futures()


import random
import basicutils.CONST as CONST
from Worker import import_applications
class CreditInfoRoutiner(Routiner):
    @classmethod
    async def info(cls, ent: CoreEntity):
        return ','.join(list(cls.credit_cmds.keys()))
    @classmethod
    async def resume(cls):
        logger.debug(f'{cls} resume called')
        # cls.future_map = {}
        # if not fapi.G.initialized:
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
        while 1:
            await asyncio.sleep(sleep2(0))
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
            for s in SessionManager.get_routiner_list(str(subs.player)):
                await s.upload(
                    CoreEntity(
                        pid=str(subs.player),
                        chain=chain.MessageChain.auto_make(
                            f'今天使用{await cls.info()}这些命令会有惊喜哦（'
                        ),
                        source='',
                        meta={}
                    )
                )


from basicutils.chain import *
class DDLNoticeRoutiner(Routiner):
    ddl = DateTimeField()
    title = StringField()
    mem = IntField()
    @classmethod
    async def info(cls, ent: CoreEntity):
        li = []
        for subs in cls.objects(player=Player.chk(ent.pid)):
            li.append(f"{str(subs.ddl)}    {subs.title}")
        return '\n'.join(li)
    @classmethod
    async def resume(cls):
        logger.debug(f'{cls} resume called')
        cls.call_map = {
            'info': cls.info
        }
        cls.future_map = {}
        for subs in cls.objects():
            await cls.routine(subs)
        # asyncio.ensure_future(cls.mainloop())
        logger.info(f'{cls} initialized')


    @classmethod
    async def noticer(cls, player: Union[Player, str], mem: int, message: str, delay: float):
        if delay <= 0:
            return
        pid = str(player)
        logger.debug('delay for {}', delay)
        await asyncio.sleep(delay)
        for s in SessionManager.get_routiner_list(pid):
            await s.upload(
                CoreEntity(
                    pid=pid,
                    chain=chain.MessageChain.auto_make([At(target=int(mem)), Plain(text=message)] if int(pid)!=mem else message),
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
        nkey = (str(subs.player), subs.title) # 优化考虑化为前两个键做一个map，title做子map键
        cls.future_map[
            nkey
        ] = [
            asyncio.ensure_future(
                cls.noticer(
                    subs.player, 
                    subs.mem,
                    f"{subs.title}还有约1天迎来ddl...",
                    ETA - 86400
                )
            ),
            asyncio.ensure_future(
                cls.noticer(
                    subs.player, 
                    subs.mem,
                    f"{subs.title}将在1h后ddl...",
                    ETA - 3600
                )
            ),
            asyncio.ensure_future(
                cls.noticer(
                    subs.player, 
                    subs.mem,
                    f"10分钟后，{subs.title}有ddl",
                    ETA - 600
                )
            ),
            asyncio.ensure_future(
                cls.noticer(
                    subs.player, 
                    subs.mem,
                    f"{subs.title}寄了。",
                    ETA - 0
                )
            )
        ]
        asyncio.ensure_future(cls.deleter(subs, ETA, nkey))
        logger.debug(cls.future_map)
            


    @classmethod
    async def cancel(cls, ent: CoreEntity):
        q = cls.objects(player=Player.chk(ent.pid), title=ent.meta['title'])
        if q:
            q.delete()
            for i in cls.future_map[
                    (str(ent.pid), ent.meta['title'])
                ]:
                logger.warning(i.cancel())
            logger.warning(cls.future_map)
            cls.future_map.pop((str(ent.pid), ent.meta['title']))
            return True
        else:
            logger.debug('No such routine')
            return False

    @classmethod
    async def add(cls, ent: CoreEntity):
        if cls.objects(
            player=Player.chk(ent.pid),
            title=ent.meta['title']
        ):
            return False
        subs = cls(
            player=Player.chk(ent.pid),
            ddl=datetime.datetime.fromtimestamp(float(ent.meta['ts'])),
            title=ent.meta['title'],
            mem=int(ent.member)
        ).save()
        await cls.routine(subs)
        return True

from bs4 import BeautifulSoup
import traceback
class WeatherReportRoutiner(Routiner):
    city = ListField(StringField())
    @classmethod
    async def resume(cls):
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
        asyncio.ensure_future(cls.mainloop())
        logger.info(f'{cls} initialized')


    @classmethod
    async def mainloop(cls):
        ses = aiohttp.ClientSession()
        while 1:
            await asyncio.sleep(sleep2(5))
            await cls.update_futures(ses)

    @classmethod
    async def update_futures(cls, ses: aiohttp.ClientSession):
        q = cls.objects()
        # if q:s
        dt = datetime.datetime.now()
        ans = [f'今天是{dt.year}年{dt.month}月{dt.day}日，{cls.youbi[dt.isoweekday()]}']
        try:
            async with ses.get('https://wannianrili.51240.com/', timeout=30) as resp:
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
            pid = str(subs.player)

            for city in subs.city:
                try:
                    async with ses.get('http://toy1.weather.com.cn/search?cityname=' + city, timeout=30) as resp:
                        j = json.loads((await resp.text())[1:-1])[0]['ref'].split('~')

                    output.append(f'{j[2]}的天气数据:')
                    async with ses.get(f'http://www.weather.com.cn/weather/{j[0]}.shtml', timeout=30) as resp:
                        b = BeautifulSoup(await resp.content.read(), 'html.parser')
                except:
                    logger.critical(traceback.format_exc())
                    output.append('网络连接错误，请检查日志')
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
            for s in SessionManager.get_routiner_list(pid):
                s.upload(
                    CoreEntity(
                        pid=pid,
                        chain=chain.MessageChain.auto_make(
                            '\n'.join(output)
                        ),
                        source='',
                        meta={}
                    )
                )


    @classmethod
    async def add(cls, ent: CoreEntity):
        c = cls.objects(
            player=Player.chk(ent.pid)
        ).first()
        if not c:
            c = cls(
            player=Player.chk(ent.pid),
            city=[]
        )
        if ent.meta['city'] not in c.city:
            c.city.append(ent.meta['city'])
            c.save()

class DailySentenceRoutiner(Routiner):
    @classmethod
    async def resume(cls):
        logger.debug(f'{cls} resume called')
        asyncio.ensure_future(cls.mainloop())
        logger.info(f'{cls} initialized')

    @classmethod
    async def update_futures(cls, ses: aiohttp.ClientSession):
        try:
            async with ses.get(
                f'http://sentence.iciba.com/index.php?c=dailysentence&m=getTodaySentence&_={int(datetime.datetime.now().timestamp()*1000)}',
                timeout=30
            ) as resp:
                j = await resp.json()
            # amr = server_api('/worker/oss/' + (await to_amr('mp3', lnk=j['tts']))['url'])
            amr = j['tts']
            ent = CoreEntity(
                pid='',
                chain=MessageChain.auto_make(
                    [Plain(j['content']+'\n'+j['note']), Image(url=j['picture']), Voice(url=amr)]
                ),
                source='',
                meta={}
            )
            for subs in cls.objects():
                pid = str(subs.player)
                ent.pid = pid
                for s in SessionManager.get_routiner_list(pid):
                    await s.upload(
                        ent
                    )
        except:
            logger.critical(traceback.format_exc())
            ent = CoreEntity(
                pid='',
                chain=MessageChain.auto_make(
                    [Plain('【每日一句】网络连接错误，请检查日志')]
                ),
                source='',
                meta={}
            )
            for subs in cls.objects():
                pid = str(subs.player)
                ent.pid = pid
                for s in SessionManager.get_routiner_list(pid):
                    await s.upload(
                        ent
                    )


    @classmethod
    async def mainloop(cls):
        ses = aiohttp.ClientSession()
        while 1:
            await asyncio.sleep(sleep2(3600*17))
            await cls.update_futures(ses)


class LoginNoticeRoutiner(Routiner):
    login_msg = StringField(default='Routiner testcase')
    @classmethod
    async def resume(cls):
        logger.debug(f'{cls} resume called')
        cls.chk('550455545448')
        cls.chk('2595247078')
        asyncio.ensure_future(cls.mainloop())
        logger.info(f'{cls} initialized')


    @classmethod
    async def mainloop(cls):
        await asyncio.sleep(60)
        for subs in cls.objects():
            pid = str(subs.player)
            ent = CoreEntity(
                pid=pid,
                chain=MessageChain.auto_make(
                    subs.login_msg
                ),
                source='',
                meta={}
            )
            for s in SessionManager.get_routiner_list(pid):
                await s.upload(
                    ent
                )

