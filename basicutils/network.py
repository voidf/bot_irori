from io import BytesIO

from pydantic import BaseModel # 为了用json
from pydantic import Field
from typing import *
import datetime
import json
from basicutils.chain import *

# Core内部传输用
class CoreEntity(BaseModel):
    """irori系统内部的消息传输形式"""
    chain: MessageChain
    # player: str  = '' # 发送来源player ObjectId
    pid: str  = ''    # 发送来源player id
    source: str  = '' # 发送来源Sessionid或是相关jwt
    meta: dict   = {} # 额外参数，对worker会使用ts时间戳来维护忙状态，解析的--参数也会放在这里
    jwt: str     = '' # 令牌
    member: str  = '' # 实际发送者的player号
    @classmethod
    def handle_json(cls, j):
        d = json.loads(j)
        d['chain'] = MessageChain.auto_make(d['chain'])
        return cls(**d)
    @classmethod
    def wrap_rawstring(cls, msg: str):
        mt = {'msg': msg}
        return cls(
            chain=MessageChain.get_empty(),
            meta=mt
        )
    @classmethod
    def wrap_strchain(cls, msg: str):
        return cls(
            chain=MessageChain.auto_make(msg),
        )
    def unpack_rawstring(self) -> str:
        return self.meta.get('msg', '')
    @classmethod
    def wrap_dict(cls, d: dict):
        return cls(
            chain=MessageChain.get_empty(),
            meta=d
        )

from abc import ABC, abstractmethod
import asyncio
import cfg
from loguru import logger
from collections import defaultdict
# from enum import Enum

class QUICSessionDefs:
    # 心跳包字符
    hbyte = b'D'
    # meta键
    META_CHANNEL_NAME   = 'C'
    META_SENDTO_TARGET  = 'S'
    # channel常量
    CHANNEL_COMMON  = 'CMN'
    CHANNEL_TASK    = 'TSK'
    CHANNEL_CONTROL = 'CTL'


class QUICSessionBase(ABC):
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self._reader = reader
        self._writer = writer
        self._ato = 0
        self._contentbuffer = []
        self._alive = True
        self._Qchannel = defaultdict(asyncio.Queue)
        self.connect_future = asyncio.ensure_future(self.keep_connect())
        self._readstate = -1
        self.initialize()
    
    @abstractmethod
    def initialize(self):
        raise NotImplementedError

    # @abstractmethod
    # def _distro_msg(self, msg: bytes):
    #     raise NotImplementedError

    # @abstractmethod
    async def recv(self, channel=QUICSessionDefs.CHANNEL_COMMON) -> CoreEntity:
        dt = await self._Qchannel[channel].get()
        # logger.info(dt)
        return dt
        # raise NotImplementedError
    @logger.catch
    async def keep_connect(self):
        while 1:
            res = await self._reader.read(cfg.buffer)
            logger.debug(">>> {}", res)
            if not res:
                for k, v in self._Qchannel.items():
                    v.put_nowait(ConnectionResetError('Connection closed'))
                raise ConnectionResetError("连接已断开") # 考虑用callback解决
            if res == QUICSessionDefs.hbyte: # 心跳包字串
                logger.debug('Heartbeat')
            else:
                for bts in res:

                    if self._readstate == -1: # 期待数字
                        if self._ato < 0: 
                            self._ato = 0
                        if bts in range(48, 57+1):
                            self._ato = self._ato * 10 + bts - 48
                        else:
                            self._contentbuffer.append(bytes([bts]))
                            self._ato -= 1
                            self._readstate = 0 # 期待payload
                    else:
                        if self._ato>0:
                            self._contentbuffer.append(bytes([bts]))
                            self._ato -= 1

                        if self._ato == 0:
                            self._readstate = -1
                            byte_stream = b''.join(self._contentbuffer)
                            self._contentbuffer = []
                            logger.debug(byte_stream)
                            ent = CoreEntity.handle_json(byte_stream)
                            channel = ent.meta.get(QUICSessionDefs.META_CHANNEL_NAME, QUICSessionDefs.CHANNEL_COMMON)

                            logger.debug('put to {}', channel)
                            self._Qchannel[channel].put_nowait(ent)
                # logger.debug("ato: {}, bts: {}", self._ato, bts)
                logger.debug("ato: {}", self._ato)
                    # logger.debug("buf: {}", self._contentbuffer)

    async def send(self, ent: CoreEntity) -> NoReturn:
        """发送CoreEntity对象"""
        data = ent.json()
        logger.debug("<<< {}", data)
        payload = data.encode('utf-8')
        contentlen = bytes(str(len(payload)), 'utf-8')
        self._writer.write(contentlen + payload)
