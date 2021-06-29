import aioquic

import json
import logging
import asyncio
from typing import NoReturn

logging.basicConfig(
	level=logging.DEBUG,  
	format='%(asctime)s<%(filename)s:%(lineno)d>[%(levelname)s]%(message)s',
	datefmt='%H:%M:%S'
)

import cfg

sport = cfg.socket_port
hostname = cfg.socket_host

class Session:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self._reader = reader
        self._writer = writer
        self._Qcontrol = asyncio.Queue()
        self._Qtask = asyncio.Queue()
        asyncio.ensure_future(self.keep_connect())
    async def keep_connect(self):
        while 1:
            res = await self._reader.read(cfg.buffer)
            if not res:
                raise ConnectionResetError("连接已断开")
            if res == b'D': # 心跳包字串
                self._writer.write(b'd')
            else:
                header, ato = res.split(b' ', 1) # task, control二选一
                if header == b'task':
                    self._Qtask.put_nowait(ato)
                elif header == b'control':
                    self._Qcontrol.put_nowait(ato)
                else:
                    raise NotImplementedError('无法处理此协议头：未实现')

    async def recv_control(self) -> bytes: return self._Qcontrol.get()
    async def recv_task(self) -> bytes: return self._Qtask.get()
    async def send(self, data: str) -> NoReturn: self._writer.write(data.encode('utf-8'))


import concurrent.futures
import datetime
import traceback
from socketutils import *
from multiprocessing.dummy import Pool as Pool2
def task_monitor(taskstr):
    task: TaskMessage = TaskMessage.parse_raw(taskstr)
    rawstr = task.chain.onlyplain()
    cmd, argstr = rawstr.split(' ', 1) 
    
    tle = task.meta.get('tle', 30)
    p = Pool2(1)
    res = p.apply_async(func, args=args)
    try:
        out = res.get(tle)
        return out
    except:
        traceback.print_exc()
        msg = '执行超时'
import ssl
from aioquic.quic.configuration import QuicConfiguration
from aioquic.h3.connection import H3_ALPN
from aioquic.asyncio.client import connect
import functools
async def run():
    conf = QuicConfiguration(
        alpn_protocols=H3_ALPN,
        is_client=True,
        max_datagram_frame_size=65536,
        idle_timeout=70,
        verify_mode=ssl.CERT_NONE
        # quic_logger=logging.Logger,
        # secrets_log_file=secrets_log_file,
    )
    loop = asyncio.get_running_loop()
    print(hostname, sport)
    while 1:
        async with connect(
            '4kr.top',
            8228,
            configuration=conf
        ) as C:
            # reader:asyncio.StreamReader
            # writer:asyncio.StreamWriter
            ses = Session(*(await C.create_stream()))
            ses.send('worker 114514')
            # G = 
            with concurrent.futures.ProcessPoolExecutor(1) as pool:
                async def assign_task_loop():
                    while 1:
                        rawtask = await ses.recv_task()
                        result = await loop.run_in_executor(
                            pool, functools.partial(
                                task_monitor, rawtask.decode('utf-8')
                            )
                        )
                # async def control_loop():
                while 1:
                    cmd = await ses.recv_control()
                    if cmd == b'kill':
                        # pool.shutdown(True)
                        for k, v in pool._processes.items():
                            v.kill()



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    