from GLOBAL import cfg
from mongoengine import *
from typing import TypeVar, get_type_hints
import datetime

INVISIBLE = TypeVar('INVISIBLE')

connect(**cfg['db'])

class Base():
    """每次都写get_base_info好烦"""
    @staticmethod
    def expand_mono(obj):
        if hasattr(obj, 'get_base_info'):
            return getattr(obj, 'get_base_info')()
        else:
            return obj
    def get_base_info(self, *args):
        try:
            d = {}
            for k in self._fields_ordered:
                if get_type_hints(self).get(k, None) == INVISIBLE:
                    continue
                selfk = getattr(self, k)
                if isinstance(selfk, list):
                    for i in selfk:
                        d.setdefault(k, []).append(Base.expand_mono(i))
                else:
                    d[k] = Base.expand_mono(selfk)
            d['id'] = str(self.id)
            return d
        except: # 不加注解上面会报错
            return self.get_all_info()
    def get_all_info(self, *args):
        # print(vars(self))
        d = {} 
        for k in self._fields_ordered:
            selfk = getattr(self, k)
            if isinstance(selfk, list):
                for i in selfk:
                    d.setdefault(k, []).append(Base.expand_mono(i))
            else:
                d[k] = Base.expand_mono(selfk)
        if hasattr(self, 'id'):
            d['id'] = str(self.id)
        return d

class SaveTimeBase(Base):
    last_modify = DateTimeField()
    create_time = DateTimeField()
    def save_changes(self):
        self.last_modify = datetime.datetime.now()
        return self.save()
    def first_create(self):
        self.create_time = datetime.datetime.now()
        return self.save_changes()
    
    def get_base_info(self, *args):
        d = super().get_base_info(*args)
        d['create_time'] = self.create_time.strftime('%Y-%m-%d')
        return d

    def get_all_info(self, *args):
        d = super().get_all_info(*args)
        d['create_time'] = self.create_time.strftime('%Y-%m-%d')
        return d

class Player(Document, Base):
    pid = StringField(primary_key=True)
    items = DictField()

