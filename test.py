import requests
translator = 'https://www.deepl.com/translator'

translator_h = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "cache-control":"no-cache",
    "dnt":"1",
    "pragma":"no-cache",
    "referer":"https://www.deepl.com/pro-account",
    "sec-fetch-mode":"navigate",
    "sec-fetch-site":"same-origin",
    "sec-fetch-user":"?1",
    "upgrade-insecure-requests":"1",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}

options_lnk = 'https://s.deepl.com/web/statistics'

options_headers = {
    "accept":"*/*",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "access-control-request-headers":"content-type",
    "access-control-request-method":"POST",
    "cache-control":"no-cache",
    "dnt":"1",
    "origin":"https://www.deepl.com",
    "pragma":"no-cache",
    "referer":"https://www.deepl.com/translator",
    "sec-fetch-mode":"cors",
    "sec-fetch-site":"same-site",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}


d = {
    'text':'混元形意太极拳',
    'source_lang':'ZH',
    'target_lang':'EN',

}
s = requests.sessions.Session()
# r1 = s.get(lnk, headers=h)
r2 = s.options(options_lnk, headers=options_headers)

print(r2.text)

while 1:
    print(eval(input('>>>')))