import asyncio
import datetime
from fapi.models.Auth import *
from fapi.models.Base import *
from mongoengine import *
from mongoengine.fields import (DateTimeField, FileField, IntField, ListField,
                                ReferenceField, StringField)

routiner_namemap = {} # 根据名字查找Routinuer用

class FileStorage(Base, Document):
    meta = {'allow_inheritance': True}
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
