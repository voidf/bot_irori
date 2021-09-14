from mongoengine import *
from typing import TypeVar, Union, get_type_hints
import datetime
import cfg

INVISIBLE = TypeVar('INVISIBLE')

connect(**cfg.db)

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

# from abc import ABC, abstractmethod
# class Routiner(RefPlayerBase, Document):
#     meta = {'allow_inheritance': True}
#     adapterid = StringField()

#     @classmethod
#     async def recover_routiners(cls):
#         for sc in cls.__subclasses__():
#             sc.resume()

#     @classmethod
#     async def resume(cls):
#         raise NotImplementedError

# class CodeforcesRoutinuer(Routiner):
#     mode = StringField(default='Y')
#     @classmethod
#     def resume(cls):


# class CFSubscribe(RefPlayerBase, Document):
#     mode = StringField(default='Y')

# TODO: 考虑移入Routiner
class ATCoderSubscribe(RefPlayerBase, Document):
    pass

class NowCoderSubscribe(RefPlayerBase, Document):
    pass

class SentenceSubscribe(RefPlayerBase, Document):
    pass

class WeatherSubscribe(Document, RefPlayerBase):
    city = ListField(StringField())

# TODO: 考虑移入application

class SlidingPuzzle(Document, RefPlayerBase):
    bg = ImageField()
    mat = ListField(ListField(IntField()))

class Asobi2048Data(RefPlayerBase, Document):
    mat = ListField(ListField(IntField()))

class Vote(Document, RefPlayerBase):
    title = StringField()
    items = DictField()
    memberChoices = DictField()
    limit = IntField(default=5)

# class DDLLog(RefPlayerBase, Document):
#     content = DictField()



# class CreditSubscribe(RefPlayerBase, Document):
#     pass

import basicutils.CONST
from basicutils.algorithms import evaluate_expression
class CreditLog(RefPlayerBase, Document):
    credit = IntField(default=500)
    @classmethod
    def get(cls, user: Union[int, str]) -> int:
        return cls.chk(user).credit
    @classmethod
    def upd(cls, user: Union[int, str], operator: str, val: int) -> bool:
        """修改用户的信用点
        参数：
            [int]user(QQ号)
            [str]operator(操作符)
            [int]val(操作数)
        返回：
            [bool]是否操作成功
        用例：
            CreditLog.upd(114514, '+', 1)
        """
        if operator not in basicutils.CONST.credit_operators: return False
        c = cls.get(user)
        c, c2 = evaluate_expression(f'{c}{operator}{int(val)}')
        c2 = c2.strip()
        cls.chk(user).update(credit=int(c2))
        return True


class Sniffer(Document, RefPlayerBase):
    commands = DictField()
    @classmethod
    def overwrite(cls, player, event, pattern, *attrs):
        eventObj = {event: {'sniff': [pattern], 'attrs': attrs}}
        sni = cls.chk(player)
        sni.commands.update(eventObj)
        sni.save()

    @classmethod
    def append(cls, player, event, pattern):
        sni = cls.chk(player)
        sni.commands[event]['sniff'].append(pattern)
        sni.save()

    @classmethod
    def clear(cls, player):
        cls.objects(pk=Player.chk(player)).delete()
    
    @classmethod
    def remove(cls, player, event):
        sni = cls.chk(player)
        sni.commands.pop(event, "未找到对应sniffer")
        sni.save()
