import asyncio
import aiohttp
from loguru import logger
import json
from basicutils.socketutils import CoreEntity, MessageChain, Plain
from fapi import generate_jwt, verify_jwt
from Worker import task


class MiraiSession():
    def __init__(self, adapter_id: str):
        self._alive = True
        self._ases  = aiohttp.ClientSession()
        self.syncid = adapter_id
        
    async def enter_loop(self, wsurl: str):
        self.ws = await self._ases.ws_connect(wsurl)
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                logger.critical(msg.data)
                j = json.loads(msg.data)
                if 'data' in j and 'type' in j['data']:
                    if j['data']['type'] == 'GroupMessage':
                        ent = CoreEntity(
                            player=str(j['data']['sender']['group']['id'] + (1<<39)),
                            source=str(self.syncid),
                            meta={'mem': j['data']['sender']['id']},
                            chain=MessageChain.auto_make(j['data']['messageChain'])
                        )
                        await self.preprocess(ent)
                    elif j['data']['type'] == 'FriendMessage':
                        ent = CoreEntity(
                            player=str(j['data']['sender']['id']),
                            source=str(self.syncid),
                            meta={'mem': j['data']['sender']['id']},
                            chain=MessageChain.auto_make(j['data']['messageChain'])
                        )
                        await self.preprocess(ent)
                    # TODO: 临时消息，系统命令
                    task.delay(ent.json())


            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
    
    async def preprocess(self, ent: CoreEntity):
        for elem in ent.chain:
            if isinstance(elem, Plain):
                data = elem.tostr()
                c, *att = data.split(' ') 

                # Adapter参数预解析
                ato = []
                for i in att:
                    if i[:2] == "--":
                        arg,*val = i[2:].split("=")
                        ent.meta["-"+arg] = "".join(val)
                    else: ato.append(i)
                elem.text = ' '.join(ato)