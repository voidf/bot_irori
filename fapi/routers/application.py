from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from cfg import *

from fapi.models.Auth import *

from fapi.utils.jwt import *

import asyncio
application_route = APIRouter(
    prefix="/application",
    tags=["application - 静态网页应用接口"],
)


@application_route.get('/ws')
async def websocket_page():
    with open('htmlws.htm', 'r') as f:
        return HTMLResponse(f.read())