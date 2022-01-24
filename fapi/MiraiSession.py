from fapi.Sessions import *
from fapi import *
from fapi.routers.convert import to_amr
from basicutils.task import server_api
import json
from Worker import task
from io import BytesIO
import markdown

class MiraiSession(Session):
    # def __init__(self, adapter_id: Union[str, Adapter]):
        # self._alive = True
        # self._ases  = aiohttp.ClientSession()
        # self.aid = adapter_id
        # self.syncid = adapter_id
        # self.jwt = generate_jwt(adapter_id)
        # self.dbobj = Adapter.trychk(self.aid)
        
    async def __receive_loop(self, wsurl: str):
        """仅用于将消息从mirai拉下来执行处理，不用于回传消息"""
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
                            ato = await self.__preprocess(ent)

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
                            ato = await self.__preprocess(ent)

                            # continue # debug
                        # TODO: 临时消息，系统命令
                        if len(ato)>=2 and ato[0] == 'sudo' and ent.member in IroriConfig.get().auth_masters:
                            # TODO: 迁移python3.10 改match语法
                            ret = await {
                                'eval': sys_eval,
                                'exec': sys_exec,
                                'run': sys_run,
                            }.get(ato[1], sys_help)(ent, ato[2:])
                            ent.chain = MessageChain.auto_make(ret)
                            await self.__auto_deliver(ent)
                            return
                        try:
                            logger.warning(f'conn2wk{ent}')
                            task.delay(ent.json()) # 向Worker发布任务
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
            except:
                logger.critical(traceback.format_exc())
    
    async def enter_loop(self, wsurl: str):
        """预处理好友表、群表"""
        self.ws = await self._ases.ws_connect(wsurl, headers={})
        """突然觉得客户通过bot发消息不太合理
        await self.ws.send_json({
            "syncId": -1,
            "command": "friendList"
        })
        a2p = SessionManager.a2p.setdefault(self.aid, {})
        
        for i in await self.ws.receive_json()['data']:
            pid = i['id']
            SessionManager.p2s.setdefault(pid, []).append(self.sid)
            a2p.setdefault(self.sid, []).append((pid, i['nickname']))

        await self.ws.send_json({
            "syncId": -1,
            "command": "groupList"
        })

        for i in await self.ws.receive_json()['data']:
            pid = i['id'] + (1 << 39)
            SessionManager.p2s.setdefault(pid, []).append(self.sid)
            a2p.setdefault(self.sid, []).append((pid, i['name']))
        """
        self.receiver = asyncio.ensure_future(self.__receive_loop(wsurl))
        
    async def close(self):
        self.receiver.cancel()
        await self.ws.close()
        await self._ases.close()
    
    async def __preprocess(self, ent: CoreEntity):
        retato = []
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
                retato.extend(ato)
        return retato
                
    async def __auto_deliver(self, ent: CoreEntity):
        """根据ent.pid决定发送目标向ws送ent序列化后的json，顺便处理markdown转换"""
        # pi = int(ent.player)
        pi = int(ent.pid)
        output = []
        if '-md' in ent.meta:
            for i in ent.chain:
                if isinstance(i, Image):
                    if i.url:
                        output.append(f'![]({i.url})')
                    elif i.base64:
                        if i.base64[:3] == 'iVB':
                            output.append(f'![](data:image/png;base64,{i.base64})')
                        else:
                            output.append(f'![](data:image/jpeg;base64,{i.base64})')
                elif isinstance(i, Voice):
                    output.append(f'<p><audio src="{i.url}""></p>')
                else:
                    output.append(f'{i.tostr()}')
            html = markdown.markdown(''.join(output).replace('\n', '<br>'))
            t = TempFile(
                filename='TempHtmlFile.htm',
                content_type='text/html',
                expires=datetime.datetime.now()+datetime.timedelta(seconds=3600)
            )
            t.content.put(BytesIO(bytes(html, 'utf-8')))
            t.save()
            asyncio.ensure_future(t.deleter())
            ent.chain.__root__ = [Plain(server_api(f'/worker/oss/{t.pk!s}'))]
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
        logger.debug('upload triggered')
        try:
            chain = ent.chain
            logger.debug(chain)
            ent.chain = MessageChain.get_empty()
            for i in chain:
                if i.meta and 'delay' in i.meta:
                    if ent.chain.__root__:
                        await self.__auto_deliver(ent)
                    await asyncio.sleep(float(i.meta['delay']))
                    ent.chain.__root__.clear()
                elif isinstance(i, Voice):
                    i = Voice(url=server_api('/worker/oss/' + (await to_amr(
                        ent.meta.get('-vmode', 0),
                        lnk=i.url if i.url else '',
                        b64=i.base64 if i.base64 else ''
                    ))['url']))
                    if ent.chain.__root__:
                        await self.__auto_deliver(ent)
                    ent.chain.__root__.clear()
                ent.chain.__root__.append(i)
            if ent.chain.__root__:
                await self.__auto_deliver(ent)
        except ValueError:
            return "not mirai"
