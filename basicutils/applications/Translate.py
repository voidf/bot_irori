"""翻译类"""
import os
import sys
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
import sys
import requests
import json
import random
import os
import ctypes
import http.client
import hashlib
import datetime
import urllib
from basicutils.chain import *
from basicutils.database import *
from basicutils.network import *
import basicutils.CONST as GLOBAL

sys.dont_write_bytecode = True

res = ''

from cfg import baidu_appid, baidu_secretKey
from fapi.models.Auth import IroriConfig
import jieba
import jieba.posseg as pseg

def _RM_convert(x, y, _volumn):
    if random.random() > _volumn:
        return x
    if x in {'，', '。'}:
        return '……'
    if x in {'!', '！'}:
        return '❤'
    if len(x) > 1 and random.random() < 0.5:
        return f'{x[0]}……{x}'
    else:
        if y == 'n' and random.random() < 0.5:
            x = '〇' * len(x)
        return f'……{x}'


def chs2yin(ent: CoreEntity):
    """#yinglish []
    抄自RimoChan/yinglish
    哼，不告诉你怎么用！
    """
    try:
        _volumn = float(ent.meta.get('-v', 0.5))
    except:
        _volumn = 0.5
    s = ent.chain.tostr()
    return ''.join([_RM_convert(x, y, _volumn) for x, y in pseg.cut(s)])

def jsontimestampnow(): return int(datetime.datetime.now().timestamp()*1000)

def deepl_translate(src, l1='ZH', l2='EN'):
    """
    src:源文本

    l1:源语言

    l2:目标语言"""
    smjb = random.randint(10000000, 99999999)
    get_translate_lnk = 'https://www2.deepl.com/jsonrpc'
    get_translate_headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-length": "435",
        "content-type": "application/json",
        "dnt": "1",
        "origin": "https://www.deepl.com",
        "pragma": "no-cache",
        "referer": "https://www.deepl.com/translator",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    get_translate_data = {
        "jsonrpc": "2.0", 
        "method": "LMT_handle_jobs", 
        "params": {
            "jobs": [
                {
                    "kind": "default", 
                    "raw_en_sentence": src, 
                    "raw_en_context_before": [], 
                    "raw_en_context_after":[], 
                    "preferred_num_beams":4, 
                    "quality":"fast"
                }
            ], 
            "lang": {
                "user_preferred_langs": [l2, l1], 
                "source_lang_user_selected": "auto", 
                "target_lang": l2
            }, 
            "priority": -1, 
            "timestamp": jsontimestampnow()
        }, 
        "id": smjb
    }
    r4 = requests.post(get_translate_lnk, headers=get_translate_headers, json=get_translate_data)
    res = json.loads(r4.text)
    print(r4.text)
    return res['result']['translations'][0]['beams'][0]['postprocessed_sentence']

def BDtranslate(req):
    trans = None
    myurl = '/api/trans/vip/translate'
    fromLang = req[0]
    toLang = req[1]
    salt = random.randint(32768, 65536)
    q = req[2]
    cfg = IroriConfig.objects().first()
    baidu_appid, baidu_secretKey = cfg.api_keys['baidu.fanyi.appid'], cfg.api_keys['baidu.fanyi.secret']

    sign = baidu_appid + q + str(salt) + baidu_secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + baidu_appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        trans = http.client.HTTPConnection('api.fanyi.baidu.com')
        trans.request('GET', myurl)
        response = trans.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        res = result['trans_result'][0]['dst']

    except:
        res = f"网络连接错误"

    finally:
        if trans:
            trans.close()
    return res

# 好好说话


def hhsh(req):
    result = ''
    url = 'https://lab.magiconch.com/api/nbnhhsh/guess'
    head = {'Content-Type': 'application/json'}
    re = {'text': req}
    res = json.loads(requests.post(
        url, headers=head, json=re, timeout=30).text)
    try:
        result += '\n'.join(res[0]['trans'])
    except:
        result = '尚未收录'
    return result

# 无符号位移: https://www.jianshu.com/p/24d11ab44ae6
# 这个函数可以得到32位int溢出结果，因为python的int一旦超过宽度就会自动转为long，永远不会溢出，有的结果却需要溢出的int作为参数继续参与运算


def int_overflow(val):
    maxint = 2147483647
    if not -maxint-1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val


def unsigned_right_shitf(n, i):
    # 数字小于0，则转为32位无符号uint
    if n < 0:
        n = ctypes.c_uint32(n).value
    # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
    if i < 0:
        return -int_overflow(n << abs(i))
    return int_overflow(n >> i)


def google_TL(src):
    a = src.strip()
    b = 406644
    b1 = 3293161072

    jd = "."
    美元b = "+-a^+6"
    Zb = "+-3^+b+-f"

    e = []
    for g in range(len(a)):
        m = ord(a[g])
        if 128 > m:
            e.append(m)
        else:
            if 2048 > m:
                e.append(m >> 6 | 192)
            else:
                if 55296 == (m & 64512) and g + 1 < len(a) and 56320 == (a[g+1] & 64512):
                    g += 1
                    m = 65535 + ((m & 1024) << 10) + (a[g] & 1023)
                    e.append(m >> 18 | 240)
                    e.append(m >> 12 & 63 | 128)
                else:
                    e.append(m >> 12 | 224)
                    e.append(m >> 6 & 63 | 128)
                e.append(m & 63 | 128)
    a = b
    for f in range(len(e)):
        a += int(e[f])
        a = google_RL(a, 美元b)
    a = google_RL(a, Zb)
    if b1:
        a ^= b1
    else:
        a ^= 0
    if 0 > a:
        a = (a & 2147483647) + 2147483647
    a %= 1E6
    return str(int(a)) + jd + str(int(a) ^ b)


def google_RL(a, b):
    t = 'a'
    Yb = '+'
    for c in range(0, len(b)-2, 3):
        d = b[c+2]
        if d >= t:
            d = ord(d[0]) - 87
        else:
            d = int(d)
        if b[c+1] == Yb:
            d = unsigned_right_shitf(a, d)
        else:
            d = int(a) << d
        if b[c] == Yb:
            a = int(a) + d & 4294967295
        else:
            a = int(a) ^ d
    return a


def googleTrans(req):
    trans = None
    fromLang = req[0]
    toLang = req[1]
    q = req[2]
    tk = google_TL(q)
    url = '/translate_a/single?client=t&sl='+fromLang+'&tl='+toLang+'&hl='+toLang+'&dt=bd&dt=ex&dt=ld&dt=md&dt=qc&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&source=sel&tk='\
        + tk+'&q='+urllib.parse.quote(q)
    try:
        trans = http.client.HTTPConnection('translate.google.cn')
        trans.request('GET', url, headers={
                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'})
        response = trans.getresponse()
        result_all = response.read().decode("utf-8")
        print(result_all)
        print('translate.google.cn'+url)
        result = json.loads(result_all)
        # print(result[0][-1][-1]) #原文读音
        # print(result[0][0][1]) #原文
        # print()
        # print(result[0][-1][-2]) #结果读音
        # print(result[0][0][0]) #结果
        # if result[7]:
        #    print(result[7][1]) #罗马音转平假
    except Exception as e:
        print(e)
    finally:
        if trans:
            trans.close()

    if req[0] == 'ja-Latn':
        if req[1] == 'ja-Hrgn':
            return result[7][1]
        else:
            tk = google_TL(result[7][1])
            url = '/translate_a/single?client=t&sl=ja&tl='+toLang+'&hl='+toLang+'&dt=bd&dt=ex&dt=ld&dt=md&dt=qc&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&source=sel&tk='\
                + tk+'&q='+urllib.parse.quote(result[7][1])
            try:
                trans = http.client.HTTPConnection('translate.google.com')
                trans.request('GET', url)
                response = trans.getresponse()
                result_all = response.read().decode("utf-8")
                result = json.loads(result_all)
            except Exception as e:
                print(e)
            finally:
                if trans:
                    trans.close()
            if req[1] == 'ja':
                return result[7][1]
    return result[0][0][0]

def deepl(ent: CoreEntity):
    """#deepl []
        向deepl发送烤肉请求，注意一段时间内请求过多会被ban
    用法：
        #deepl <源语言> <目标语言> <待翻译文本>
    也可以订阅快速翻译（碰到英文句子即触发）：
        #deepl --q
    或：
        #deepl --q=[目标语言*]
        * 目标语言为以下中的一种，默认为ZH
        "DE" - German
        "EN" - English
        "FR" - French
        "IT" - Italian
        "JA" - Japanese
        "ES" - Spanish
        "NL" - Dutch
        "PL" - Polish
        "PT" - Portuguese (all Portuguese varieties mixed)
        "RU" - Russian
        "ZH" - Chinese
    """
    player = ent.pid
    attrs = ent.chain.tostr().split(' ')
    if ' '.join(attrs) in GLOBAL.unsubscribes or ' '.join(attrs[2:]) in GLOBAL.unsubscribes:
        Sniffer.clear(player, '#deepl')
        return [Plain('我住嘴了')]
    if '-q' in ent.meta or '-quick' in ent.meta:
        tr = ent.meta.get('-q', ent.meta.get('-quick', 'ZH'))
        if not tr: tr = 'ZH'
        tr = tr.upper()
        sni: Sniffer = Sniffer.overwrite(player, '#deepl')
        sni.add(
            '#deepl',
            [
                TriggerRule(r'^[.0-9\s+-/*&^<>~=|%\(\)]+$', 99, False),
                TriggerRule(r'https{0,1}://', 99, False),
                TriggerRule(r'''^((?![^\x00-\xff]).)*[a-zA-Z]+((?![^\x00-\xff]).)*$''', args=('EN', tr))
            ]
        )
        return [Plain(f'快速翻译启动,结束打E')]
    if len(attrs) > 2:
        return [Plain(text=deepl_translate(l1=attrs[0], l2=attrs[1], src=' '.join(attrs[2:])))]
    else:
        return [Plain(text='原谅我不知道你在说什么（')]

def 能不能好好说话(ent: CoreEntity):
    """#好好说话 [#hhsh]
    来自fufu的功能，如果有不懂的缩写可以用它查询，例:#好好说话 bksn
    """
    r = ent.chain.tostr()
    if r:
        return [Plain(hhsh(r))]
    else:
        return [Plain('宁想说什么？')]


def 咕狗翻译(ent: CoreEntity):
    """#gkr []
    从fufu那里焊接来的咕狗翻译功能
    格式：
        #gkr <源语言> <目标语言> <待翻译部分>
    订阅智能翻译(不带等号指定语言时默认翻成中文)：
        #gkr --q=[目标语言]
    或：
        #gkr --q
    一般用例：
        #gkr ja zh-CN やりますね
    """
    player = ent.pid
    attrs = ent.chain.tostr().split(' ')
    if ' '.join(attrs) in GLOBAL.unsubscribes or ' '.join(attrs[2:]) in GLOBAL.unsubscribes:
        Sniffer.clear(player, '#gkr')
        return [Plain('我住嘴了')]
    if '-q' in ent.meta or '-quick' in ent.meta:
        tr = ent.meta.get('-q', ent.meta.get('-quick', 'zh'))
        if not tr: tr = 'zh'
        sni: Sniffer = Sniffer.overwrite(player, '#gkr')
        sni.add(
            '#gkr',
            [
                TriggerRule(r'^[.0-9\s+-/*&^<>~=|%\(\)]+$', 99, False),
                TriggerRule(r'https{0,1}://', 99, False),
                TriggerRule(r'''^((?![^\x00-\xff]).)*[a-zA-Z]+((?![^\x00-\xff]).)*$''', args=('en', tr))
            ]
        )
        return [Plain(f'快速翻译启动,结束打E')]
    if len(attrs) > 2:
        return [Plain(text=googleTrans([attrs[0], attrs[1], ' '.join(attrs[2:])]))]
    else:
        return [Plain(text='原谅我不知道你在说什么（')]


def 百度翻译(ent: CoreEntity):
    """#bkr [#kr]
    从fufu那里焊接来的度娘翻译功能
    格式：
        #bkr <源语言> <目标语言> <待翻译部分>
    订阅智能翻译(不带等号指定语言时默认翻成中文)：
        #bkr --q=[目标语言]
    或：
        #bkr --q
    一般用例：
        #bkr jp zh 自分で百度しろ
    """
    player = ent.pid
    attrs = ent.chain.tostr().split(' ')
    if ' '.join(attrs) in GLOBAL.unsubscribes or ' '.join(attrs[2:]) in GLOBAL.unsubscribes:
        Sniffer.clear(player, '#bkr')
        return [Plain('我住嘴了')]
    if '-q' in ent.meta or '-quick' in ent.meta:
        tr = ent.meta.get('-q', ent.meta.get('-quick', 'zh'))
        if not tr: tr = 'zh'
        sni: Sniffer = Sniffer.overwrite(player, '#bkr')
        sni.add(
            '#bkr',
            [
                TriggerRule(r'^[.0-9\s+-/*&^<>~=|%\(\)]+$', 99, False),
                TriggerRule(r'https{0,1}://', 99, False),
                TriggerRule(r'''^((?![^\x00-\xff]).)*[a-zA-Z]+((?![^\x00-\xff]).)*$''', args=('en', tr))
            ]
        )
        return [Plain(f'快速翻译启动，结束打E')]
    if len(attrs) > 2:
        return [Plain(text=BDtranslate([attrs[0], attrs[1], ' '.join(attrs[2:])]))]
    else:
        return [Plain(text='原谅我不知道你在说什么（\n')]


if __name__ == '__main__':
    req = []
    req.append('en')
    req.append('zh-CN')
    #req.append('わたしは だれですか？')
    req.append('Who I am?')
    print(googleTrans(req))
