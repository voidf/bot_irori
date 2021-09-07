import datetime
import hashlib
import json
import traceback
import logging
import G

from fastapi import APIRouter, Depends, HTTPException, Request, Response, File, UploadFile
from typing import Optional
from pydantic import BaseModel
from cfg import *

from jose import jwt, JWTError
from passlib.context import CryptContext
from models.Auth import *
from fapi import encrypt
import time

auth_route = APIRouter(
    prefix="/auth",
    tags=["auth"],
)



class login_form(BaseModel):
    username: str
    password: str
    miraiwsurl: str


@auth_route.post('/login')
async def login_auth(f: login_form):
    
    return trueReturn()

class register_form(BaseModel):
    username: str
    password: str

async def register_auth(f: register_form):
    if Adapter.objects(username=f.username):
        return HTTPException(401, '用户名已被占用')
    else:
        Adapter(
            username=f.username, 
            password=encrypt(f.password),
            role=Role.objects(name='guest').first()
        ).save()
        return trueReturn()


