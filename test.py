import datetime
import requests
import json
import random


def jsontimestampnow(): return int(datetime.datetime.now().timestamp()*1000)

smjb = random.randint(10000000, 99999999)
s = requests.sessions.Session()

def reactive_session():


    global s, smjb
    get_cfduid_lnk = 'https://static.deepl.com/css/cookieBanner.$21aa7c.css'

    get_cfduid_headers = {
        "accept": "text/css,*/*;q=0.1",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "referer": "https://www.deepl.com/translator",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }

    privacy_lnk = 'https://www.deepl.com/PHP/backend/privacy.php?request_type=jsonrpc&il=ZH'

    privacy_headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-length": "138",
        "content-type": "application/json",
        "dnt": "1",
        "origin": "https://www.deepl.com",
        "pragma": "no-cache",
        "referer": "https://www.deepl.com/translator",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }

    privacy_payload = {
        "jsonrpc": "2.0",
        "method": "setPrivacySettings",
        "params": {
            "consent": [
                "NECESSARY",
                "PERFORMANCE",
                "COMFORT"
            ],
            "mode": "LAX_AUTO"
        },
        "id": smjb
    }

    LMTBID_lnk = 'https://www2.deepl.com/jsonrpc'

    LMTBID_headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-length": "389",
        "content-type": "application/json",
        "dnt": "1",
        "origin": "https://www.deepl.com",
        "pragma": "no-cache",
        "referer": "https://www.deepl.com/translator",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }


    LMTBID_data = {
        "jsonrpc": "2.0",
        "method": "LMT_handle_jobs",
        "params": {
            "jobs": [
                {
                    "kind": "default",
                    "raw_en_sentence": "h",
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
            "commonJobParams": {"formality": None},
            "timestamp": jsontimestampnow()
        },
        "id": smjb
    }
    r = s.get(get_cfduid_lnk, headers=get_cfduid_headers)
    r2 = s.post(privacy_lnk, headers=privacy_headers, json=privacy_payload)
    r3 = s.post(LMTBID_lnk, headers=LMTBID_headers, json=LMTBID_data)

def deepl_translate(src, l1='ZH', l2='EN'):
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

    r4 = s.post(get_translate_lnk, headers=get_translate_headers, json=get_translate_data)
    res = json.loads(r4.text)
    print(res['result']['translations'][0]['beams'][0]['postprocessed_sentence'])

BaiduTTSLnk = ' http://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&spd=5&text='

while 1:
    print(eval(input('>>>')))
