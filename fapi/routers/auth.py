import datetime
import hashlib
import json
import traceback
import fapi.G

from fastapi import APIRouter, Depends, HTTPException, Request, Response, File, UploadFile, Form

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Optional
from pydantic import BaseModel
from cfg import *

from fapi.models.Auth import *
from fapi import encrypt, generate_jwt, trueReturn, falseReturn, verify_jwt
import time

from fapi.Sessions import MiraiSession
import asyncio
import fapi.G
auth_route = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

from fapi.models.Routinuer import *
from fapi.models.FileStorage import *
class login_form(BaseModel):
    username: str
    password: str
    miraiwsurl: str

async def try_close_session(a: Adapter):
    if a.username in fapi.G.adapters:
        await fapi.G.adapters[a.username].close()
        return True
    else:
        return False

async def connect_mirai(a: Adapter, miraiwsurl: str):
    await try_close_session(a)
    await Routiner.recover_routiners(a)
    if not fapi.G.initialized:
        await TempFile.resume()
        fapi.G.initialized = True
    ml = MiraiSession(a.username)
    fapi.G.adapters[a.username] = ml
    asyncio.ensure_future(ml.enter_loop(miraiwsurl))

@auth_route.post('/legacy')
async def legacy_auth(f: login_form):
    a = Adapter.objects(username=f.username).first()
    if not a:
        return falseReturn(401, '用户名或密码错误')

    # await Routiner.recover_routiners(a)

    # if not fapi.G.initialized:
        # await TempFile.resume()
        # fapi.G.initialized = True
        # 一次启动上下文

    if not encrypt(f.password) == a.password:
        return falseReturn(401, '用户名或密码错误')
    
    await connect_mirai(a, f.miraiwsurl)
    # ml = MiraiSession(f.username)
    # fapi.G.adapters[f.username] = ml
    # asyncio.ensure_future(ml.enter_loop(f.miraiwsurl))
    tk = generate_jwt(a, 86400)
    return {"access_token": tk, "token_type": "bearer"}


@auth_route.post('/login')
async def login_auth(f: OAuth2PasswordRequestForm = Depends()):
    a = Adapter.objects(username=f.username).first()
    if not a:
        return falseReturn(401, '用户名或密码错误')

    # await Routiner.recover_routiners(a)

    # if not fapi.G.initialized:
        # await TempFile.resume()
        # fapi.G.initialized = True
        # 一次启动上下文

    if not encrypt(f.password) == a.password:
        return falseReturn(401, '用户名或密码错误')
    # ml = MiraiSession(f.username)
    # fapi.G.adapters[f.username] = ml
    # asyncio.ensure_future(ml.enter_loop(f.miraiwsurl))
    tk = generate_jwt(a, 86400)
    return {"access_token": tk, "token_type": "bearer"}

class register_form(BaseModel):
    username: str
    password: str

@auth_route.post('/register')
async def register_auth(f: register_form):
    if Adapter.objects(username=f.username):
        return falseReturn(401, '用户名已被占用')
    else:
        a=Adapter(
            username=f.username, 
            password=encrypt(f.password),
            role=Role.objects(name='guest').first()
        ).save()
        tk = generate_jwt(a, 86400)
        return {"access_token": tk, "token_type": "bearer"}


o2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
@auth_route.delete('/logout')
async def logout_session(tk: str = Depends(o2_scheme)):
    a, msg = verify_jwt(tk)
    if not a:
        return falseReturn(401, msg)
    await try_close_session(a)
    return trueReturn()

@auth_route.post('/mirai')
async def mirai_login(tk: str = Depends(o2_scheme), miraiwsurl: str = Form(...)):
    a, msg = verify_jwt(tk)
    if not a:
        return falseReturn(401, msg)
    await connect_mirai(a, miraiwsurl)
    return trueReturn()
    # await Routiner.recover_routiners(a)
    # if not fapi.G.initialized:
    #     await TempFile.resume()
    #     fapi.G.initialized = True