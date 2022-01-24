from fapi.Sessions import SessionManager
import hashlib
from fapi.webcfg import salt, jwt_key
from fapi.models.Auth import *
from jose import jwt
from basicutils.chain import *
from basicutils.network import *
import os
from typing import Union
from loguru import logger
from basicutils.task import ArgumentParser
from typing import Union
import asyncio
import traceback


# @logger.catch
# def announcement(msg: Union[str, CoreEntity], ignored=[]):
#     if isinstance(msg, str):
#         ent = CoreEntity.wrap_rawstring(msg)
#     elif isinstance(msg, CoreEntity):
#         ent = msg
#     else:
#         raise TypeError('广播消息类型错误')
#     for k, v in fapi.G.adapters.items():
#         if str(k) not in ignored:
#             # logger.debug('k: {}, ignored: {}', k, ignored)
#             asyncio.ensure_future(v.send(ent))

# 管理员函数族
async def sys_exec(ent: CoreEntity, args: list): return f"""{exec(' '.join(args))}"""
async def sys_eval(ent: CoreEntity, args: list): return f"""{eval(' '.join(args))}"""
async def sys_run(ent: CoreEntity, args: list): return f"""{os.popen(' '.join(args)).read()}"""
async def sys_help(ent: CoreEntity, args: list): return '目前仅支持exec, eval, run, send四个命令'
async def sys_unauthorized(ent: CoreEntity, args: list): return "您没有权限执行此调用"
# async def sys_announcement(ent: CoreEntity, args: list): 
    # announcement(' '.join(args), [ent.source])
    # return '广播成功'
# async def sys_sendp(ent: CoreEntity, args: list):
#     # await websocket.send(' '.join(args))
#     ap = ArgumentParser('send')
#     ap.add_argument('target', type=str, help='送往对象player号，若是QQ应该是一个整数')
#     ap.add_argument('content', type=str, help='消息内容')
#     try:
#         pap = ap.parse_args(args)
#     except Exception as e:
#         return '发送失败：' + str(e) + ap.format_help()
#     if pap.target not in player_adapter:
#         return '找不到player对应的adapter'
#     else:
#         sendto: QUICServerSession = adapters[player_adapter[pap.target]]
#         ent.chain = MessageChain.auto_make(pap.content)
#         await sendto.send(ent) # 保证送出去的还是CoreEntity
#         return '发送成功'
# async def sys_sends(ent: CoreEntity, args: list):
#     # await websocket.send(' '.join(args))
#     ap = ArgumentParser('send')
#     ap.add_argument('target', type=str, help='送往对象终端号(syncid)')
#     ap.add_argument('content', type=str, help='消息内容')
#     try:
#         pap = ap.parse_args(args)
#     except Exception as e:
#         return '发送失败：' + str(e) + ap.format_help()
#     if pap.target not in adapters:
#         return '找不到syncid对应的adapter'
#     else:
#         sendto: QUICServerSession = adapters[pap.target]
#         ent.chain = MessageChain.auto_make(pap.content)
#         await sendto.send(ent) # 保证送出去的还是CoreEntity
#         return '发送成功'

def encrypt(s: str) -> str:
    return hashlib.sha256((s + salt).encode('utf-8')).hexdigest()

def generate_login_jwt(expires: float=86400):
    return jwt.encode(
        {
            'ts': str((datetime.datetime.now()+ datetime.timedelta(seconds=expires)).timestamp())
        },  # payload, 有效载体
        jwt_key,  # 进行加密签名的密钥
    )

def generate_player_jwt(pid: str):
    return jwt.encode(
        {
            'pid': pid,
            'ts': str(datetime.datetime.now().timestamp())
        },  # payload, 有效载体
        jwt_key,  # 进行加密签名的密钥
    )

def generate_session_jwt(sid: int, expire_seconds: float = 120.0):
    token_dict = {
        'sid': sid,
        'ts': str((datetime.datetime.now()+ datetime.timedelta(seconds=expire_seconds)).timestamp())
    }
    return jwt.encode(
        token_dict,  # payload, 有效载体
        jwt_key,  # 进行加密签名的密钥
    )

# def generate_adapter_jwt(adapter: Union[Adapter, str], expire_seconds: float = 120.0):
#     token_dict = {
#         'aid': str(adapter.pk) if isinstance(adapter, Adapter) else adapter,
#         'ts': str((datetime.datetime.now()+ datetime.timedelta(seconds=expire_seconds)).timestamp())
#     }
#     return jwt.encode(
#         token_dict,  # payload, 有效载体
#         jwt_key,  # 进行加密签名的密钥
#     )

# def verify_adapter_jwt(token):
#     try:
#         payload = jwt.decode(token, jwt_key)
#         if datetime.datetime.now().timestamp() > float(payload['ts']):
#             return None, "令牌过期"
#         adapter = Adapter.objects(pk=payload['aid']).first()
#         if not adapter:
#             return None, "无此用户"
#         return adapter, ""
#     except:
#         traceback.print_exc()
#         return None, "数据错误"

def verify_session_jwt(token):
    try:
        payload = jwt.decode(token, jwt_key)
        if datetime.datetime.now().timestamp() > float(payload['ts']):
            return None, "令牌过期"
        session = payload['sid']
        if session not in SessionManager.s:
            return None, "无此会话"
        return session, ""
    except:
        logger.critical(traceback.format_exc())
        return None, "非预期错误"

def verify_login_jwt(token):
    try:
        payload = jwt.decode(token, jwt_key)
        if datetime.datetime.now().timestamp() > float(payload['ts']):
            return None, "令牌过期"
        return True, ""
    except:
        logger.critical(traceback.format_exc())
        return None, "非预期错误"




# def verify_jwt():pass
def trueReturn(data=None, msg=""):
    return {
        'data': data,
        'msg': msg,
        'status': True
    }

from fastapi import HTTPException

def falseReturn(code=500, msg="", data=None):
    raise HTTPException(code, {
        'data': data,
        'msg': msg,
        'status': False
    })