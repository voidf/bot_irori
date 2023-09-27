import hashlib
import random
import json
import http
import urllib
import requests
import re
import time
from loguru import logger


# 网页白嫖
class Bing:
    timestamp_key = None
    token = None
    valid_time = None
    session = requests.session()
    session.headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'accept-encoding': 'gzip, deflate, br',
    }
    translator_url = 'https://cn.bing.com/translator'
    translate_url = 'https://cn.bing.com/ttranslatev3?isVertical=1&&IG=C14796C62F544E239E123D9292F50339&IID=translator.5026'
    cred_pat = re.compile(r"""var params_AbusePreventionHelper = \[(\d+),"([\w\-]+)",(\d+)\];""")
    @classmethod
    def get_cred(cls):
        if cls.timestamp_key is None or cls.timestamp_key + cls.valid_time < int(time.time() * 1000):
            r = cls.session.get(cls.translator_url)
            timestamp_key, cls.token, valid_time = cls.cred_pat.search(r.text).groups()
            cls.timestamp_key = int(timestamp_key)
            cls.valid_time = int(valid_time)
        return cls.timestamp_key, cls.token
    
    @classmethod
    def trans(cls, _from, _to, _text):
        # zh-Hans
        # en
        cls.get_cred()
        resp = cls.session.post(cls.translate_url, data={
            'fromLang': _from,
            'to': _to,
            'key': cls.timestamp_key,
            'token': cls.token,
            'text': _text,
        })
        logger.debug({
            'fromLang': _from,
            'to': _to,
            'key': cls.timestamp_key,
            'token': cls.token,
            'text': _text,
        })
        logger.debug(resp)
        logger.debug(resp.request.headers)
        logger.debug(resp.headers)
        logger.debug(resp.content)
        logger.debug(resp.text)
        return ''.join(map(lambda x: x['text'], resp.json()[0]['translations']))


# api
class Baidu:
    appid = None
    secret = None

    @classmethod
    def get_cred(cls):
        if cls.appid is None or cls.secret is None:
            from fapi.models.Auth import IroriConfig
            cfg = IroriConfig.objects().first()
            cls.appid, cls.secret = cfg.api_keys['baidu.fanyi.appid'], cfg.api_keys['baidu.fanyi.secret']
        return cls.appid, cls.secret

    @classmethod
    def trans(cls, _from, _to, _text):
        conn = None
        myurl = '/api/trans/vip/translate'
        salt = random.randint(32768, 65536)
        
        baidu_appid, baidu_secretKey = cls.get_cred()

        sign = baidu_appid + _text + str(salt) + baidu_secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + baidu_appid + '&q=' + urllib.parse.quote(
            _text) + '&from=' + _from + '&to=' + _to + '&salt=' + str(salt) + '&sign=' + sign

        try:
            conn = http.client.HTTPConnection('api.fanyi.baidu.com')
            conn.request('GET', myurl)
            response = conn.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            li = []
            for r in result['trans_result']:
                li.append(r['dst'])
            res = '\n'.join(li)

        except:
            res = f"网络连接错误"

        finally:
            if conn:
                conn.close()
        return res