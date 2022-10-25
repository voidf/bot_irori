import hashlib
import random
import json
import http
import urllib
from loguru import logger


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
            logger.debug(f"trans_result:{result['trans_result']}")
            res = result['trans_result'][0]['dst']

        except:
            res = f"网络连接错误"

        finally:
            if conn:
                conn.close()
        return res