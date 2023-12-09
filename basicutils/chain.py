from pydantic import BaseModel, RootModel # 为了用json
from pydantic import Field
from typing import *
import datetime
import json
from io import BytesIO

from loguru import logger

class Element(BaseModel):
    type: str = None
    meta: dict = {}
    def json(self):
        return super().json(exclude_none=True)
    def tostr(self) -> str:
        return ''
    def __str__(self) -> str:
        return self.tostr()

def convert_text(x: dict):
    return {
        'type': "Plain",
        'text': x['data']['text']
    }

def convert_image(x: dict):
    return {
        'type': 'Image',
        'url': x['data']['url']
    }

onebot2mirai_converter = {
    "text": convert_text,
    "image": convert_image
}

class MessageChain(RootModel):
    root: List[Element]
    @classmethod
    def parse_obj(cls, obj: List[Element]) -> "MessageChain":
        handled_elements = []
        for i in obj:
            if isinstance(i, Element): # 已经是Element
                if i.meta:
                    handled_elements.append(i)
                    continue
                else:
                    tobeappend = i
            elif isinstance(i, dict):
                if "type" in i: # 目前为dict，但可以转换成Element
                    if i["type"] in onebot2mirai_converter:
                        i = onebot2mirai_converter[i["type"]](i)
                    for ii in Element.__subclasses__():
                        if ii.__name__ == i["type"]:
                            tobeappend = ii.model_validate(i)
                            break
            elif isinstance(i, (tuple, list)):
                newchain = cls.model_validate(i)
                for j in newchain:
                    if not j.meta and handled_elements and handled_elements[-1].type == 'Plain' and j.type == 'Plain':
                        handled_elements[-1].text += j.text
                    else:
                        handled_elements.append(j)
                continue
            elif isinstance(i, str):
                tobeappend = Plain(text=i)

                
            if tobeappend.type == "Plain": # 转换后的Element
                if not tobeappend.text:
                    continue
                if not tobeappend.meta and handled_elements and handled_elements[-1].type == "Plain":
                    handled_elements[-1].text += tobeappend.text
                    continue
            handled_elements.append(tobeappend)
        return cls(root=handled_elements)
    @classmethod
    def get_empty(cls) -> "MessageChain":
        return MessageChain(root=[])
    @classmethod
    def auto_merge(cls, *iterables: Iterable, attach_kwargs: dict={}) -> "MessageChain":
        li = []
        for i in iterables:
            chain = MessageChain.auto_make(i)
            if chain.root:
                chain.root[0].meta.update(attach_kwargs)
                li.extend(chain.root)
        return MessageChain.auto_make(li)
    @classmethod
    def auto_make(cls, obj: Union[str, Element, list, tuple, "MessageChain"]) -> "MessageChain":
        if isinstance(obj, str):
            if not obj:
                return cls(root=[])
            return cls(root=[Plain(obj)])
        if isinstance(obj, Element):
            return cls(root=[obj])
        if isinstance(obj, (list, tuple)):
            return MessageChain.parse_obj(obj)
        if isinstance(obj, MessageChain):
            return obj
        logger.error(f'转换错误：不可转换的实体{obj}')
        return cls(root=[Plain(str(obj))])
    def __iter__(self):
        return self.root.__iter__()
    def __str__(self) -> str:
        return self.tostr()
    def to_str_list(self) -> list[dict]:
        """序列化自己为可json的dict列表"""
        return [i.model_dump() for i in self.root]
    def tostr(self) -> str:
        """调用所有消息元素的tostr方法然后不分隔的拼成一个字符串返回"""
        output = []
        for i in self.root:
            output.append(i.tostr())
        return ''.join(output)
    def onlyplain(self) -> str:
        """只将Plain文本元素空格隔开拼成一个字符串返回"""
        output = []
        for i in self.root:
            if i.type == "Plain":
                output.append(i.tostr())
        return ' '.join(output)
    def pop_first_cmd(self) -> str:
        for p, i in enumerate(self.root):
            if i.type == 'Plain':
                cmd, *ato = i.text.split(' ', 1)
                if not ato:
                    self.root.pop(p)
                i.text = ' '.join(ato)
                return cmd.strip()
        return ''

class Plain(Element):
    type: str = "Plain"
    text: str
    def __init__(self, text: str, *_, **__):
        super().__init__(text=text, **__)
    def tostr(self) -> str:
        return self.text

class Source(Element):
    id: int
    time: int

class Quote(Element):
    id: int
    groupId: int
    senderId: int
    targetId: int
    origin: MessageChain

class At(Element):
    type: str = "At"
    target: int
    display: Optional[str] = None
    def tostr(self) -> str:
        return self.display

class AtAll(Element):
    type: str = "AtAll"
    def tostr(self):
        return '@全体成员'

class Face(Element):
    type: str = "Face"
    faceId: int
    name: Optional[str] = None
    def tostr(self):
        return f'[表情:{self.faceId}]'

class Image(Element): # 三个参数任选其一，出现多个参数时，按照imageId > url > path > base64的优先级
    type: str = "Image"
    imageId: Optional[str] = None # 存在时忽略后两个
    url: Optional[str] = None # 网址
    base64: Optional[str] = None # b64
    path: Optional[str] = None # 本地路径，相对于plugins/MiraiAPIHTTP/images，不建议用
    def tostr(self):
        return "[图片]"

class FlashImage(Element):
    type: str = "FlashImage"
    imageId: Optional[str] = None
    url: Optional[str] = None 
    base64: Optional[str] = None
    path: Optional[str] = None
    def tostr(self):
        return "[闪照]"

class Voice(Element):
    type: str = "Voice"
    voiceId: Optional[str] = None
    url: Optional[str] = None
    base64: Optional[str] = None
    path: Optional[str] = None
    def tostr(self):
        return "[语音]"

class Xml(Element):
    type: str = "Xml"
    xml: str
    def tostr(self):
        return self.xml

class Json(Element):
    type: str = "Json"
    Json: str = Field(..., alias="json")
    def tostr(self):
        return self.Json

class App(Element):
    type: str = "App"
    content: str
    def tostr(self):
        return "[App消息]"

class Poke(Element):
    type: str = "Poke"
    name: str
    def tostr(self) -> str:
        return f"[戳一戳:{self.name}]"

class Dice(Element):
    type: str = "Dice"
    value: int
    def tostr(self):
        return f"[骰子:{self.value}]"

class MusicShare(Element):
    type:str = "MusicShare"
    kind: str
    title: str
    summary: str
    jumpUrl: str
    pictureUrl: str
    musicUrl: str
    brief: str
    def tostr(self):
        return f"[音乐分享:{self.musicUrl}]"

class ForwardMessageNode(BaseModel):
    senderId: int # 发送人QQ
    time: int # 时间戳
    senderName: str
    messageChain: str
    sourceId: int


class ForwardMessage(Element):
    type: str = "Forward"
    nodeList: List[ForwardMessageNode] = []

class File(Element):
    type: str = "File"
    id: str # 文件识别id
    name: str # 文件名
    size: int # 文件大小