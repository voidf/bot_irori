from fapi.Sessions import *
from fapi import *
from Worker import task
from starlette.websockets import WebSocketState
import fastapi
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
                if await self._handle_syscall(ent):
                    continue
                try:
                    task.delay(ent.json()) # 向Worker发布任务
                except:
                    logger.critical(traceback.format_exc())
            except RuntimeError:
                break
            except:
                logger.critical(traceback.format_exc())
        self._alive = False
        await self.ws.close()
    
    async def enter_loop(self, ws: fastapi.WebSocket,  pid: str):
        self.pid = pid
        self.ws = ws
        await self.ws.accept()

        self.receiver = asyncio.ensure_future(self._receive_loop())
        return [self.pid]
        
    async def close(self):
        self.receiver.cancel()
        await self.ws.close()
        await self._ases.close()
        self._alive = False

    @abstractmethod
    async def _deliver(self, ent: CoreEntity):
        raise NotImplementedError

class WebsocketSessionJson(WebsocketSessionBase):
    async def _recv_ent(self) -> CoreEntity:
        message = await self.ws.receive_json()
        j = message['chain'] # chain: 消息链
        return CoreEntity(
            jwt=generate_session_jwt(self.sid),
            pid=self.pid,
            source=self.sid,
            member=self.pid,
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

