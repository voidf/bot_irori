import asyncio
from typing import Callable, Deque, Dict, List, Optional, Union, cast


import aioquic
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.tls import SessionTicket

import random
import traceback

import logging
logging.basicConfig(
	level=logging.DEBUG,  
	format='%(asctime)s<%(filename)s:%(lineno)d>[%(levelname)s]%(message)s',
	datefmt='%H:%M:%S'
)
from loguru import logger

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
buffersize = 65536

class QUICServerSession:
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
                await asyncio.sleep(20)
                self._writer.write(b'D')
        except:
            logger.warning(traceback.format_exc())
    
    async def keep_connect(self):
        while 1:
            res = await self._reader.read(buffersize)
            if not res:
                self._Q.put_nowait(ConnectionResetError("ConnectionReset"))
                self._alive = False
                return
            if res == b'd':
                logger.debug(res)
                continue
            else:
                logger.info(res)
                self._Q.put_nowait(res)

    async def send(self, data: str): self._writer.write(data.encode('utf-8'))
    async def recv(self) -> bytes: return await self._Q.get()

worker_pool={}
adapters={}

async def handle_inbound(
    reader: asyncio.StreamReader, 
    writer: asyncio.StreamWriter
):
    data = await reader.read(65536)
    message = data.decode()
    logger.info(message)
    vkey, *meta = message.split(' ', 2)
    if vkey != 'mykey':
        logger.critical(f"Detected invalid key {vkey}")
        return
    ses = QUICServerSession(reader, writer)

    new_name = random.randint(0, 65535)
    while new_name in worker_pool:
        new_name = random.randint(0, 65535)
    worker_pool[new_name] = ses
    logger.info(f"new worker standby ... {new_name}")
    try:
        # raise NameError('233')
        while 1:
            msg = (await ses.recv()).decode('utf-8')
            logger.info('Received: {}', msg)
    except:
        logger.warning(traceback.format_exc())
    finally:
        logger.warning('Discard {} => ', new_name)
        worker_pool.pop(new_name, '')

    logger.critical("Session exit!")

def inbound_wrapper(reader, writer):
    try:
        asyncio.ensure_future(handle_inbound(reader, writer))
    except:
        logger.warning(traceback.format_exc())

if __name__ == "__main__":
    conf = QuicConfiguration(
        is_client=False,
    )

    conf.load_cert_chain('ssl/A.crt', 'ssl/A.key')

    ticket_store = SessionTicketStore()

    server = aioquic.asyncio.serve(
        '0.0.0.0', 8110, 
        configuration=conf, 
        stream_handler=inbound_wrapper,
        session_ticket_fetcher=ticket_store.pop,
        session_ticket_handler=ticket_store.add,
        retry=False
    )

    logger.info(f'QUIC listening on 0.0.0.0 {8110}')

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(server)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.critical(traceback.format_exc())
