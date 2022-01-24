import fapi.G

from fastapi import APIRouter, Depends, HTTPException, Request, Response, File, UploadFile, Form

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel
from cfg import *

from fapi.models.Auth import *
from fapi.Sessions import SessionManager
from fapi import generate_login_jwt, trueReturn, falseReturn, verify_login_jwt

from fapi.MiraiSession import MiraiSession
import asyncio
auth_route = APIRouter(
    prefix="/auth",
    tags=["auth"],
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


async def connect_mirai(miraiwsurl: str) -> int:
    # await try_close_session(a)
    # await Routiner.recover_routiners()
    # if not fapi.G.initialized:
        # await TempFile.resume()
        # fapi.G.initialized = True
    return SessionManager.new(MiraiSession, miraiwsurl)


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
async def login_auth(f: OAuth2PasswordRequestForm = Depends()):
    tk = f.username if f.username else f.password
    if tk != IroriUUID.get().uuid:
        return falseReturn(401, '口令错误')

    # await Routiner.recover_routiners(a)

    # if not fapi.G.initialized:
        # await TempFile.resume()
        # fapi.G.initialized = True
        # 一次启动上下文

    # ml = MiraiSession(f.username)
    # fapi.G.adapters[f.username] = ml
    # asyncio.ensure_future(ml.enter_loop(f.miraiwsurl))
    tk = generate_login_jwt(86400)
    return {"access_token": tk, "token_type": "bearer"}


class register_form(BaseModel):
    username: str
    password: str

# @auth_route.post('/register')
# async def register_auth(f: register_form):
#     if Adapter.objects(username=f.username):
#         return falseReturn(401, '用户名已被占用')
#     else:
#         a=Adapter(
#             username=f.username,
#             password=encrypt(f.password),
#             role=Role.objects(name='guest').first()
#         ).save()
#         tk = generate_adapter_jwt(a, 86400)
#         return {"access_token": tk, "token_type": "bearer"}


o2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


@auth_route.delete('/logout')
async def logout_session(tk: str = Depends(o2_scheme), session_id: int = Form(...)):
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
    # await Routiner.recover_routiners(a)
    # if not fapi.G.initialized:
    #     await TempFile.resume()
    #     fapi.G.initialized = True
