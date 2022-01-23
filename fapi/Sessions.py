import asyncio
import traceback
import aiohttp
from loguru import logger
from basicutils.network import *
from basicutils.chain import *
from fapi import *

from fapi.models.FileStorage import *
# def search_player(pid, aid):
#     return Player.chk(pid, aid)
# import ctypes
from abc import ABC

class Session(ABC):
    """收发消息的实体"""
    def __init__(self) -> None:
        self._ases = aiohttp.ClientSession()
        self._alive = True
    def _init_sid(self, sid):
        self.sid = sid
    # def _lateinit(self, *args):
        # pass
    @abstractmethod
    async def enter_loop(self, *args):
        pass
    async def close(self):
        await self._ases.close()
    @abstractmethod    
    async def upload(self, ent: CoreEntity):
        pass

class SessionManager():
    s = {}      # 活动Session表
    # a2p = {}    # adapter: {session: [(player, playername)]}表 内部通信用
    p2s = {}    # player: [session]表 日程器用

    
    @staticmethod
    def get(k: int) -> Session: # 顶多抛异常
        return SessionManager.s[k]

    @staticmethod
    async def autoupload(ent: CoreEntity):
        """根据ent.source选择session进行上传"""
        await SessionManager.s[ent.source].upload(ent)

    # @staticmethod
    # def get(k: int): # 不安全，可能段错误而直接被OS杀死
        # return ctypes.cast(k, ctypes.py_object).value

    # @staticmethod
    # def hangout_adapter(aid: str):
    #     """清理所有属于给定adapter的会话"""
    #     for ses, (pid, pname) in SessionManager.a2p.get(aid, {}).items():
    #         asyncio.ensure_future(ses.close())
    #         SessionManager
    
    @staticmethod
    def new(sestyp, *args):
        """算是个工厂？sestyp提供需要造的Session是哪种，args为传入enter_loop的参数，返回Session的id"""
        ses: Session = sestyp()
        sid = id(ses)
        SessionManager.s[sid] = ses
        ses._init_sid(sid)
        # ses._lateinit(*args)
        asyncio.ensure_future(ses.enter_loop(*args))
        return sid

    @staticmethod
    def close(k: int):
        """关掉一个会话"""
        try:
            asyncio.ensure_future(SessionManager.s.pop(k).close())
            # for _, v in SessionManager.a2p.items():
                # v.pop(k)
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
    def get_routiner_list(pid: str):
        return SessionManager.p2s.get(pid, [])
