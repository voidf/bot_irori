from fastapi import FastAPI, Depends
from cfg import db

def create_fastapi() -> FastAPI:
    from mongoengine import connect
    app = FastAPI(version="2.0.0", title="Irori distributed system")
    connect(**db)

    from fapi.routers import master_router