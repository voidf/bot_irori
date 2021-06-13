import os
import json
import traceback
from Utils import chkcfg
from typing import *
from mongoengine import *
from database_utils import *
from GLOBAL import logging

class Sniffer(Document, Base):
    player = ReferenceField(Player, primary_key=True)
    commands = DictField()

def removeSniffer(player, event):
    player = str(player)
    logging.debug(chkcfg(player).quick_calls.pop(event, "未找到对应sniffer"))
    sni = Sniffer.chk(Player.chk(player))
    logging.debug(sni.commands.pop(event, "未找到对应sniffer"))
    sni.save()



def overwriteSniffer(player, event, pattern, *attrs):
    player = str(player)
    eventObj = {event: {'sniff': [pattern], 'attrs': attrs}}
    chkcfg(player).quick_calls.update(eventObj)
    sni = Sniffer.chk(Player.chk(player))
    sni.commands.update(eventObj)
    sni.save()

def appendSniffer(player, event, pattern):  # 注意捕捉exc
    player = str(player)
    chkcfg(player).quick_calls[event]['sniff'].append(pattern)
    sni = Sniffer.chk(Player.chk(player))
    sni.commands[event]['sniff'].append(pattern)
    sni.save()

def clearSniffer(player) -> str:
    player = str(player)
    tc = chkcfg(player)
    tc.quick_calls = {}
    Sniffer.objects(pk=Player.chk(player)).delete()
    return "[Sniffer] 清除完毕"


def syncSniffer(player) -> str:
    player = str(player)
    tc = chkcfg(player)
    sni = Sniffer.chk(Player.chk(player))
    tc.quick_calls = sni.commands
    print(f'[Sniffer] 同步完毕，现有{len(tc.quick_calls)}个已经激活的嗅探器')
    return f'[Sniffer] 同步完毕，现有{len(tc.quick_calls)}个已经激活的嗅探器'
