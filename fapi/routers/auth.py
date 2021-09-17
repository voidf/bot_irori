import datetime
import hashlib
import json
import traceback
import fapi.G

from fastapi import APIRouter, Depends, HTTPException, Request, Response, File, UploadFile
from typing import Optional
from pydantic import BaseModel
from cfg import *

from passlib.context import CryptContext
from fapi.models.Auth import *
from fapi import encrypt, trueReturn, falseReturn
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


@auth_route.post('/login')
async def login_auth(f: login_form):
    a = Adapter.objects(username=f.username).first()
    if not a:
        return falseReturn(401, '用户名不存在')

    await Routiner.recover_routiners(a)

    if not fapi.G.initialized:
        await TempFile.resume()
        fapi.G.initialized = True
        # 一次启动上下文

    if not encrypt(f.password) == a.password:
        return falseReturn(401, '用户名或密码错误')
    ml = MiraiSession(f.username)
    fapi.G.adapters[f.username] = ml
    asyncio.ensure_future(ml.enter_loop(f.miraiwsurl))
    return trueReturn()

class register_form(BaseModel):
    username: str
    password: str

@auth_route.post('/register')
async def register_auth(f: register_form):
    if Adapter.objects(username=f.username):
        return falseReturn(401, '用户名已被占用')
    else:
        Adapter(
            username=f.username, 
            password=encrypt(f.password),
            role=Role.objects(name='guest').first()
        ).save()
        return trueReturn()


