import asyncio
import aiohttp

class MiraiSession():
    def __init__(self):
        self._alive = True
        self._ases  = aiohttp.ClientSession()
        
    async def enter_loop(self, wsurl: str):
        self.ws = await