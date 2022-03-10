import datetime
import traceback
import aiohttp
import os
from fastapi.param_functions import Form
import magic
from fapi.models.FileStorage import *
import fastapi
from fastapi import APIRouter, Depends, HTTPException, Request, Response, File, UploadFile
from typing import Optional
from cfg import *
from loguru import logger
from fapi.models.Auth import *

import asyncio
convert_route = APIRouter(
    prefix="/convert",
    tags=["convert - 公用媒体转换器"],
)




import fapi

import base64
@convert_route.post('/amr')
async def convert_to_amr(mode: int = 0, f: Optional[UploadFile] = fastapi.File(None), lnk: Optional[str]=Form(''), b64: Optional[str] = Form('')):
    """
    format:

        ffmpeg需要根据传入的扩展名确定源格式，一般是三个小写字母
        
    mode:

        0: 不裁剪

        1: 限制质量

        2: 限制长度"""
    return await fapi.to_amr(mode, f, lnk, b64)