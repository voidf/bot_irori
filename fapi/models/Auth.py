from mongoengine import *
from mongoengine.queryset.base import *
from fapi.models.Base import *

class Role(Base, Document):
    allow = ListField(StringField())
    name = StringField(primary_key=True)
    @classmethod
    def chk(cls, pk):
        return super().chk(pk)
    @classmethod
    def trychk(cls, pk):
        return super().trychk(pk)

class Adapter(Base, Document):
    username = StringField(primary_key=True)
    password = StringField()
    role = ReferenceField(Role, reverse_delete_rule=DO_NOTHING)
    @classmethod
    def chk(cls, pk):
        return super().chk(pk)
    @classmethod
    def trychk(cls, pk):
        return super().trychk(pk)
    # def __int__(self):
    #     return int(self.username)
    def __str__(self):
        return str(self.username)