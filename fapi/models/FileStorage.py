from asyncio.tasks import ensure_future

from mongoengine.queryset.base import CASCADE
from basicutils.applications.File import ddl通知姬
from time import sleep
from typing import Union
from loguru import logger

from mido.messages.messages import Message
from mongoengine.fields import DateTimeField, FileField, IntField, ListField, ReferenceField, StringField
from basicutils import chain
import fapi.G

from fapi.models.Base import *
from mongoengine import *
import aiohttp
import asyncio
import math
import datetime
from basicutils.network import CoreEntity
from mongoengine import *
from fapi.models.Auth import *
from fapi.models.Auth import Adapter

routiner_namemap = {} # 根据名字查找Routinuer用

class FileStorage(Base, Document):
    meta = {'allow_inheritance': True}
    adapter = ReferenceField(Adapter, reverse_delete_rule=CASCADE)
    content = FileField()
    filename = StringField()
    content_type = StringField()

class TempFile(FileStorage):
    expires = DateTimeField()
    async def deleter(self):
        await asyncio.sleep(
            (self.expires-datetime.datetime.now()).total_seconds()
        )
        self.delete()
    @classmethod
    async def resume(cls):
        for i in cls.objects():
            asyncio.ensure_future(i.deleter())
