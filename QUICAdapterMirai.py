import aioquic

import json
import logging
import asyncio
from typing import NoReturn
from basicutils.taskutils import ArgumentParser
from loguru import logger
import sys
import aiohttp

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

class QUICMiraiSession(QUICSessionBase):
    def initialize(self):
        self.ases = aiohttp.ClientSession()
        
    async def pulling_loop(self):
        while 1:
            ent = await self.recv()
            plaintext = ent.chain.onlyplain()
            if plaintext:
                logger.info('文本内容：\n{}', plaintext) # 处理irori server的信息
                await self.upload_chain(ent)
            sysinfo = ent.unpack_rawstring()
            if sysinfo:
                logger.warning('系统消息：\n{}', sysinfo)
    
    async def command_loop(self):
        app = ArgumentParser('command')
        app.add_argument('cmd', choices=[
            'send', 'raw', 'hex', 'eval', 'sudo', 'api'
        ])
        session = PromptSession('(irori - Mirai)>')
        while 1:
            try:
                cmdlist = (await session.prompt_async()).split()
                session.message = '(irori - Mirai OwO)>'
                if not cmdlist:
                    continue
                cmd, *ato = cmdlist
                logger.debug(ato)
                
                if cmd == 'send':
                    # player, message = cmdlist
                    ent = CoreEntity(
                        chain=MessageChain.auto_make(' '.join(ato)),
                        player=self.playerid,
                        source=self.syncid,
                        meta={}
                    )
                    # tosend = ent.json()
                    logger.debug('SEND {}', ent.json())
                    await self.send(ent)
                elif cmd == 'sudo':
                    ent = CoreEntity(
                        chain=MessageChain.auto_make(' '.join(['sudo'] + ato)),
                        player=self.playerid,
                        source=self.syncid,
                        meta={}
                    )
                    logger.debug('SEND {}', ent.json())
                    await self.send(ent)
                elif cmd == 'api':
                    content = ' '.join(ato)
                    logger.debug('SEND {}', content)
                    await self.ws.send_json(content)
            except KeyboardInterrupt:
                break
            except:
                logger.debug(traceback.format_exc())
                session.message = '(irori - Mirai QwQ)>'
                app.print_help()

    async def mirai_loop(self, syncid: str):
        self.syncid = syncid
        self.ws = await self.ases.ws_connect(cfg.authdata['url'] + f'all?qq={cfg.authdata["qq"]}&verifyKey={cfg.authdata["token"]}')
        asyncio.ensure_future(self.pulling_loop())
        asyncio.ensure_future(self.command_loop())
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                logger.critical(msg.data)
                j = json.loads(msg.data)
                if 'data' in j and 'type' in j['data']:
                    if j['data']['type'] == 'GroupMessage':
                        ent = CoreEntity(
                            player=str(j['data']['sender']['group']['id'] + (1<<39)),
                            source=str(self.syncid),
                            meta={'mem': j['data']['sender']['id']},
                            chain=MessageChain.auto_make(j['data']['messageChain'])
                        )
                        await self.send(ent)
                    elif j['data']['type'] == 'FriendMessage':
                        ent = CoreEntity(
                            player=str(j['data']['sender']['id']),
                            source=str(self.syncid),
                            meta={'mem': j['data']['sender']['id']},
                            chain=MessageChain.auto_make(j['data']['messageChain'])
                        )
                        await self.send(ent)

            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
        
    async def upload_chain(self, ent: CoreEntity):
        """将消息链往mirai发送"""
        try:
            pi = int(ent.player)
            payload = {
                "syncId": self.syncid,
                "content": {
                    "messageChain": ent.chain.dict()["__root__"]
                },
            }
            if pi > (1<<32):
                pi -= 1<<39
                payload['command'] = "sendGroupMessage"
                payload['content']['target'] = pi
                logger.warning(json.dumps(payload))
                await self.ws.send_json(payload)
            else:
                payload['command'] = "sendFriendMessage"
                payload['content']['target'] = pi
                logger.warning(json.dumps(payload))
                await self.ws.send_json(payload)

        except ValueError:
            return "not mirai"

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



import uuid

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
            pid = 'Irori - ' + str(uuid.uuid1())
            writer.write(f'A {cfg.quic_admin_key} {pid}'.encode('utf-8'))
            
            ses = QUICMiraiSession(reader, writer)
            ses.playerid = pid
            syncid = (await ses.recv()).unpack_rawstring()
            logger.critical("您的终端号：{}", syncid)
            await ses.mirai_loop(syncid)

            # async with aiohttp.ClientSession() as ases:
                
                    

                    

            
                
                        


if __name__ == "__main__":
    # playerid = 'T' + input('随便取一个playerid？>>>')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    