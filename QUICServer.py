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


class QUICServerSession(QUICSessionBase):
    def on_connection_lost(self, arg: asyncio.Future):
        logger.warning('lost with {}', arg)
        self._alive = False
        self.connect_future.cancel()
    def initialize(self):
        self.heartbeat_future = asyncio.ensure_future(self.heartbeat())
        self.connect_future.add_done_callback(self.on_connection_lost)

    async def heartbeat(self):
        try:
            while 1:
                if not self._alive:
                    logger.warning('Connection lost')
                    return
                await asyncio.sleep(cfg.heartbeat_time)
                self._writer.write(QUICSessionDefs.hbyte)
        except:
            traceback.print_exc()
            logger.warning(traceback.format_exc())
    


@logger.catch
def announcement(msg: Union[str, CoreEntity], ignored=[]):
    if isinstance(msg, str):
        ent = CoreEntity.wrap_rawstring(msg)
    elif isinstance(msg, CoreEntity):
        ent = msg
    else:
        raise TypeError('广播消息类型错误')
    for k, v in adapters.items():
        if str(k) not in ignored:
            # logger.debug('k: {}, ignored: {}', k, ignored)
            asyncio.ensure_future(v.send(ent))

@logger.catch
def at_dead(syncid):
    """回收一个adapter连接"""
    adapters.pop(syncid)
    announcement(f"终端节点「{syncid}」已离线")
    for k, v in tuple(player_adapter.items()):
        if v == syncid:
            player_adapter.pop(k)
    logger.info('Adapter {} disconnected', syncid)

# 管理员函数族
async def sys_exec(ent: CoreEntity, args: list): return f"""{exec(' '.join(args))}"""
async def sys_eval(ent: CoreEntity, args: list): return f"""{eval(' '.join(args))}"""
async def sys_run(ent: CoreEntity, args: list): return f"""{os.popen(' '.join(args)).read()}"""
async def sys_help(ent: CoreEntity, args: list): return '目前仅支持exec, eval, run, send四个命令'
async def sys_adapters(ent: CoreEntity, args: list): return f'{player_adapter}'
async def sys_unauthorized(ent: CoreEntity, args: list): return "您没有权限执行此调用"
async def sys_announcement(ent: CoreEntity, args: list): 
    announcement(' '.join(args), [ent.source])
    return '广播成功'
async def sys_sendp(ent: CoreEntity, args: list):
    # await websocket.send(' '.join(args))
    ap = ArgumentParser('send')
    ap.add_argument('target', type=str, help='送往对象player号，若是QQ应该是一个整数')
    ap.add_argument('content', type=str, help='消息内容')
    try:
        pap = ap.parse_args(args)
    except Exception as e:
        return '发送失败：' + str(e) + ap.format_help()
    if pap.target not in player_adapter:
        return '找不到player对应的adapter'
    else:
        sendto: QUICServerSession = adapters[player_adapter[pap.target]]
        ent.chain = MessageChain.auto_make(pap.content)
        await sendto.send(ent) # 保证送出去的还是CoreEntity
        return '发送成功'
async def sys_sends(ent: CoreEntity, args: list):
    # await websocket.send(' '.join(args))
    ap = ArgumentParser('send')
    ap.add_argument('target', type=str, help='送往对象终端号(syncid)')
    ap.add_argument('content', type=str, help='消息内容')
    try:
        pap = ap.parse_args(args)
    except Exception as e:
        return '发送失败：' + str(e) + ap.format_help()
    if pap.target not in adapters:
        return '找不到syncid对应的adapter'
    else:
        sendto: QUICServerSession = adapters[pap.target]
        ent.chain = MessageChain.auto_make(pap.content)
        await sendto.send(ent) # 保证送出去的还是CoreEntity
        return '发送成功'




@logger.catch
async def handle_inbound(
    reader: asyncio.StreamReader, 
    writer: asyncio.StreamWriter
):
    data = await reader.read(cfg.buffer)
    message = data.decode()
    logger.info(message)
    role, vkey, *meta = message.split(' ', 2) # TODO: meta的player一次请求还是反向学习
    if vkey not in (cfg.quic_key, cfg.quic_admin_key):
        logger.critical("Detected invalid key {}", vkey)
        return
    ses = QUICServerSession(reader, writer)

    async def worker():
        new_name = name_pool.pop()
        worker_pool[new_name] = ses
        logger.info(f"new worker standby ... {new_name}")
        announcement(f"新的工作节点「{new_name}」已上线")
        try:
            while 1:
                ent = (await ses.recv())
                sendto: QUICServerSession = adapters[player_adapter[ent.player]]
                await sendto.send(ent)
        except:
            logger.warning(traceback.format_exc())
        finally:
            announcement(f"工作节点「{new_name}」已离线")
            logger.warning('回收 {}的会话: {}', new_name, worker_pool.pop(new_name, '不在worker表中'))
            logger.warning('回收 {}的busy: {}', new_name, busy_pool.pop(new_name, '不在busy表中'))
            name_pool.add(new_name)
            
    async def adapter():
        syncid = random.randint(0, (1<<31) - 1)
        while syncid in adapters:
            syncid = random.randint(0, (1<<31) - 1)
        logger.info(f"new adapter standby ... {syncid}")
        playerid = ''.join(meta)
        player_adapter[playerid] = syncid           # 登录昵称
        announcement(f"「{playerid}」已登录，终端号为：[{syncid}]")
        adapters[syncid] = ses
        await ses.send(CoreEntity.wrap_rawstring(str(syncid)))
        if vkey == cfg.quic_admin_key: # 简单的鉴权
            async def handle_sudo(ato):
                switcher_t = {
                    'exec': sys_exec,
                    'eval': sys_eval,
                    'run': sys_run,
                    'send': sys_sendp,
                    'sends': sys_sends,
                    'adapters': sys_adapters,
                    'announce': sys_announcement,
                }
                if ato:
                    c, *ato = ato
                resp: str = await switcher_t.get(c, sys_help)(ent, ato)
                if not resp:
                    resp = 'No returns'
                logger.critical(resp)
                ent.chain = MessageChain.auto_make(resp)
                await ses.send(ent)
        else:
            async def handle_sudo(ato):
                # ent = CoreEntity.wrap_rawstring('您没有权限执行此调用')
                # await ses.send(ent)

                switcher_t = {
                    'send': sys_sendp,
                    'sends': sys_sends,
                    'adapters': sys_adapters,
                }
                if ato:
                    c, *ato = ato
                resp: str = await switcher_t.get(c, sys_unauthorized)(ent, ato)
                if not resp:
                    resp = 'No returns'
                logger.critical(resp)
                ent.chain = MessageChain.auto_make(resp)
                await ses.send(ent)
        try:
            while 1:
                ent = (await ses.recv())
                logger.debug("Adapter received: {}", ent)
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
                    await handle_sudo(ato)
                else: # TODO: 分析meta实现adapter间消息传送
                    if not worker_pool:
                        ent.chain = MessageChain.auto_make('没有可用的worker')
                        await ses.send(ent)
                        continue
                    idle = worker_pool.keys() - busy_pool.keys()
                    if idle:
                        wname = idle.pop()
                    else:
                        wname = random.choice(tuple(worker_pool.keys()))
                    wses: QUICServerSession = worker_pool[wname]
                    logger.info("worker {} gain work", wname)
                    busy_pool[wname] = ent.meta['ts'] = datetime.datetime.now().timestamp()
                    ent.meta[QUICSessionDefs.META_CHANNEL_NAME] = QUICSessionDefs.CHANNEL_TASK
                    await wses.send(ent) # 往worker里面塞东西需要一个头
                # await writer.drain()
        except Exception as e:
            at_dead(syncid)
            logger.error(traceback.format_exc())
            # raise e
        
    switcher = {
        'W': worker,
        'A': adapter
    }
    await switcher[role]()
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
        max_datagram_frame_size=cfg.buffer,
        idle_timeout=cfg.idle_tle,
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
