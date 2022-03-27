from fapi.Sessions import *
from fapi.utils.jwt import *
import json
from Worker import task
from loguru import logger

class MiraiSession(Session):
    # def __init__(self, adapter_id: Union[str, Adapter]):
        # self._alive = True
        # self._ases  = aiohttp.ClientSession()
        # self.aid = adapter_id
        # self.syncid = adapter_id
        # self.jwt = generate_jwt(adapter_id)
        # self.dbobj = Adapter.trychk(self.aid)
        
    async def _receive_loop(self, wsurl: str):
        """
        仅用于将消息从mirai拉下来执行处理，不用于回传消息。
        只要接收回环还在运行，就认为会话存活。
        反之销毁会话必须停止接收回环。
        """
        async for msg in self.ws:
            # if not self._alive:
                # logger.warning('manually closed')
                # break
            try:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    logger.debug(msg.data)
                    j = json.loads(msg.data)
                    # logger.warning(j)
                    if 'data' in j and 'type' in j['data']:
                        if j['data']['type'] == 'GroupMessage':
                            pid = str(j['data']['sender']['group']['id'] + (1<<39))
                            ent = CoreEntity(
                                jwt=generate_session_jwt(self.sid),
                                pid=pid,
                                source=self.sid,
                                member=str(j['data']['sender']['id']),
                                meta={},
                                chain=MessageChain.auto_make(j['data']['messageChain'])
                            )

                        elif j['data']['type'] == 'FriendMessage':
                            pid = str(j['data']['sender']['id'])
                            ent = CoreEntity(
                                jwt=generate_session_jwt(self.sid),
                                pid=pid,
                                source=self.sid,
                                member=str(j['data']['sender']['id']),
                                meta={},
                                chain=MessageChain.auto_make(j['data']['messageChain'])
                            )

                            # continue # debug
                        # TODO: 临时消息
                        if await self._handle_syscall(ent):
                            continue
                        try:
                            # logger.warning(f'conn2wk{ent}')
                            task.delay(ent.json()) # 向Worker发布任务
                        except:
                            logger.critical(traceback.format_exc())

                else:
                    logger.critical(msg.type)
                    logger.critical(f'connection closed {wsurl}')
                # elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
            except:
                logger.critical(traceback.format_exc())
        self._alive = False
    
    async def enter_loop(self, wsurl: str):
        self._ases = aiohttp.ClientSession()

        """回环入口，对于mirai的对接，向提供的wsurl发起websocket连接"""
        self.ws = await self._ases.ws_connect(wsurl, headers={})
        await self.ws.receive_json() # 捕获连接消息
        myplayers = []
        await self.ws.send_json({
            "syncId": -1,
            "command": "friendList"
        })
        ret=(await self.ws.receive_json())
        logger.debug(ret)
        for i in ret['data']['data']:
            pid = i['id']
            myplayers.append(str(pid))

        await self.ws.send_json({
            "syncId": -1,
            "command": "groupList"
        })
        ret=(await self.ws.receive_json())
        logger.debug(ret)
        for i in ret['data']['data']:
            pid = i['id'] + (1 << 39)
            myplayers.append(str(pid))
        
        self.receiver = asyncio.ensure_future(self._receive_loop(wsurl))
        return myplayers

    async def close(self):
        if self._alive:
            self.receiver.cancel()
            await self.ws.close()
            await self._ases.close()
        self._alive = False

    async def _deliver(self, ent: CoreEntity):
        pi = int(ent.pid)
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


    
