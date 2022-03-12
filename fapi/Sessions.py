import asyncio
import traceback
import aiohttp
from loguru import logger
from basicutils.network import *
from basicutils.chain import *
from fapi import *
from basicutils.task import server_api
from fapi.models.FileStorage import *
# def search_player(pid, aid):
#     return Player.chk(pid, aid)
# import ctypes
from fapi.utils.media import to_amr
from abc import ABC, abstractmethod
import markdown
from fapi.utils.syscall import *

class Session(ABC):
    """收发消息的实体，表示一个Irori能向外输出的会话接口"""
    def __init__(self) -> None:
        self._alive = True
    def _init_sid(self, sid):
        self.sid = sid
    # def _lateinit(self, *args):
        # pass
    def alive(self) -> bool:
        return self._alive

    async def close(self):
        if self._alive:
            await self._ases.close()
        self._alive = False

    @abstractmethod
    async def enter_loop(self, *args) -> Iterable[str]:
        """进入接收回环，子类应该提供其能访问的所有player号"""
        raise NotImplementedError

    async def _preprocess(self, ent: CoreEntity) -> List[str]:
        """预处理解析双减号参数，返回其余文本串的空格分片"""
        retato = []
        for elem in ent.chain:
            if isinstance(elem, Plain):
                data = elem.tostr()
                att = data.split(' ') 

                # --手写参数解析
                ato = []
                for i in att:
                    if i[:2] == "--":
                        arg,*val = i[2:].split("=")
                        ent.meta["-"+arg] = "".join(val)
                    else: ato.append(i)
                elem.text = ' '.join(ato)
                retato.extend(ato)
        return retato

    async def _handle_syscall(self, ent: CoreEntity):
        ato = await self._preprocess(ent)
        if len(ato)>=2 and ato[0] == 'sudo' and ent.member in IroriConfig.get().auth_masters:
            # TODO: 迁移python3.10 改match语法
            try:
                ret = await {
                    'eval': sys_eval,
                    'exec': sys_exec,
                    'run': sys_run,
                }.get(ato[1], sys_help)(ent, ato[2:])
                ent.chain = MessageChain.auto_make(ret)
            except:
                ent.chain = MessageChain.auto_make(traceback.format_exc())
            await self._deliver(ent)
            return True
        return False

    
    @abstractmethod
    async def _deliver(self, ent: CoreEntity) -> None:
        """消息发送，Session子类应该会自己根据ent.pid选择发送方式"""
        raise NotImplementedError

    async def _package(self, ent: CoreEntity) -> None:
        """消息装箱，处理markdown转换"""
        output = []
        if '-md' in ent.meta:
            for i in ent.chain:
                if isinstance(i, Image):
                    if i.url:
                        output.append(f'![]({i.url})')
                    elif i.base64:
                        if i.base64[:3] == 'iVB':
                            output.append(f'![](data:image/png;base64,{i.base64})')
                        else:
                            output.append(f'![](data:image/jpeg;base64,{i.base64})')
                elif isinstance(i, Voice):
                    output.append(f'<p><audio src="{i.url}""></p>')
                else:
                    output.append(f'{i.tostr()}')
            html = markdown.markdown(''.join(output).replace('\n', '<br>'))
            t = TempFile(
                filename='TempHtmlFile.htm',
                content_type='text/html',
                expires=datetime.datetime.now()+datetime.timedelta(seconds=3600)
            )
            t.content.put(BytesIO(bytes(html, 'utf-8')))
            t.save()
            asyncio.ensure_future(t.deleter())
            ent.chain.__root__ = [Plain(server_api(f'/worker/oss/{t.pk!s}'))]
        elif '-tts' in ent.meta:
            from basicutils.media import BaiduTTS
            ent.chain.__root__ = [Voice(
                url=server_api('/worker/oss/' + 
                (await to_amr(lnk=BaiduTTS(ent.chain.tostr())))['url'])
            )]
        await self._deliver(ent)

    async def upload(self, ent: CoreEntity):
        """发送消息链，处理meta delay分片"""

        logger.debug('upload triggered')
        try:
            chain = ent.chain
            logger.debug(chain)
            ent.chain = MessageChain.get_empty()
            for i in chain:
                if i.meta and 'delay' in i.meta:
                    if ent.chain.__root__:
                        await self._package(ent)
                    await asyncio.sleep(float(i.meta['delay']))
                    ent.chain.__root__.clear()
                elif isinstance(i, Voice):
                    i = Voice(url=server_api('/worker/oss/' + (await to_amr(
                        ent.meta.get('-vmode', 0),
                        lnk=i.url if i.url else '',
                        b64=i.base64 if i.base64 else ''
                    ))['url']))
                    if ent.chain.__root__:
                        await self._package(ent)
                    ent.chain.__root__.clear()
                ent.chain.__root__.append(i)
            if ent.chain.__root__:
                await self._package(ent)
        except ValueError:
            return "not mirai"


class SessionManager():
    """用来管理活动Session的静态函数包，别实例化"""
    s = {}      # 活动Session表
    # a2p = {}    # adapter: {session: [(player, playername)]}表 内部通信用
    p2s = {}    # player: [session号]表 日程器用

    
    @staticmethod
    def get(k: int) -> Union[None, Session]: # 顶多抛异常
        """根据session号找session，不存在或者寄了就是None"""
        ses = SessionManager.s.get(k, None)
        if ses and ses.alive():
            return ses
        SessionManager.s.pop(k)
        return None

    @staticmethod
    async def autoupload(ent: CoreEntity):
        """根据ent.source选择session进行上传"""
        await SessionManager.s[ent.source].upload(ent)

    # @staticmethod
    # def get(k: int): # 不安全，可能段错误而直接被OS杀死
        # return ctypes.cast(k, ctypes.py_object).value

    @staticmethod
    async def new(sestyp, *args):
        """算是个工厂？sestyp提供需要造的Session是哪种，args为传入enter_loop的参数，返回Session的id"""
        ses: Session = sestyp()
        sid = id(ses)
        SessionManager.s[sid] = ses
        ses._init_sid(sid)
        # ses._lateinit(*args)
        for plr in (await ses.enter_loop(*args)):
            SessionManager.p2s.setdefault(plr, []).append(sid)
        return sid

    @staticmethod
    async def hangon(k: int):
        s = SessionManager.get(k)
        if s:
            return await s.receiver
        return

    @staticmethod
    def close(k: int):
        """关掉一个会话"""
        try:
            asyncio.ensure_future(SessionManager.s.pop(k).close())
            for _, v in SessionManager.p2s.items():
                try:
                    v.remove(k)
                except ValueError:
                    pass
            return True
        except:
            logger.error(traceback.format_exc())
            return False
    # @staticmethod
    # def get_contactable_list(aid: str):
        # return [(sid, pid, pname) for sid, (pid, pname) in SessionManager.a2p.get(aid, {}).items()]
    @staticmethod
    def get_routiner_list(pid: str) -> List[Session]:
        """返回可以联系到给定的pid标识的player的Session表
        
        调用时懒惰更新存活表"""
        a = []
        sessions: List[Session] = []
        for i in SessionManager.p2s.get(pid, []):
            s = SessionManager.get(i)
            if s:
                a.append(i)
                sessions.append(s)
        SessionManager.p2s[pid] = a
        return sessions
