from mongoengine import *
from mongoengine.queryset.base import *
from fapi.models.Base import *

# from enum import Enum

# class Scope(Enum):
#     """权限集"""
#     FILE_MANAGER = "file_manager"
#     SYS = "sys"
#     OSS_ADMIN = "oss_A"

# class Role(Base, Document):
#     allow = ListField(StringField())
#     name = StringField(primary_key=True)
#     @classmethod
#     def chk(cls, pk):
#         return super().chk(pk)
#     @classmethod
#     def trychk(cls, pk):
#         return super().trychk(pk)

# class Profile(Base, Document):
    # master = ReferenceField("Player")
    # name = StringField(primary_key=True)

import uuid
class IroriUUID(Document):
    """单例令牌"""
    uuid = StringField()

    @classmethod
    def get(cls) -> "IroriUUID":
        return cls.objects().first()

    @classmethod
    def regen(cls):
        cls.objects().modify(uuid=uuid.uuid4())

class IroriConfig(Document):
    """首选项单例文件，塞数据库为了热更
    放Server端需要读的数据"""
    auth_masters = ListField(StringField(), default=[]) # 狗管理名单，可以执行系统调用

    player_whitelist = DictField(default={}) # 白名单，player只能执行给定的指令 {pid: ["#A", "#C"] ...}
    player_blacklist = DictField(default={}) # 黑名单，player不能执行指定的指令 {pid: ["#A", "#C"] ...}
    player_ignorelist = ListField(default=[]) # 屏蔽player号名单，注意要当成一个set来维护

    startup_connect_actions = ListField(default=[]) # 启动时连接动作，目前只实现了miraiwsurl

    api_keys = DictField(default={})
    """放爬虫需要的api keys，现含的值有:
    - baidu.fanyi.appid
    - baidu.fanyi.secret
    - saucenao.key
    """
    @classmethod
    def get(cls) -> "IroriConfig":
        return cls.objects().first()

# class Adapter(Base, Document):
#     username = StringField(primary_key=True)
#     password = StringField()
#     role = ReferenceField(Role, reverse_delete_rule=DO_NOTHING)
#     items = DictField()
#     tokens = ListField(StringField())
#     profile = ReferenceField(Profile)
#     @classmethod
#     def chk(cls, pk):
#         return super().chk(pk)
#     @classmethod
#     def trychk(cls, pk):
#         return super().trychk(pk)
#     # def __int__(self):
#     #     return int(self.username)
#     def __str__(self):
#         return str(self.username)