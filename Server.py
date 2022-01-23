from fapi.models.FileStorage import *
from fapi.models.Routinuer import *
from fastapi import FastAPI, Depends
from loguru import logger
from cfg import db, web_host, web_port

from fapi.models.Auth import *
# import fapi.G
import os
import sys


def create_fastapi() -> FastAPI:
    from mongoengine import connect
    app = FastAPI(version="2.0.0", title="Irori distributed system")
    connect(**db)
    uuidtoken = IroriUUID.objects()
    if not uuidtoken:
        uuidtoken = str(uuid.uuid4())
        IroriUUID(uuid=uuidtoken).save()
    else:
        uuidtoken = uuidtoken.first().uuid
    logger.critical(f'token: {uuidtoken}')

    if not IroriConfig.objects():
        IroriConfig().save()
    # if not Role.objects(name='guest'):
    #     Role(name='guest', allow=[]).save()
    # if not Role.objects(name='file_manager'):
    #     r = Role(name='file_manager', allow=['file_manager']).save()
    #     Adapter(username='file_manager', password='prohibit_login', role=r).save()
    # if not Profile.objects():
    #     Profile(name='default', master='114514').save()

    # fapi.G.first_time = True
    # from fapi.models.Routinuer import Routiner
    # Routiner
    if os.getcwd() not in sys.path:
        sys.path.append(os.getcwd())
    print(sys.path)

    from fapi.routers import master_router
    app.include_router(master_router)

    return app


app = create_fastapi()


@app.on_event('startup')
async def startup_coroutines():
    await Routiner.recover_routiners()
    await TempFile.resume()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        app,
        host=web_host,
        port=web_port,
    )
