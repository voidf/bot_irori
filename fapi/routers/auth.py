from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, File, UploadFile, Form

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel
from cfg import *

from fapi.models.Auth import *
from fapi.Sessions import SessionManager

from fapi.utils.jwt import *

import asyncio
auth_route = APIRouter(
    prefix="/auth",
    tags=["auth - 网页后台接口"],
)


class login_form(BaseModel):
    username: str
    password: str
    miraiwsurl: str

# async def try_clear_adapter(a: Adapter):
#     if a.username in fapi.G.adapters:
#         await fapi.G.adapters[a.username].close()
#         return True
#     else:
#         return False

import fapi.MiraiSession
#from fapi.MiraiSession import *
async def connect_mirai(miraiwsurl: str) -> int:
    return (await SessionManager.new(fapi.MiraiSession.MiraiSession, miraiwsurl))


# @auth_route.post('/legacy')
# async def legacy_auth(f: login_form):
    # a = Adapter.objects(username=f.username).first()
    # if not a:
    # return falseReturn(401, '用户名或密码错误')

    # await Routiner.recover_routiners(a)

    # if not fapi.G.initialized:
    # await TempFile.resume()
    # fapi.G.initialized = True
    # 一次启动上下文

    # if not encrypt(f.password) == a.password:
    #     return falseReturn(401, '用户名或密码错误')

    # sessionid = await connect_mirai(a, f.miraiwsurl)
    # tk = generate_adapter_jwt(a, 86400)
    # return {"access_token": tk, "token_type": "bearer", "session_id": sessionid}


@auth_route.post('/login')
async def login_auth(rsp: Response, f: OAuth2PasswordRequestForm = Depends(),):
    """使用uuid口令连入，获取令牌，用户名和密码都贴上令牌即可"""
    tk = f.username if f.username else f.password
    if tk != IroriUUID.get().uuid:
        return falseReturn(401, '口令错误')

    tk = generate_login_jwt(86400)
    rsp.set_cookie("Authorization", tk, 86400)
    return {"access_token": tk, "token_type": "bearer"}


class register_form(BaseModel):
    username: str
    password: str

o2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


@auth_route.delete('/logout')
async def logout_session(tk: str = Depends(o2_scheme), session_id: int = Form(...)):
    """注销一个session"""
    a, msg = verify_login_jwt(tk)
    if not a:
        return falseReturn(401, msg)

    return trueReturn(data={'isclose': SessionManager.close(session_id)})


@auth_route.post('/mirai')
async def mirai_login(tk: str = Depends(o2_scheme), miraiwsurl: str = Form(...)):
    a, msg = verify_login_jwt(tk)
    if not a:
        return falseReturn(401, msg)
    await connect_mirai(miraiwsurl)
    return trueReturn()

from fapi.WebsocketSession import *
from fastapi import WebSocket
from fastapi import status
@auth_route.websocket('/ws')
async def ws_connectin(websocket: WebSocket, player_token: str, typ: str='json'):
    """
    player_token: player对应的口令，可以通过bot申请
    typ: 欲创建的ws连接种类，仅提供json和plain两种
    """
    p, msg = verify_player_jwt(player_token)
    if not p:
        await websocket.close(status.WS_1008_POLICY_VIOLATION)
    if typ == 'json':
        await SessionManager.new(WebsocketSessionJson, websocket, p.pid)
    elif typ == 'plain':
        await SessionManager.new(WebsocketSessionPlain, websocket, p.pid)
    else:
        await websocket.close(status.WS_1008_POLICY_VIOLATION)

    
