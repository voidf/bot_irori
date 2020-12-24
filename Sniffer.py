import os
import json
import traceback
from Utils import chkcfg
from typing import *


def removeSniffer(player, event):
    print(chkcfg(player).quick_calls.pop(event, "未找到对应sniffer"))
    try:
        with open(f'sniffer/{player}', 'r') as f:
            j = json.load(f)
        del j[event]
        with open(f'sniffer/{player}', 'w') as f:
            json.dump(j, f)
    except:
        print('缓存sniffer文件出错')
        print(traceback.format_exc())


def overwriteSniffer(player, event, pattern, *attrs):
    eventObj = {event: {'sniff': [pattern], 'attrs': attrs}}
    chkcfg(player).quick_calls.update(eventObj)
    if not os.path.exists(f'sniffer/{player}'):
        with open(f'sniffer/{player}', 'w') as f:
            json.dump(eventObj, f)
        return
    with open(f'sniffer/{player}', 'r') as f:
        j = json.load(f)
    j.update(eventObj)
    with open(f'sniffer/{player}', 'w') as f:
        json.dump(j, f)


def appendSniffer(player, event, pattern):  # 注意捕捉exc
    chkcfg(player).quick_calls[event]['sniff'].append(pattern)
    with open(f'sniffer/{player}', 'r') as f:
        j = json.load(f)
    j[event]['sniff'].append(pattern)
    with open(f'sniffer/{player}', 'w') as f:
        json.dump(j, f)


def clearSniffer(player) -> str:
    tc = chkcfg(player)
    print('clearing')
    try:
        tc.quick_calls = {}
    except:
        print('可能是内存里没有这个嗅探器引起的：')
        traceback.print_exc()
    if not os.path.exists(f'sniffer/{player}'):
        return '没有储存sniffer，无需清空'
    else:
        os.remove(f'sniffer/{player}')
        return '已清除sniffer'


def syncSniffer(player) -> str:
    tc = chkcfg(player)
    if not os.path.exists(f'sniffer/{player}'):
        try:
            tc.quick_calls = {}
        except:
            print(traceback.format_exc())
        return '同步完毕，没有活动的嗅探器'
    else:
        with open(f'sniffer/{player}', 'r') as f:
            j = json.load(f)
        tc.quick_calls = j
    return f'同步完毕，现有{len(tc.quick_calls)}个已经激活的嗅探器'
