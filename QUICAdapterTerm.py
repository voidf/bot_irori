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
            reader, writer = await C.create_stream()

            writer.write(f'A {cfg.quic_admin_key} {playerid}'.encode('utf-8'))
            
            ses = QUICTerminalSession(reader, writer)
            syncid = (await ses.recv()).unpack_rawstring()
            logger.critical("您的终端号：{}", syncid)

            async def pulling_loop():
                while 1:
                    ent = await ses.recv()
                    plaintext = ent.chain.onlyplain()
                    if plaintext:
                        logger.info('文本内容：\n{}', plaintext)
                    sysinfo = ent.unpack_rawstring()
                    if sysinfo:
                        logger.warning('系统消息：\n{}', sysinfo)
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
                            meta={}
                        )
                        # tosend = ent.json()
                        logger.debug('SEND {}', ent.json())
                        await ses.send(ent)

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
    