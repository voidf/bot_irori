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



def sub_task(taskstr: str, writer: asyncio.StreamWriter):
    import os
    import importlib
    import inspect
    import re

    task: TaskMessage = TaskMessage.parse_raw(taskstr)

    app_dir = 'applications'
    app_doc = {}
    app_fun = {}
    tot_funcs = {}
    tot_alias = {}

    async def printHelp(chain: MessageChain, meta: dict = {}):
        """不传参打印命令表，传参则解释命令"""
        kwargs = meta
        attrs = chain.onlyplain().split(' ')
        show_limit = int(kwargs.get('-showlim', 20))
        l = []
        img = []
        ext = []
        if not attrs:
            l.append('已导入的模块：')
            for k, v in app_doc.items():
                l.append(f'''\t{k} {v}''')
            l.append('''输入#h <模块名> 以查询模块下命令
    使用#h <命令名> 可以查询详细用法
    使用#h search <关键字> 可以按照关键字查找相关命令
    尖括号表示参数必要，方括号表示参数可选，实际使用中不必一定需要
    使用#h #abb可以查询缩写表

    通用选项：
        --fi --force-image 强制把文本消息转换成图片发送
        --paste 强制把文本消息粘贴至ubuntu pastebin
        --tts 【试验阶段】强制把消息转换成语音发送
        --voice 【试验阶段】如果命令支持的话，发送语音消息''')
        else:
            if attrs[0] in tot_alias:
                attrs = [tot_alias[attrs[0]],*attrs[1:]]
            if attrs[0] in tot_funcs:
                l.append(tot_funcs[attrs[0]].__doc__)
            elif attrs[0] == '#abb':
                l.append(f'可用缩写表:{tot_alias}')
            # elif attrs[0] in ('all', 'old'):
            #     l.append('可用命令表：')
            #     for k in tot_funcs:
            #         l.append('\t'+k)
            #     l.append('使用#h 命令名（带井号）可以查询详细用法')
            #     l.append('使用#h #abb可以查询缩写表')
            #     l.append('注命令后需打空格，之后的参数如存在空格即以空格分开多个参数，如#qr 1 1 4 5 1 4')
            #     img.append(generateImageFromFile('Assets/muzukashi.png'))
            elif attrs[0] in app_fun:
                l.append(f'分类：{attrs[0]}')
                for k, v in app_fun[attrs[0]].items():
                    print(f'descLen = {len(v.__doc__.strip()[:show_limit])}')
                    l.append(f'''\t{k}\t{v.__doc__.strip()[:show_limit]
                    if len(v.__doc__.strip()[:show_limit])<=show_limit
                    else v.__doc__.strip()[:show_limit]+'...'}\n''' )
            elif attrs[0] == "search" and len(attrs) > 1:
                key = attrs[1]
                checked = set()
                for k, v in tot_funcs.items():
                    if re.search(key, k, re.S) or re.search(key, v.__doc__, re.S):
                        l.append(f'''\t{k}\t{v.__doc__.strip()}\n''' )
                if not l:
                    l = ["没有结果喵"]
            else:
                l.append('【错误】参数不合法\n')
                ext = await printHelp(MessageChain())
            
        return [Plain('\n'.join(l))] + img + ext

    for applications in os.listdir(app_dir):
        pkgname = os.path.splitext(applications)[0]
        if pkgname == '__pycache__': continue
        module = importlib.import_module(app_dir+'.'+pkgname)
        importlib.reload(module)
        names = module.__dict__.get("__all__", [x for x in module.__dict__ if x[:1] != '_'])
        globals().update({k: getattr(module, k) for k in names})

        funcs = {}
        alias = {}
        helps = {}

        for n, f in inspect.getmembers(module): # 判断这是个可以加进QQ消息调用表的函数
            if not inspect.isbuiltin(f):
                argsinfo = inspect.getfullargspec(f)
                if argsinfo.args == ['chain', 'meta']:
                    header, f.__doc__ = f.__doc__.split('\n', 1)
                    fname, ato = header.split(' ', 1)
                    funcs.update({fname: f})
                    L, R = ato.index('['), ato.rindex(']')

                    for ss in ato[L+1:R].split(','):
                        ss = ss.strip()
                        if not ss: continue
                        if ss not in alias and ss not in funcs:
                            alias.update({ss: fname})
                    helps[fname] = f.__doc__
        app_fun[pkgname] = funcs
        app_doc[pkgname] = module.__doc__
        tot_funcs.update(funcs)
        tot_alias.update(alias)

    tot_funcs['#h'] = printHelp

    cmd = task.chain.pop_first_cmd()
    cmd = tot_alias.get(cmd, cmd)
    if cmd in tot_funcs:
        reply = asyncio.run(tot_funcs[cmd](task.chain, task.meta))
        if not reply:
            return
        if isinstance(reply, str):
            reply = MessageChain(__root__=[Plain(reply)])
        if isinstance(reply, Plain):
            reply = MessageChain(__root__=[reply])

    

import concurrent.futures
import datetime
import traceback
from socketutils import *
# from multiprocessing.dummy import Pool as Pool2
# def task_monitor(taskstr: str, writer: asyncio.StreamWriter):
#     task: TaskMessage = TaskMessage.parse_raw(taskstr)
#     rawstr = task.chain.onlyplain()
#     cmd, argstr = rawstr.split(' ', 1) 
    
#     tle = task.meta.get('tle', 30)
#     task.meta['writer'] = writer

#     p = Pool2(1)

    


#     res = p.apply_async(func, args=args)
#     try:
#         out = res.get(tle)
#         return out
#     except:
#         traceback.print_exc()
#         msg = '执行超时'
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
                async def clear_pool(delay: float):
                    await asyncio.sleep(delay)
                    for k, v in pool._processes.items():
                        v.kill()
                        v.join()

                async def assign_task_loop():
                    while 1:
                        rawtask = await ses.recv_task()
                        asyncio.ensure_future(clear_pool(30))
                        result = await loop.run_in_executor(
                            pool, functools.partial(
                                sub_task, rawtask.decode('utf-8'),
                                ses._writer
                            )
                        )
                asyncio.ensure_future(assign_task_loop())
                while 1:
                    cmd = await ses.recv_control()
                    if cmd == b'kill':
                        await clear_pool(0)
                        # pool.shutdown(True)
                        


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    