import datetime
import hashlib
import json
import traceback
import fapi.G

from fastapi import APIRouter, Depends, HTTPException, Request, Response, File, UploadFile
from typing import Optional
from pydantic import BaseModel
from cfg import *

from jose import jwt, JWTError
from passlib.context import CryptContext
from fapi.models.Auth import *
from fapi import encrypt, trueReturn, falseReturn
import time

from basicutils.socketutils import CoreEntity
from fapi.Sessions import MiraiSession
import asyncio

worker_route = APIRouter(
    prefix="/worker",
    tags=["worker"],
)


from fapi import verify_jwt
from loguru import logger

class CoreEntityJson(BaseModel):
    ents: str
@worker_route.post('/submit')
async def login_auth(f: CoreEntityJson):
    logger.critical(f)
    ent = CoreEntity.handle_json(f.ents)
    src, msg = verify_jwt(ent.source)
    if not src:
        return falseReturn(400, msg)
    await fapi.G.adapters[src.pk].upload(ent)
    return trueReturn()

