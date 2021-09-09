from mongoengine import *
from fapi.models.Base import *

class Role(Base, Document):
    allow = ListField(StringField())
    name = StringField(primary_key=True)

class Adapter(Base, Document):
    username = StringField(primary_key=True)
    password = StringField()
    role = ReferenceField(Role, reverse_delete_rule=DO_NOTHING)