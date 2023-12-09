from pydantic import BaseModel # 为了用json
import json
from basicutils.chain import MessageChain

# Core内部传输用
class CoreEntity(BaseModel):
    """irori系统内部的消息传输形式"""
    chain: MessageChain
    # player: str  = '' # 发送来源player ObjectId
    pid: str  = ''    # 发送来源player id
    source: str  = '' # 发送来源Sessionid或是相关jwt
    meta: dict   = {} # 额外参数，对worker会使用ts时间戳来维护忙状态，解析的--参数也会放在这里
    jwt: str     = '' # 令牌
    member: str  = '' # 实际发送者的player号
    @classmethod
    def handle_json(cls, j):
        d = json.loads(j)
        d['chain'] = MessageChain.auto_make(d['chain'])
        return cls(**d)
    @classmethod
    def wrap_rawstring(cls, msg: str):
        mt = {'msg': msg}
        return cls(
            chain=MessageChain.get_empty(),
            meta=mt
        )
    @classmethod
    def wrap_strchain(cls, msg: str):
        return cls(
            chain=MessageChain.auto_make(msg),
        )
    def unpack_rawstring(self) -> str:
        return self.meta.get('msg', '')
    @classmethod
    def wrap_dict(cls, d: dict):
        return cls(
            chain=MessageChain.get_empty(),
            meta=d
        )
    # 更pydantic2.0后，MessageChain不能直接输出子元素的field，所以这里要手动处理
    def old_style_json(self):
        j = self.model_dump()
        j['chain'] = json.dumps(self.chain.to_str_list())
        return j