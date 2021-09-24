import datetime
import hashlib
import json
import traceback
import fapi.G
import fastapi
from fastapi import *
# from fastapi import File as fapi_File
from fastapi.responses import *
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
    tags=["worker - 分布式任务执行模块自用，非外部调用接口"],
)


from fapi import verify_jwt
from loguru import logger
from typing import Tuple
class CoreEntityJson(BaseModel):
    ents: str

async def parse_adapter_jwt(f: CoreEntityJson) -> Tuple[CoreEntity, Adapter]:
    logger.critical(f)
    ent = CoreEntity.handle_json(f.ents)
    src, msg = verify_jwt(ent.jwt)
    ent.jwt = ''
    if not src:
        return falseReturn(401, msg)
    ent.source = src.pk
    return ent, src

    

@worker_route.post('/submit')
async def submit_worker(tp: Tuple[CoreEntity, Adapter] = Depends(parse_adapter_jwt)):
    ent, src = tp
    await fapi.G.adapters[src.pk].upload(ent)
    return trueReturn()

oss_route = APIRouter(
    prefix="/oss",
    tags=["oss - 内置对象储存模块"],
)

from fapi.models.FileStorage import FileStorage, TempFile

import magic
@oss_route.post('')
async def upload_oss(delays: int = -1, fileobj: UploadFile=fastapi.File(...), ents: str = Form(...)):
    ent, src = await parse_adapter_jwt(CoreEntityJson(ents=ents))
    # delays = ent.get('delays', -1)
    logger.debug('file name: {}', fileobj.filename)
    logger.debug('file type: {}', fileobj.content_type)
    typ = magic.from_buffer(fileobj.file, mime=True)
    fileobj.file.seek(0)
    logger.debug('guessed type: {}', typ)
    if delays>=0:
        fs = TempFile(
            adapter=src,
            filename=fileobj.filename,
            content_type=typ,
            expires=datetime.datetime.now()+datetime.timedelta(seconds=delays)
        )
        asyncio.ensure_future(fs.deleter())
    else:
        fs = FileStorage(
            adapter=src,
            filename=fileobj.filename,
            content_type=typ
        )
    fs.content.put(fileobj.file)
    fs.save()
    return {'url': str(fs.pk)}

@oss_route.get('/{fspk}')
async def download_oss(fspk: str):
    fs: FileStorage = FileStorage.trychk(fspk)
    
    if not fs:
        return falseReturn(404, 'No such resource')
    else:
        return Response(fs.content.read(), media_type=fs.content_type)

@oss_route.delete('/{fspk}')
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

worker_route.include_router(oss_route)

routiner_route = APIRouter(
    prefix="/routiner",
    tags=["routiner - 内置日程器模块"],
)

async def resolve_routiner(tp: Tuple[CoreEntity, Adapter] = Depends(parse_adapter_jwt)) -> Tuple[CoreEntity, Adapter, str, Routiner]:
    ent, src = tp
    return ent, src, str(ent.player), fapi.models.Routinuer.routiner_namemap[ent.meta.get('routiner')]

@routiner_route.post('')
async def create_routine(tp: Tuple[CoreEntity, Adapter, str, Routiner] = Depends(resolve_routiner)):
    """创建日程器"""
    ent, src, pid, R = tp
    # pid = str(ent.player)
    # R = ent.meta.get('routiner')
    res = await R.add(ent)
    ent.chain = MessageChain.auto_make(f'【订阅器】{R}创建成功')
    await fapi.G.adapters[src.pk].upload(ent)
    return {'res': res}

@routiner_route.delete('')
async def delete_routine(tp: Tuple[CoreEntity, Adapter, str, Routiner] = Depends(resolve_routiner)):
    """销毁日程器（取消订阅）"""
    ent, src, pid, R = tp
    res = await R.cancel(ent)
    ent.chain = MessageChain.auto_make(f'【订阅器】{R}删除成功')
    await fapi.G.adapters[src.pk].upload(ent)
    return {'res': res}

@routiner_route.options('')
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

worker_route.include_router(routiner_route)