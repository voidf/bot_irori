import aioquic

import json
import logging
import asyncio

hostname = '127.0.0.1'

logging.basicConfig(
	level=logging.DEBUG,  
	format='%(asctime)s<%(filename)s:%(lineno)d>[%(levelname)s]%(message)s',
	datefmt='%H:%M:%S'
)

with open('cfg.json', 'r',encoding='utf-8') as f:
    jj = json.load(f)
    sport = jj['socket_port']
    del jj


import datetime
import traceback
from multiprocessing.dummy import Pool as Pool2
def task_monitor(func, *args, **kwargs):
    tle = kwargs.get('tle', None)
    p = Pool2(1)
    res = p.apply_async(func, args=args)
    pid = kwargs['pid']
    # print(kwargs)
    try:
        out = res.get(tle)
        # kwargs['worker'].release()

        tmpd = kwargs['pcb'][pid]
        tmpd['status'] = 'done'
        kwargs['pcb'].update({pid:tmpd})
        # kwargs['pcb'][pid].update(status='done')
        # print(kwargs)
        print(pid, '执行完毕, 结果：', out)
        return out
    except:
        traceback.print_exc()
        # kwargs['worker'].release()

        tmpd = kwargs['pcb'][pid]
        tmpd['status'] = 'timeout'
        kwargs['pcb'].update({pid:tmpd})
        print(pid, '执行超时')
import ssl
from aioquic.quic.configuration import QuicConfiguration
from aioquic.h3.connection import H3_ALPN
from aioquic.asyncio.client import connect
async def run():
    conf = QuicConfiguration(
        alpn_protocols=H3_ALPN,
        is_client=True,
        max_datagram_frame_size=65536,
        idle_timeout=200,
        verify_mode=ssl.CERT_NONE
        # quic_logger=logging.Logger,
        # secrets_log_file=secrets_log_file,
    )
    print(hostname, sport)
    async with connect(
        hostname,
        sport,
        configuration=conf
    ) as C:
        reader:asyncio.StreamReader
        writer:asyncio.StreamWriter
        reader, writer = await C.create_stream()
        writer.write(b'worker 114514')
        d1 = datetime.datetime.now()
        print(d1)
        # await writer.drain()
        try:
            while 1:
                msg = await reader.read(1<<16)
                if msg == b'Doki':
                    print(msg, datetime.datetime.now())
                    writer.write(b'doki')
                    continue
        except:
            traceback.print_exc()
        d2 = datetime.datetime.now()
        print(d2)
        print(d2-d1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    