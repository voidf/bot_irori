"""用户账号管理类"""
from fapi.models.Player import Player
import os
import sys

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

import basicutils.CONST as GLOBAL


from bs4 import BeautifulSoup
import re
import asyncio
import requests
import json
import random
import urllib
import traceback
import hashlib
import urllib
from basicutils.chain import *
from basicutils.network import *
from basicutils.task import *

from uuid import uuid4
from basicutils.algorithms import randstr
from fapi.utils.jwt import generate_player_jwt

def 外部令牌(ent: CoreEntity):
    """/token [/tk]
    管理您的外部令牌
    用法：
    /token regen 重新生成口令，并使先前的jwt无效化
    /token jwt 生成jwt令牌
    """
    args = ent.chain.tostr().split(' ')
    player = Player.chk(ent.member)
    ctoken = player.items.get('token', '')
    buf = []
    if ent.pid != ent.member:
        buf.append('【警告】不建议在群聊中使用此功能')
    if not ctoken or args and args[0] == 'regen':
        ctoken = str(uuid4())
        player.items['token'] = ctoken
        player.save()
        buf.append('【提示】口令已重新生成，注意先前的jwt令牌会全部失效')
    if args and args[0] == 'jwt':
        buf.append('【重要】请妥善保管您的新jwt令牌: '+generate_player_jwt(ent.member))

    return buf