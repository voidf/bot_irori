import asyncio
import traceback
import aiohttp
from loguru import logger
import json
from basicutils.network import *
from basicutils.chain import *
from fapi import generate_jwt, verify_jwt
from Worker import task
from typing import Union
from fapi.models.Auth import *

class MiraiSession():
    def __init__(self, adapter_id: Union[str, Adapter]):
        self._alive = True
        self._ases  = aiohttp.ClientSession()
        # self.syncid = adapter_id
        self.jwt = generate_jwt(adapter_id)
        
    async def enter_loop(self, wsurl: str):
        """仅用于将消息从mirai拉下来执行处理，不用于回传消息"""
        self.ws = await self._ases.ws_connect(wsurl, headers={})
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                logger.debug(msg.data)
                j = json.loads(msg.data)
                # logger.warning(j)
                if 'data' in j and 'type' in j['data']:
                    if j['data']['type'] == 'GroupMessage':
                        ent = CoreEntity(
                            player=str(j['data']['sender']['group']['id'] + (1<<39)),
                            source=str(self.jwt),
                            meta={'mem': j['data']['sender']['id']},
                            chain=MessageChain.auto_make(j['data']['messageChain'])
                        )
                        await self.preprocess(ent)
                        if j['data']['sender']['group']['id'] not in (699731560, 491959457):
                            continue

                    elif j['data']['type'] == 'FriendMessage':
                        ent = CoreEntity(
                            player=str(j['data']['sender']['id']),
                            source=str(self.jwt),
                            meta={'mem': j['data']['sender']['id']},
                            chain=MessageChain.auto_make(j['data']['messageChain'])
                        )
                        await self.preprocess(ent)
                        # continue # debug
                    # TODO: 临时消息，系统命令

                    # logger.warning(ent)
                    try:
                        task.delay(ent.json())
                    except UnboundLocalError as e:
                        logger.debug('非可处理消息事件:{}', str(e))
                        pass
                    except:
                        logger.critical(traceback.format_exc())

            else:
                logger.critical(msg.type)
                logger.critical(f'connection closed {wsurl}')
            # elif msg.type == aiohttp.WSMsgType.ERROR:
                break
    
    async def preprocess(self, ent: CoreEntity):
        for elem in ent.chain:
            if isinstance(elem, Plain):
                data = elem.tostr()
                att = data.split(' ') 

                # Adapter参数预解析
                ato = []
                for i in att:
                    if i[:2] == "--":
                        arg,*val = i[2:].split("=")
                        ent.meta["-"+arg] = "".join(val)
                    else: ato.append(i)
                elem.text = ' '.join(ato)

    async def auto_deliver(self, ent: CoreEntity):
        pi = int(ent.player)
        payload = {
            "syncId": -1,
            "content": {
                "messageChain": ent.chain.dict()["__root__"]
            },
        }
        if pi > (1<<32):
            pi -= 1<<39
            payload['command'] = "sendGroupMessage"
            payload['content']['target'] = pi
            logger.warning(json.dumps(payload))
            await self.ws.send_json(payload)
        else:
            payload['command'] = "sendFriendMessage"
            payload['content']['target'] = pi
            logger.warning(json.dumps(payload))
            await self.ws.send_json(payload)


    async def upload(self, ent: CoreEntity):
        """将消息链往mirai发送，实际上只取用了player和chain，后继应该支持meta特殊处理"""
        try:
            chain = ent.chain
            ent.chain = MessageChain.get_empty()
            for i in chain:
                if i.meta and 'delay' in i.meta:
                    if ent.chain.__root__:
                        await self.auto_deliver(ent)
                    await asyncio.sleep(float(i.meta['delay']))
                    ent.chain = MessageChain.get_empty()
                ent.chain.__root__.append(i)
            if ent.chain.__root__:
                await self.auto_deliver(ent)
        except ValueError:
            return "not mirai"