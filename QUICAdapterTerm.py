import aioquic

import json
import logging
import asyncio
from typing import NoReturn
from basicutils.taskutils import ArgumentParser
from loguru import logger
import sys

logger.add(lambda msg: print())

# logger.add(sys.stdout, format='>')
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import PromptSession

logging.basicConfig(
	level=logging.DEBUG,  
	format='%(asctime)s<%(filename)s:%(lineno)d>[%(levelname)s]%(message)s',
	datefmt='%H:%M:%S'
)

import cfg

sport = cfg.quic_port
hostname = cfg.quic_host

from basicutils.socketutils import *

class QUICTerminalSession(QUICSessionBase):
    def initialize(self):
        pass
    # def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    #     self._reader = reader
    #     self._writer = writer
    #     self._contentbuffer = []
    #     self._ato = -1

    #     self._Q = asyncio.Queue()
    #     asyncio.ensure_future(self.keep_connect())
    # async def keep_connect(self):
    #     while 1:
    #         res = await self._reader.read(cfg.buffer)
    #         if not res:
    #             raise ConnectionResetError("连接已断开")
    #         if res == b'D': # 心跳包字串
    #             logger.debug('Heartbeat')
    #             self._writer.write(b'd')
    #         else:
    #             if self._ato == -1:
    #                 ptr = 0
    #                 while res[ptr] in range(48, 57+1):
    #                     self._ato = self._ato * 10 + res[ptr] - 48
    #                     ptr += 1
    #                 self._contentbuffer.append(res[ptr:])
    #                 self._ato -= len(self._contentbuffer[-1])
    #             else:
    #                 self._contentbuffer.append(res)
    #                 self._ato -= len(self._contentbuffer[-1])
    #             if self._ato == 0:
    #                 self._ato = -1
    #                 self._Q.put_nowait(b''.join(res))
    # async def recv(self) -> bytes: return await self._Q.get()
    # async def send(self, data: str) -> NoReturn:
    #     payload = data.encode('utf-8')
    #     contentlen = bytes(str(len(payload)), 'utf-8')
    #     self._writer.write(contentlen + payload)



import concurrent.futures
import datetime
import traceback
from basicutils.socketutils import *

import ssl
from aioquic.quic.configuration import QuicConfiguration
from aioquic.h3.connection import H3_ALPN
from aioquic.asyncio.client import connect
import functools

syncid: str
playerid: str

async def run():
    with patch_stdout():
        conf = QuicConfiguration(
            alpn_protocols=H3_ALPN,
            is_client=True,
            max_datagram_frame_size=cfg.buffer,
            idle_timeout=cfg.idle_tle,
            verify_mode=ssl.CERT_NONE
            # quic_logger=logger.Logger,
            # secrets_log_file=secrets_log_file,
        )
        loop = asyncio.get_running_loop()
        print(hostname, sport)
        # while 1:
        async with connect(
            cfg.quic_host,
            cfg.quic_port,
            configuration=conf
        ) as C:
            # reader:asyncio.StreamReader
            # writer:asyncio.StreamWriter
            ses = QUICTerminalSession(*(await C.create_stream()))
            await ses.send(f'A {cfg.quic_key}')
            
            syncid = (await ses.recv()).decode('utf-8')
            logger.critical("您的终端号：{}", syncid)

            async def pulling_loop():
                while 1:
                    ent = await ses.recv()
                    # smsg = msg.decode('utf-8')
                    logger.debug('消息：\n{}', smsg)
                    # ent: CoreEntity = CoreEntity.handle_json(smsg)
                    logger.info('文本内容：\n{}', ent.chain.onlyplain())
            asyncio.ensure_future(pulling_loop())
            app = ArgumentParser('command')
            app.add_argument('cmd', choices=[
                'send', 'raw', 'hex', 'eval'
            ])
            session = PromptSession('(irori)>')
            while 1:
                try:
                    cmdlist = (await session.prompt_async()).split()
                    session.message = '(irori OwO)>'
                    if not cmdlist:
                        continue
                    cmd, *ato = cmdlist
                    logger.debug(ato)
                    
                    if cmd == 'send':
                        # player, message = cmdlist
                        ent = CoreEntity(
                            chain=MessageChain.auto_make(' '.join(ato)),
                            player=playerid,
                            source=syncid,
                            meta={},
                            mode='W'
                        )
                        tosend = ent.json()
                        logger.debug('SEND {}', tosend)
                        await ses.send(tosend)

                except KeyboardInterrupt:
                    break
                except:
                    logger.debug(traceback.format_exc())
                    session.message = '(irori QwQ)>'
                    app.print_help()
                    # print("send")

                
                        


if __name__ == "__main__":
    playerid = 'T' + input('随便取一个playerid？>>>')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    