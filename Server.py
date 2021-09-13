from fastapi import FastAPI, Depends
from cfg import db, web_host, web_port

from fapi.models.Auth import *
from fapi import encrypt
# import fapi.G
def create_fastapi() -> FastAPI:
    from mongoengine import connect
    app = FastAPI(version="2.0.0", title="Irori distributed system")
    connect(**db)
    # fapi.G.first_time = True
    # from fapi.models.Routinuer import Routiner
    # Routiner


    from fapi.routers import master_router
    app.include_router(master_router)
    
    return app

app = create_fastapi()



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        app,
        host=web_host,
        port=web_port,
    )