from mongoengine import DateTimeField
from typing import TypeVar, get_type_hints
import datetime

INVISIBLE = TypeVar('INVISIBLE')

class Base():
    """需要和mongoengine的Document多继承配套使用"""
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
    @classmethod
    def chk(cls, pk):
        if isinstance(pk, cls):
            return pk
        tmp = cls.objects(pk=pk).first()
        if not tmp:
            return cls(pk=pk).save()
        return tmp
    @classmethod
    def trychk(cls, pk):
        if isinstance(pk, cls):
            return pk
        tmp = cls.objects(pk=pk).first()
        if not tmp:
            return None
        return tmp

class SaveTimeBase(Base):
    create_time = DateTimeField()
    def save_changes(self):
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
    def __int__(self):
        return int(self.pid)
    def __str__(self):
        return str(self.pid)
    @classmethod
    def chk(cls, pk):
        return super().chk(str(pk))

class RefPlayerBase(Base):
    _player = ReferenceField(Player, primary_key=True, reverse_delete_rule=2)
    @classmethod
    def chk(cls, pk):
        if isinstance(pk, Player):
            return super().chk(pk)
        else:
            return super().chk(Player.chk(pk))
    @classmethod
    def trychk(cls, pk):
        if isinstance(pk, Player):
            return super().trychk(pk)
        else:
            return super().trychk(Player.chk(pk))
    @property
    def player(self):
        return Player.chk(self._data['_player'].id)