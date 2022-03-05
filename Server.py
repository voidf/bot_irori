from fapi.models.Routiner import *
from fastapi import FastAPI, Depends
from loguru import logger
from cfg import db, web_host, web_port

from fapi.models.Auth import *
# import fapi.G
import os
import sys

sys.dont_write_bytecode = True

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
    from fapi.models.FileStorage import TempFile
    await TempFile.resume()
    for i in IroriConfig.objects().first().startup_connect_actions:
        from fapi.routers.auth import connect_mirai
        await connect_mirai(i['miraiwsurl'])
    # if os.path.exists('startup_actions.json'):
    #     import json
    #     with open('startup_actions.json', 'r') as f:
    #         j = json.load(f)
    #     await connect_mirai(j['miraiwsurl'])


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        app,
        host=web_host,
        port=web_port,
    )
