from mongoengine import *
from typing import Optional, TypeVar, Union, get_type_hints

from mongoengine.fields import *
from mongoengine.pymongo_support import *
from mongoengine.context_managers import *
from mongoengine.document import *

from fapi.models.Auth import Adapter
from fapi.models.Base import *
from basicutils.algorithms import *
import basicutils.CONST

INVISIBLE = TypeVar('INVISIBLE')

class Player(Document):
    pid = StringField()
    aid = ReferenceField(Adapter)
    items = DictField()
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
    # def __int__(self):
        # return int(self.pid)
    def __str__(self):
        return str(self.pk)
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
    def chk(cls, pk: str, aid: Optional[Union[Adapter, str]]=None):
        # print("CHK", pk, aid)
        # print(pk, )
        if isinstance(pk, cls):
            return pk
        if aid is None or len(pk)==24:
            q = cls.objects(pk=pk).first()
            if not q:
                raise FileNotFoundError("指定player不存在")
            # print(q.get_base_info())
            return q
        else:
            a = Adapter.chk(aid)
            q = cls.objects(aid=a, pid=pk).first()
            if not q:
                q = cls(aid=a, pid=pk).save()
                # print("NEW PLAYER", q.get_base_info(), "CREATED!")
            # print(q.get_base_info())
            return q
    
    def upd_credit(self, operator: str, val: float) -> bool:
        """修改用户的信用点
        参数：
            [str]operator(操作符)
            [int]val(操作数)
        返回：
            [bool]是否操作成功
        """
        if operator not in basicutils.CONST.credit_operators: return False
        c = self.items.get('credit', 500)
        c, c2 = evaluate_expression(f'{c}{operator}{float(val)}')
        c2 = float(c2.strip())
        self.items['credit'] = c2
        self.save()
        return True

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