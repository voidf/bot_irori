from fapi.webcfg import salt, jwt_key
import hashlib
import datetime
from jose import jwt
import traceback
from loguru import logger
from fapi.models.Player import Player
from typing import *
from fapi.Sessions import *

def encrypt(s: str) -> str:
    return hashlib.sha256((s + salt).encode('utf-8')).hexdigest()

def generate_login_jwt(expires: float=86400):
    return jwt.encode(
        {
            'ts': str((datetime.datetime.now()+ datetime.timedelta(seconds=expires)).timestamp())
        },  # payload, 有效载体
        jwt_key,  # 进行加密签名的密钥
    )
def verify_login_jwt(token):
    try:
        payload = jwt.decode(token, jwt_key)
        if datetime.datetime.now().timestamp() > float(payload['ts']):
            return None, "令牌过期"
        return True, ""
    except:
        logger.critical(traceback.format_exc())
        return None, "非预期错误"

def generate_player_jwt(pid: str):

    return jwt.encode(
        {
            'pid': pid,
            'token': Player.objects(pid=pid).first().items.get('token', ''), 
        },  # payload, 有效载体
        jwt_key,  # 进行加密签名的密钥
    )

def verify_player_jwt(token) -> Tuple[Player, str]:
    try:
        payload = jwt.decode(token, jwt_key)
        plr: Player = Player.objects(pid=payload['pid']).first()
        if not plr:
            return None, "用户不存在"
        if not plr.items.get('token', '') == payload['token']:
            return None, "令牌无效"
        return plr, ""
    except:
        logger.critical(traceback.format_exc())
        return None, "非预期错误"

def generate_session_jwt(sid: int, expire_seconds: float = 120.0):
    token_dict = {
        'sid': sid,
        'ts': str((datetime.datetime.now()+ datetime.timedelta(seconds=expire_seconds)).timestamp())
    }
    return jwt.encode(
        token_dict,  # payload, 有效载体
        jwt_key,  # 进行加密签名的密钥
    )
def verify_session_jwt(token):
    try:
        payload = jwt.decode(token, jwt_key)
        if datetime.datetime.now().timestamp() > float(payload['ts']):
            return None, "令牌过期"
        session = payload['sid']
        if not SessionManager.get(session):
            return None, "无此会话"
        return session, ""
    except:
        logger.critical(traceback.format_exc())
        return None, "非预期错误"

# from fastapi import Request
# async def verify_login_cookie(auth: Request):
#     """验证cookie中的login令牌"""
#     toberaise = HTTPException(400, "数据错误")
#     try:
#         logger.debug(auth.client.host)
#         Authorization = auth.cookies.get('Authorization', None)
#         if Authorization:
#             sta, msg = verify_login_jwt(Authorization)
#             if sta:
#                 return
#             toberaise = HTTPException(401, msg)
#         toberaise = HTTPException(401, "没有令牌")
#     except:
#         logger.critical(traceback.format_exc())
#     raise toberaise


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


