from abc import ABC, abstractmethod
import asyncio
from QUICFaker import Configuration as cfg
from loguru import logger
from collections import defaultdict
from basicutils.network import *
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

