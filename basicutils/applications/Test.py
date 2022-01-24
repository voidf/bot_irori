"""测试类（开发用"""
from basicutils.database import Sniffer
from basicutils.task import server_api
import os
import sys
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
import basicutils.CONST as GLOBAL
import asyncio
from basicutils.network import *
from basicutils.chain import *


async def 表情符号查询姬(*attrs,kwargs={}):
    return [Plain(' '.join( [str(ord(i)) for i in ' '.join(attrs)] ))]

async def Unicode测试姬(*attrs,kwargs={}):
    s = int(attrs[0])
    e = int(attrs[1])
    s,e = min(s,e),max(s,e)
    w = ' '.join(attrs[2:])
    asyncio.ensure_future(fuzzT(kwargs['gp'],s,e,w))

def 乒乓球(ent: CoreEntity):
    """#ping []
    用来测试bot有没有在线
    """
    if GLOBAL.pingCtr==0:
        s = 'pong'
    else:
        s = f'pong - {GLOBAL.pingCtr}'
    GLOBAL.pingCtr+=1
    return [Plain(s)]

async def 废话生成器(*attrs,kwargs={}): return [Plain(' '.join(attrs[:-1])*int(attrs[-1]))]


async def 清空嗅探器(ent: CoreEntity):
    """%clear []
    清空所有本会话Sniffer
    """
    return [Plain(Sniffer.drop(ent.pid))]

import requests
def 音乐测试(ent: CoreEntity):
    """#mu []
    测试Voice或者转码工不工作
    """
    # loop = asyncio.get_running_loop()
    # voi = loop.run_until_complete(GLOBAL.app.uploadVoice(getFileBytes('Assets/wf.amr')))
    # voi = getFileBytes('Assets/wf.amr')
    # return [voi]
    ret = requests.post(
        server_api('/convert/amr?format=mp3&mode=0'),
        data={'lnk': 'http://127.0.0.1:8000/download/6145599b94aa42fdbe423c93'}
    ).json()['url']
    return [Voice(url=server_api('/worker/oss/'+ret))]


functionMap = {
    '#fuzz':Unicode测试姬,
    '#ping':乒乓球,
    '#废话':废话生成器,
    '#echo':表情符号查询姬,
}

shortMap = {

}

functionDescript = {
    '#fuzz':
"""
【测试用】基本上是用来测试unicode的
用法：
    #fuzz <起始unicode码> <终止unicode码> <额外输出字符>
""",
    '#lim':'设置返回的消息长度大于等于多少时,转换为图片发送',
    '#echo':'查询当前字符串的unicode码',
    '#ping':'',
    '#废话':'【测试用】复读某个字符串，一开始是为测量消息最大长度而设计，目前已知私聊字符串最大长度876，群聊32767.用法#废话 <复读字符串> <复读次数>',
}
