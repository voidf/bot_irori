import starlette
from fapi.Sessions import *
from fapi import *
from Worker import task
from starlette.websockets import WebSocketState
import fastapi
import asyncio
from fapi.utils.jwt import generate_session_jwt
class WebsocketSessionBase(Session):
    @abstractmethod
    async def _recv_ent(self) -> CoreEntity:
        raise NotImplementedError
    async def _receive_loop(self):
        """仅用于将消息从ws拉下来执行处理，不用于回传消息"""
        while self._alive and self.ws.application_state == WebSocketState.CONNECTED:
            try:
                ent = await self._recv_ent()
                if not ent:
                    continue
                if await self._handle_syscall(ent):
                    continue
                try:
                    task.delay(ent.json()) # 向Worker发布任务
                except:
                    logger.critical(traceback.format_exc())
            except RuntimeError:
                break
            except starlette.websockets.WebSocketDisconnect:
                break
            except:
                logger.critical(traceback.format_exc())
        await self.close()
    
    async def enter_loop(self, ws: fastapi.WebSocket,  pid: str):
        self.pid = pid
        self.ws = ws
        await self.ws.accept()

        self.receiver = asyncio.ensure_future(self._receive_loop())
        return [self.pid]
        
    async def close(self):
        await self.ws.close()
        await self._ases.close()
        self._alive = False
        self.receiver.cancel()

    @abstractmethod
    async def _deliver(self, ent: CoreEntity):
        raise NotImplementedError

class WebsocketSessionJson(WebsocketSessionBase):
    async def _recv_ent(self) -> CoreEntity:
        message = await self.ws.receive_json()
        j = message['chain'] # chain: 消息链
        custom_pid = (message.get('pid') or self.pid)
        custom_mid = (message.get('mid') or self.pid)
        return CoreEntity(
            jwt=generate_session_jwt(self.sid),
            pid=custom_pid,
            source=self.sid,
            member=custom_mid,
            meta={},
            chain=MessageChain.auto_make(j)
        )
    async def _deliver(self, ent: CoreEntity):
        """向ws送ent序列化后的json"""
        payload = {
            "chain": ent.chain.dict()["__root__"]
        }
        await self.ws.send_json(payload)

class WebsocketSessionPlain(WebsocketSessionBase):
    async def _recv_ent(self) -> CoreEntity:
        return CoreEntity(
            jwt=generate_session_jwt(self.sid),
            pid=self.pid,
            source=self.sid,
            member=self.pid,
            meta={},
            chain=MessageChain.auto_make(await self.ws.receive_text())
        )

    async def _deliver(self, ent: CoreEntity):
        """向ws送字符串"""
        await self.ws.send_text(ent.chain.tostr())

class WebsocketSessionOnebot(WebsocketSessionBase):
    async def enter_loop(self, ws: fastapi.WebSocket):
        self.ws = ws
        await self.ws.accept()
        await self.ws.send_json({
            "action": "get_friend_list"
        })
        ret = await self.ws.receive_json()
        logger.debug(ret)
        myplayers = []
        for i in ret['data']:
            pid = i['user_id']
            myplayers.append(str(pid))

        await self.ws.send_json({
            "action": "get_group_list"
        })

        ret = await self.ws.receive_json()
        logger.debug(ret)
        for i in ret['data']:
            pid = i['group_id']
            myplayers.append(str(pid + (1 << 39)))

        self.receiver = asyncio.ensure_future(self._receive_loop())
        return myplayers


    async def _recv_ent(self) -> CoreEntity:
        message = await self.ws.receive_json()
        logger.debug(message)
        if message.get("post_type") != "message":
            return

        j = message['message'] # chain: 消息链
        if group_id := message.get('group_id'):
            pid = int(group_id) + (1<<39)
            mid = int(message['user_id'])
        else:
            pid = int(message['user_id'])
            mid = int(message['user_id'])
        return CoreEntity(
            jwt=generate_session_jwt(self.sid),
            pid=int(pid),
            source=int(self.sid),
            member=int(mid),
            meta={},
            chain=MessageChain.auto_make(j)
        )

    async def _deliver(self, ent: CoreEntity):
        """向ws送ent序列化后的json"""
        pi = int(ent.pid)
        if pi & (1<<39):
            payload['group_id'] = str(pi - (1<<39))
            payload = {
                "action": "send_group_msg",
                "group_id": pi,
                "message": ent.chain.dict()["__root__"]
            }
        else:
            payload = {
                "action": "send_private_msg",
                "user_id": pi,
                "message": ent.chain.dict()["__root__"]
            }
        await self.ws.send_json(payload)

