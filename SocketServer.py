import socket, ssl
import websockets
import logging
import asyncio

import random

logging.basicConfig(
	level=logging.DEBUG,  
	format='%(asctime)s<%(filename)s:%(lineno)d>[%(levelname)s]%(message)s',
	datefmt='%d %H:%M:%S'
)



worker_pool = {}
worker_alias = {}
name_pool = set()

terminals = {}

import json
import argparse
import os

with open('cfg.json', 'r',encoding='utf-8') as f:
    jj = json.load(f)
    wsuri = jj['ws']
    sport = jj['socket_port']
    del jj

async def main():
    # async def handle_ws_inbound(ws: websockets.WebSocketCommonProtocol, path: str):
    async with websockets.connect(wsuri) as websocket:
        logging.info("LOGGED INTO MIRAI WS")
        async def pull_event():
            while 1:
            # await websocket.send("Hello world!")
                wsmsg: bytes = await websocket.recv()
                jsoncontent = json.loads(wsmsg.decode('utf-8'))
                
                logging.warning(wsmsg)

        

        async def handle_inbound(
            reader: asyncio.StreamReader, 
            writer: asyncio.StreamWriter
        ):
            data = await reader.read(1<<16)
            message = data.decode()
            role, *args = message.split(' ')

            addr = writer.get_extra_info('peername')

            async def worker():
                worker_pool[addr] = (reader, writer)
                new_name = name_pool.pop()
                worker_alias[new_name] = addr
                logging.info(f"new worker standby ... {new_name} => {addr}")
            async def terminal():
                logging.info(f"new terminal standby ... => {addr}")
                async def sys_exec(args: list): return f"""{exec(' '.join(args))}"""
                async def sys_eval(args: list): return f"""{eval(' '.join(args))}"""
                async def sys_run(args: list): return f"""{os.popen(' '.join(args)).read()}"""
                async def sys_blank(args: list): return ''
                async def sys_send(args: list):
                    await websocket.send(' '.join(args))
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
                        ap = argparse.ArgumentParser()
                        ap.add_argument('cmd', default='blank')
                        c, ato = ap.parse_known_args(data.decode('utf-8').split(' '))
                        resp: str = await switcher_t.get(c.cmd, sys_blank)(ato)
                        if not resp:
                            resp = 'No returns'
                        logging.critical(resp)
                        writer.write(resp.encode('utf-8'))
                        await writer.drain()
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
        server = await asyncio.start_server(handle_inbound, '0.0.0.0', sport)
        addr = server.sockets[0].getsockname()
        logging.info(f'Socket Serving on {addr}')
        asyncio.ensure_future(pull_event())


        # writer.write(data)
        # await writer.drain()

        async with server:
            await server.serve_forever()
import string
for digits in string.digits:
    for uppers in string.ascii_uppercase:
        name_pool.add(digits + uppers)

asyncio.run(main())
# ec = zip_msg('AAAAB'*1000)
# print(ec)
# unzip_msg(ec)
# dd = {}
