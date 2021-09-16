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

from basicutils.network import *
from basicutils.chain import *
from fapi.Sessions import MiraiSession
from fapi.models.Routinuer import *

worker_route = APIRouter(
    prefix="/worker",
    tags=["worker"],
)


from fapi import verify_jwt
from loguru import logger
from typing import Tuple
class CoreEntityJson(BaseModel):
    ents: str

async def parse_adapter_jwt(f: CoreEntityJson) -> Tuple[CoreEntity, Adapter]:
    logger.critical(f)
    ent = CoreEntity.handle_json(f.ents)
    src, msg = verify_jwt(ent.source)
    if not src:
        return falseReturn(401, msg)
    ent.source = src.pk
    return ent, src

    

@worker_route.post('/submit')
async def submit_worker(tp: Tuple[CoreEntity, Adapter] = Depends(parse_adapter_jwt)):
    ent, src = tp
    await fapi.G.adapters[src.pk].upload(ent)
    return trueReturn()

from fapi.models.FileStorage import FileStorage, TempFile
@worker_route.post('/oss')
async def upload_oss(f: UploadFile, delays: Optional[int]=-1, tp: Tuple[CoreEntity, Adapter] = Depends(parse_adapter_jwt)):
    ent, src = tp
    if delays>=0:
        fs = TempFile(
            adapter=src,
            filename=f.filename,
            content_type=f.content_type,
            expires=datetime.datetime.now()+datetime.timedelta(seconds=delays)
        )
        asyncio.ensure_future(fs.deleter())
    else:
        fs = FileStorage(
            adapter=src,
            filename=f.filename,
            content_type=f.content_type
        )
    fs.content.put(f.file)
    fs.save()
    return {'url': str(fs.pk)}

@worker_route.get('/oss/{fspk}')
async def download_oss(fspk: str):
    fs: FileStorage = FileStorage.trychk(fspk)
    
    if not fs:
        return falseReturn(404, 'No such resource')
    else:
        return Response(fs.content.read(), media_type=fs.content_type)

@worker_route.delete('/oss/{fspk}')
async def delete_oss(fspk: str, tp: Tuple[CoreEntity, Adapter] = Depends(parse_adapter_jwt)):
    ent, src = tp
    fs: FileStorage = FileStorage.trychk(fspk)
    if not fs:
        return falseReturn(404, 'No such resource')
    if fs.adapter == src or 'oss_A' in src.role.allow or 'A' in src.role.allow:
        fs.delete()
        return trueReturn()
    else:
        return falseReturn(403, 'Not permitted')
    

async def resolve_routiner(tp: Tuple[CoreEntity, Adapter] = Depends(parse_adapter_jwt)) -> Tuple[CoreEntity, Adapter, str, Routiner]:
    ent, src = tp
    return ent, src, str(ent.player), fapi.models.Routinuer.routiner_namemap[ent.meta.get('routiner')]

@worker_route.post('/routiner')
async def create_routine(tp: Tuple[CoreEntity, Adapter, str, Routiner] = Depends(resolve_routiner)):
    """创建日程器"""
    ent, src, pid, R = tp
    # pid = str(ent.player)
    # R = ent.meta.get('routiner')
    res = await R.add(ent)
    ent.chain = MessageChain.auto_make(f'【订阅器】{R}创建成功')
    await fapi.G.adapters[src.pk].upload(ent)
    return {'res': res}

@worker_route.delete('/routiner')
async def delete_routine(tp: Tuple[CoreEntity, Adapter, str, Routiner] = Depends(resolve_routiner)):
    """销毁日程器（取消订阅）"""
    ent, src, pid, R = tp
    res = await R.cancel(ent)
    ent.chain = MessageChain.auto_make(f'【订阅器】{R}删除成功')
    await fapi.G.adapters[src.pk].upload(ent)
    return {'res': res}

@worker_route.options('/routiner')
async def options_routine(tp: Tuple[CoreEntity, Adapter, str, Routiner] = Depends(resolve_routiner)):
    """调用日程器的内部功能"""
    ent, src, pid, R = tp
    F = ent.meta.get('call')
    logger.info(F)
    logger.info(R)
    logger.info(R.call_map)
    # ent.meta['aid'] = str(src)
    # ent.meta['pid'] = str(ent.player)
    if hasattr(R, 'call_map') and F in R.call_map:
        res = await R.call_map[F](ent)
        logger.debug(f'return: {res}')
        return {'res': res}
    return falseReturn(404, "No such method")

