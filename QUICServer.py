# 只能运行在linux上，wsl也行

import argparse
import asyncio
import importlib
# import logger
import time
from collections import deque
from email.utils import formatdate
from typing import Callable, Deque, Dict, List, Optional, Union, cast


import aioquic
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.h3.connection import H3_ALPN, H3Connection
from aioquic.h3.events import DataReceived, H3Event, HeadersReceived
from aioquic.h3.exceptions import NoAvailablePushIDError
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import DatagramFrameReceived, ProtocolNegotiated, QuicEvent
from aioquic.tls import SessionTicket

import random
from basicutils.taskutils import ArgumentParser
import json
import os
import traceback

try:
    import uvloop
except ImportError:
    uvloop = None

import logging
logging.basicConfig(
	level=logging.DEBUG,  
	format='%(asctime)s<%(filename)s:%(lineno)d>[%(levelname)s]%(message)s',
	datefmt='%H:%M:%S'
)

from loguru import logger

busy_pool = {}
worker_pool = {}
worker_meta = {}

# worker_alias = {}
name_pool = set()

adapters = {}
adapters_meta = {}
player_adapter = {} # player -> adapter映射表

import cfg

sport = cfg.bind_port

import string
for digits in string.digits:
    for uppers in string.ascii_uppercase:
        name_pool.add(digits + uppers)

class SessionTicketStore:
    """
    Simple in-memory store for session tickets.
    """

    def __init__(self) -> None:
        self.tickets: Dict[bytes, SessionTicket] = {}

    def add(self, ticket: SessionTicket) -> None:
        self.tickets[ticket.ticket] = ticket

    def pop(self, label: bytes) -> Optional[SessionTicket]:
        return self.tickets.pop(label, None)


import datetime
from basicutils.socketutils import *

class QUICServerSession():
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self._reader = reader
        self._writer = writer
        self._alive = True
        self._Q = asyncio.Queue()
        asyncio.ensure_future(self.heartbeat())
        asyncio.ensure_future(self.keep_connect())


    async def heartbeat(self):
        try:
            while 1:
                if not self._alive:
                    logger.warning('Connection lost')
                    return
                await asyncio.sleep(cfg.heartbeat_time)
                self._writer.write(b'D')
        except:
            traceback.print_exc()
            logger.warning(traceback.format_exc())
    
    async def keep_connect(self):
        while 1:
            res = await self._reader.read(cfg.buffer)
            logger.info(res)
            if not res:
                self._alive = False
                self._Q.put_nowait(ConnectionResetError("连接已断开"))
                return
            if res == b'd': # 心跳包字串
                continue
            else:
                self._Q.put_nowait(res)

    async def send(self, data: str) -> NoReturn: self._writer.write(data.encode('utf-8'))
    async def recv(self) -> bytes: return await self._Q.get()

@logger.catch
async def handle_inbound(
    reader: asyncio.StreamReader, 
    writer: asyncio.StreamWriter
):
    data = await reader.read(cfg.buffer)
    message = data.decode()
    logger.info(message)
    role, vkey, *meta = message.split(' ', 2) # TODO: meta的player一次请求还是反向学习
    if vkey != cfg.quic_key:
        # writer.close()
        logger.critical("Detected invalid key {}", vkey)
        # logger.critical(vkey)
        return
    ses = QUICServerSession(reader, writer)

    async def worker():
        new_name = name_pool.pop()
        # worker_pool[new_name] = (reader, writer)
        worker_pool[new_name] = ses
        
        logger.info(f"new worker standby ... {new_name}")
        # asyncio.ensure_future(heartbeat(writer))
        try:
            while 1:
                msg = (await ses.recv()).decode('utf-8')
                # print(msg)
                logger.info('Received: {}', msg)
                ent: CoreEntity = CoreEntity.handle_json(msg)
                sendto: QUICServerSession = adapters[player_adapter[ent.player]]
                await sendto.send(msg)

        except:
            # traceback.print_exc()
            logger.warning(traceback.format_exc())
        finally:
            logger.warning('回收 {} => ', worker_pool.pop(new_name, '不在worker表中'))
            logger.warning('回收 {} => ', busy_pool.pop(new_name, '不在busy表中'))
            name_pool.add(new_name)
            
    async def adapter():
        syncid = random.randint(0, (1<<31) - 1)
        logger.info(f"new adapter standby ... {syncid}")
        while syncid in adapters:
            syncid = random.randint(0, (1<<31) - 1)
        adapters[syncid] = ses
        await ses.send(str(syncid))

        # ap = ArgumentParser()
        # ap.add_argument('cmd', default='help', choices=['exec', 'eval', 'run', 'send'], help="")
        async def sys_exec(args: list): return f"""{exec(' '.join(args))}"""
        async def sys_eval(args: list): return f"""{eval(' '.join(args))}"""
        async def sys_run(args: list): return f"""{os.popen(' '.join(args)).read()}"""
        async def sys_help(args: list): return '目前仅支持exec, eval, run, send四个命令'
        async def sys_adapters(args: list): return f'{adapters_meta}'
        async def sys_send(args: list):
            # await websocket.send(' '.join(args))
            ap = ArgumentParser('send')
            ap.add_argument('target', type=str, help='送往对象player号，若是QQ应该是一个整数')
            ap.add_argument('content', type=str, help='消息内容')
            try:
                ap.parse_args(args)
            except Exception as e:
                return '发送失败：' + str(e) + ap.format_help()
            if ap.target not in player_adapter:
                return '找不到player对应的adapter'
            else:
                sendto: QUICServerSession = adapters[player_adapter[ap.target]]
                ent.chain = MessageChain.auto_make(ap.content)
                await sendto.send(ent.json()) # 保证送出去的还是CoreEntity
                return '发送成功'
        def at_dead():
            """回收一个adapter连接"""
            adapters.pop(syncid)
            for k, v in tuple(player_adapter.items()):
                if v == syncid:
                    player_adapter.pop(k)
            logger.info('Adapter {} disconnected', syncid)

        switcher_t = {
            'exec': sys_exec,
            'eval': sys_eval,
            'run': sys_run,
            'send': sys_send,
            'adapters': sys_adapters,
        }


        try:
            while 1:
                data = (await ses.recv()).decode('utf-8')
                logger.debug("Adapter received: {}", data)
                if len(data) == 0:
                    at_dead()
                    break
                ent: CoreEntity = CoreEntity.handle_json(data)

                logger.debug(ent)
                logger.debug(ent.json())
                player_adapter[ent.player] = syncid # 反向学习

                data = ent.chain.onlyplain()
                c, *att = data.split(' ') 

                # Adapter参数预解析
                ato = []
                for i in att:
                    if i[:2] == "--":
                        arg,*val = i[2:].split("=")
                        ent.meta["-"+arg] = "".join(val)
                    else: ato.append(i)

                if c == 'sudo': # 系统命令
                    if ato:
                        c, *ato = ato
                    # c, ato = ap.parse_known_args(data.decode('utf-8').split(' '))
                    resp: str = await switcher_t.get(c, sys_help)(ato)
                    if not resp:
                        resp = 'No returns'
                    logger.critical(resp)
                    ent.chain = MessageChain.auto_make(resp)
                    await ses.send(ent.json())
                    # writer.write(resp.encode('utf-8'))
                else:
                    if not worker_pool:
                        await ses.send('没有可用的worker')
                        continue
                    idle = worker_pool.keys() - busy_pool.keys()
                    if idle:
                        wname = idle.pop()
                    else:
                        wname = random.choice(tuple(worker_pool.keys()))
                    wses: QUICServerSession = worker_pool[wname]
                    logger.info("worker {} gain work", wname)
                    busy_pool[wname] = ent.meta['ts'] = datetime.datetime.now().timestamp()
                    await wses.send('task ' + ent.json()) # 往worker里面塞东西需要一个头
                # await writer.drain()
        except Exception as e:
            at_dead()
            logger.error(traceback.format_exc())
            # raise e
        
    switcher = {
        'W': worker,
        'A': adapter
    }
    await switcher[role]()
    # asyncio.ensure_future(
    #     switcher[role]()
    # )
    logger.critical("Session exit!")

@logger.catch
def inbound_wrapper(reader, writer):
    asyncio.ensure_future(handle_inbound(reader, writer))

# import websockets
# import ssl

if __name__ == "__main__":
    conf = QuicConfiguration(
        # alpn_protocols=H3_ALPN,
        is_client=False,
        # max_datagram_frame_size=cfg.buffer,
        # idle_timeout=cfg.idle_tle,
        # quic_logger=logger.Logger,
        # secrets_log_file=secrets_log_file,
    )

    conf.load_cert_chain('ssl/A.crt', 'ssl/A.key')

    ticket_store = SessionTicketStore()

    server = aioquic.asyncio.serve(
        '0.0.0.0', sport, 
        configuration=conf, 
        stream_handler=inbound_wrapper,
        # session_ticket_fetcher=ticket_store.pop,
        # session_ticket_handler=ticket_store.add,
        retry=False
    )

    logger.info(f'QUIC listening on 0.0.0.0 {sport}')


    loop = asyncio.get_event_loop()
    loop.run_until_complete(server)
    logger.info(server)
    # asyncio.run(server)
    try:
        loop.run_forever()
        logger.critical('Done')
    except KeyboardInterrupt:
        traceback.print_exc()
