import datetime
import hashlib
import json
import traceback
import aiohttp
import os
from fastapi.param_functions import Form
import magic
from fapi.models.FileStorage import *
import fapi.G
import fastapi
from fastapi import APIRouter, Depends, HTTPException, Request, Response, File, UploadFile
from typing import Optional
from pydantic import BaseModel
from cfg import *

from passlib.context import CryptContext
from fapi.models.Auth import *
from fapi import encrypt, trueReturn, falseReturn
import time

import asyncio
convert_route = APIRouter(
    prefix="/convert",
    tags=["convert - 公用媒体转换器"],
)

import platform

from basicutils.media import *

manager = Adapter.objects(
    username='file_manager'
).first()

def nolimitAudioSize(src) -> str:
    dst = generateTmpFileName(ext='.amr')
    if src[-3:] == "mid" and platform.system() != 'Windows':
        os.system(f'timidity {src} -Ow -o - | ffmpeg -y -i - -codec amr_nb -ac 1 -ar 8000 {dst}')
    else:
        os.system(f'ffmpeg -y -i {src} -codec amr_nb -ac 1 -ar 8000 {dst}')
    # asyncio.ensure_future(rmTmpFile(dst))
    return dst

def limitAudioSizeByBitrate(src) -> str:
    """依赖ffmpeg，生成一个临时文件，全 损 音 质"""
    # lim = 8 * 1024 # 即1MB，大于1M发不出去
    lim = 8000
    dst = generateTmpFileName(ext='.amr')
    dur = os.popen(f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {src}').read()
    dur = float(dur)
    print(dur)
    if src[-3:] == "mid" and platform.system() != 'Windows':
        os.system(f'timidity {src} -Ow -o - | ffmpeg -y -i - -codec amr_nb -ac 1 -ar 8000 -b:a {lim / dur}k {dst}')
    else:
        os.system(f'ffmpeg -y -i {src} -codec amr_nb -ac 1 -ar 8000 -b:a {lim / dur}k {dst}')
    # asyncio.ensure_future(rmTmpFile(dst))
    return dst

def limitAudioSizeByCut(src) -> str:
    """超出部分会被剪掉"""
    dst = generateTmpFileName(ext='.amr')
    if src[-3:] == "mid" and platform.system() != 'Windows':
        os.system(f'timidity {src} -Ow -o - | ffmpeg -y - -codec amr_nb -ac 1 -ar 8000 -fs 1000K {dst}')
    else:
        os.system(f'ffmpeg -y -i {src} -codec amr_nb -ac 1 -ar 8000 -fs 1000K {dst}')
    # asyncio.ensure_future(rmTmpFile(dst))
    return dst

import base64
@convert_route.post('/amr')
async def to_amr(mode: int = 0, f: Optional[UploadFile] = fastapi.File(None), lnk: Optional[str]=Form(''), b64: Optional[str] = Form('')):
    """
    format:

        ffmpeg需要根据传入的扩展名确定源格式，一般是三个小写字母
        
    mode:

        0: 不裁剪

        1: 限制质量

        2: 限制长度"""
    fname = f'tmp{datetime.datetime.now().timestamp()}'
    with open(fname, 'wb') as fi:
        if lnk:
            ses = aiohttp.ClientSession()
            async with ses.get(lnk) as resp:
                fi.write(await resp.content.read())
        elif b64:
            fi.write(base64.b64decode(b64))
        else:
            fi.write(await f.read())
    try:
        typ = magic.from_file(fname, mime=True)
        logger.debug(magic.from_file(fname))
        logger.debug(magic.from_file(fname, mime=True))
        
        if typ == 'application/octet-stream':
            fn = fname + '.amr'
            os.rename(fname, fn)
            ret = fn
            fname = fn
        else:
            fn = fname + '.' + typ.split('/')[1]
            os.rename(fname, fn)
            fname = fn
            ret = [
                nolimitAudioSize,
                limitAudioSizeByBitrate,
                limitAudioSizeByCut
            ][mode](fname)
        with open(ret, 'rb') as fi:
            t = TempFile(
                adapter=manager,
                filename=ret,
                content_type='audio/AMR',
                expires=datetime.datetime.now()+datetime.timedelta(seconds=30)
            )
            t.content.put(fi)
            t.save()
            asyncio.ensure_future(t.deleter())
        os.remove(fname)
        os.remove(ret)
        return {'url': str(t.pk)}
    except:
        os.remove(fname)
        try:
            os.remove(ret)
        except:
            pass
        return traceback.format_exc()
        
