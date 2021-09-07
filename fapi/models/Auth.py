from mongoengine import *
from models.Base import *

class Role(Base, Document):
    allow = ListField(StringField())
    name = StringField(primary_key=True)

class Adapter(Base, Document):
    username = StringField(primary_key=True)
    password = StringField()
    role = ReferenceField(Role)