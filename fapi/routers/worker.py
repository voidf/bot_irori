import magic
from fapi.models.FileStorage import FileStorage, TempFile
from typing import Tuple
from loguru import logger
from fapi import verify_session_jwt
import datetime
import fapi.G
import fastapi
from fastapi import *
# from fastapi import File as fapi_File
from fastapi.responses import *
from pydantic import BaseModel
from cfg import *

from fapi.models.Auth import *
from fapi import trueReturn, falseReturn

from basicutils.network import *
from basicutils.chain import *
from fapi.models.Routinuer import *

worker_route = APIRouter(
    prefix="/worker",
    tags=["worker - 分布式任务执行模块自用，非外部调用接口"],
)


class CoreEntityJson(BaseModel):
    ents: str


async def parse_session_jwt(f: CoreEntityJson) -> CoreEntity:
    logger.critical(f)
    ent = CoreEntity.handle_json(f.ents)
    # logger.debug(ent)
    src, msg = verify_session_jwt(ent.jwt)
    ent.jwt = ''
    if not src:
        return falseReturn(401, msg)
    ent.source = src
    return ent


@worker_route.post('/submit')
async def submit_worker(ent: CoreEntity = Depends(parse_session_jwt)):
    await SessionManager.get(ent.source).upload(ent)
    return trueReturn()

oss_route = APIRouter(
    prefix="/oss",
    tags=["oss - 内置对象储存模块"],
)


@oss_route.post('')
async def upload_oss(delays: int = -1, fileobj: UploadFile = fastapi.File(...), ents: str = Form(...)):
    ent: CoreEntity = await parse_session_jwt(CoreEntityJson(ents=ents))
    # delays = ent.get('delays', -1)
    logger.debug('file name: {}', fileobj.filename)
    logger.debug('file type: {}', fileobj.content_type)
    # buf = BytesIO(fileobj.file.read())
    # magic.from_descriptor(fileobj.file.fileno())
    typ = magic.from_descriptor(fileobj.file.fileno(), mime=True)
    fileobj.file.seek(0)
    logger.debug('guessed type: {}', typ)
    if delays >= 0:
        fs = TempFile(
            filename=fileobj.filename,
            content_type=typ,
            expires=datetime.datetime.now()+datetime.timedelta(seconds=delays)
        )
        asyncio.ensure_future(fs.deleter())
    else:
        fs = FileStorage(
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
async def delete_oss(fspk: str, ent: CoreEntity = Depends(parse_session_jwt)):
    fs: FileStorage = FileStorage.trychk(fspk)
    if not fs:
        return falseReturn(404, 'No such resource')
    fs.delete()
    return trueReturn()

worker_route.include_router(oss_route)

routiner_route = APIRouter(
    prefix="/routiner",
    tags=["routiner - 内置日程器模块"],
)


async def resolve_routiner(ent: CoreEntity = Depends(parse_session_jwt)) -> Tuple[CoreEntity, Routiner]:
    return ent, fapi.models.Routinuer.routiner_namemap[ent.meta.get('routiner')]


@routiner_route.post('')
async def create_routine(tp: Tuple[CoreEntity, Routiner] = Depends(resolve_routiner)):
    """创建日程器"""
    ent, R = tp
    # pid = str(ent.player)
    # R = ent.meta.get('routiner')
    res = await R.add(ent)
    ent.chain = MessageChain.auto_make(f'【订阅器】{R}创建成功')
    await SessionManager.autoupload(ent)
    return {'res': res}


@routiner_route.delete('')
async def delete_routine(tp: Tuple[CoreEntity, Routiner] = Depends(resolve_routiner)):
    """销毁日程器（取消订阅）"""
    ent, R = tp
    res = await R.cancel(ent)
    ent.chain = MessageChain.auto_make(f'【订阅器】{R}删除成功')
    await SessionManager.autoupload(ent)
    return {'res': res}


@routiner_route.options('')
async def options_routine(tp: Tuple[CoreEntity, Routiner] = Depends(resolve_routiner)):
    """调用日程器的内部功能"""
    ent, R = tp
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
