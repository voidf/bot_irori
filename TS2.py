import aioquic

import json
from loguru import logger
import asyncio
from typing import NoReturn

import logging
logging.basicConfig(
	level=logging.DEBUG,  
	format='%(asctime)s<%(filename)s:%(lineno)d>[%(levelname)s]%(message)s',
	datefmt='%H:%M:%S'
)
buffersize = 65536

class QUICWorkerSession:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self._reader = reader
        self._writer = writer
        self._Q = asyncio.Queue()
        asyncio.ensure_future(self.keep_connect())
    async def keep_connect(self):
        while 1:
            res = await self._reader.read(buffersize)
            if not res:
                raise ConnectionResetError()
            if res == b'D':
                logger.debug('Heartbeat')
                self._writer.write(b'd') # send Heartbeat ACK msg
            else:
                logger.debug(f'Putting {res} into queue')
                self._Q.put_nowait(res)

    async def recv(self) -> bytes: return await self._Q.get()
    async def send(self, data: str) -> NoReturn: self._writer.write(data.encode('utf-8'))

import traceback

import ssl
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.client import connect

@logger.catch
async def run():
    conf = QuicConfiguration(
        is_client=True,
        verify_mode=ssl.CERT_NONE
    )
    loop = asyncio.get_running_loop()
    async with connect(
        '127.0.0.1',
        8110,
        configuration=conf
    ) as C:
        ses = QUICWorkerSession(*(await C.create_stream()))
        await ses.send('mykey')

        while 1:
            cmd = await ses.recv()
            if cmd == b'kill':
                logger.warning('Kill signal detected')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run())
    