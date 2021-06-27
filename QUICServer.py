import argparse
import asyncio
import importlib
import logging
import time
from collections import deque
from email.utils import formatdate
from typing import Callable, Deque, Dict, List, Optional, Union, cast

import wsproto
import wsproto.events

import aioquic
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.h3.connection import H3_ALPN, H3Connection
from aioquic.h3.events import DataReceived, H3Event, HeadersReceived
from aioquic.h3.exceptions import NoAvailablePushIDError
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import DatagramFrameReceived, ProtocolNegotiated, QuicEvent
from aioquic.tls import SessionTicket

import random
from taskutils import ArgumentParser
import json
import os
import traceback

try:
    import uvloop
except ImportError:
    uvloop = None

logging.basicConfig(
	level=logging.DEBUG,  
	format='%(asctime)s<%(filename)s:%(lineno)d>[%(levelname)s]%(message)s',
	datefmt='%H:%M:%S'
)

# logger = logging.Logger('')

busy_pool = {}
worker_pool = {}

worker_alias = {}
name_pool = set()

terminals = {}

with open('cfg.json', 'r',encoding='utf-8') as f:
    jj = json.load(f)
    wsuri = jj['ws']
    sport = jj['socket_port']
    cport = jj['control_port']
    del jj
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

async def heartbeat(writer: asyncio.StreamWriter):
    try:
        while 1:
            await asyncio.sleep(60)
            writer.write(b'Doki')
    except:
        traceback.print_exc()

import datetime
async def handle_inbound(
    reader: asyncio.StreamReader, 
    writer: asyncio.StreamWriter
):
    data = await reader.read(1<<16)
    message = data.decode()
    print(message)
    role, vkey = message.split(' ')
    addr = writer.get_extra_info('peername')

    async def worker():
        worker_pool[addr] = (reader, writer)
        new_name = name_pool.pop()
        worker_alias[new_name] = addr
        logging.info(f"new worker standby ... {new_name} => {addr}")
        asyncio.ensure_future(heartbeat(writer))
        try:
            while 1:
                msg = await reader.read(1<<16)
                if msg == b'doki': # 这里做业务处理
                    print('心跳，',datetime.datetime.now())
                    continue
        except:
            traceback.print_exc()
        finally:
            worker_pool.pop(addr)
    async def terminal():
        logging.info(f"new terminal standby ... => {addr}")
        ap = ArgumentParser()
        ap.add_argument('cmd', default='help', choices=['exec', 'eval', 'run', 'send'], help="欢迎使用irori终端，以上是目前支持的命令，输入help或未匹配上面的命令会出现此提示。")
        async def sys_exec(args: list): return f"""{exec(' '.join(args))}"""
        async def sys_eval(args: list): return f"""{eval(' '.join(args))}"""
        async def sys_run(args: list): return f"""{os.popen(' '.join(args)).read()}"""
        async def sys_help(args: list): return ''
        async def sys_send(args: list):
            # await websocket.send(' '.join(args))
            return ''
        switcher_t = {
            'exec': sys_exec,
            'eval': sys_eval,
            'run': sys_run,
            'send': sys_send
        }
        syncid = random.randint(0, (1<<31) - 1)
        while syncid in terminals:
            syncid = random.randint(0, (1<<31) - 1)

        terminals[syncid] = writer
        try:
            while 1:
                data = await reader.read(1<<16)
                if len(data) == 0:
                    terminals.pop(syncid)
                    break
                c, ato = ap.parse_known_args(data.decode('utf-8').split(' '))
                resp: str = await switcher_t.get(c.cmd, sys_help)(ato)
                if not resp:
                    resp = 'No returns'
                logging.critical(resp)
                writer.write(resp.encode('utf-8'))
                # await writer.drain()
        except Exception as e:
            terminals.pop(syncid)
            raise e
        
    switcher = {
        'worker': worker,
        'terminal': terminal
    }
    asyncio.ensure_future(
        switcher[role]()
    )

def inbound_wrapper(reader, writer):
    asyncio.ensure_future(handle_inbound(reader, writer))

if __name__ == "__main__":
    conf = QuicConfiguration(
        alpn_protocols=H3_ALPN,
        is_client=False,
        max_datagram_frame_size=65536,
        idle_timeout=200
        # quic_logger=logging.Logger,
        # secrets_log_file=secrets_log_file,
    )

    conf.load_cert_chain('ssl/A.crt', 'ssl/A.key')

    ticket_store = SessionTicketStore()

    server = aioquic.asyncio.serve(
        '0.0.0.0', sport, 
        configuration=conf, 
        stream_handler=inbound_wrapper,
        session_ticket_fetcher=ticket_store.pop,
        session_ticket_handler=ticket_store.add,
    )
    # monitor = await asyncio.start_server(handle_inbound, '0.0.0.0', cport)
    # addr = server.sockets[0].getsockname()
    logging.info(f'Socket Serving started at 0.0.0.0 {sport}')


    loop = asyncio.get_event_loop()
    loop.run_until_complete(server)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        traceback.print_exc()
