import requests
from bs4 import BeautifulSoup as BS
import basicutils.CONST as C
import datetime
import json

def make_req2(dvd: int, typ: str='BTC'):
    ima = datetime.datetime.now()
    prv = ima - datetime.timedelta(days=dvd)
    r = requests.get(
            f'''https://api.nasdaq.com/api/quote/{typ}/historical?assetclass=crypto&fromdate={prv.strftime('%Y-%m-%d')}&limit={dvd}&todate={ima.strftime('%Y-%m-%d')}''',
            headers={
                "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "accept-encoding":"gzip, deflate, br",
                "accept-language":"zh-CN,zh;q=0.9",
                "cache-control":"no-cache",
                "dnt":"1",
                "pragma":"no-cache",
                "sec-fetch-mode":"navigate",
                "sec-fetch-site":"none",
                "sec-fetch-user":"?1",
                "upgrade-insecure-requests":"1",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
            }
        )
    res = r.text
    print(json.loads(res))
    return res

def fetch_cryptocurrency_info(typ: str = 'BTC'):
    lnk = f'https://api.nasdaq.com/api/quote/{typ}/info?assetclass=crypto'
    r = requests.get(lnk, headers={
        "accept":"application/json, text/plain, */*",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"zh-CN,zh;q=0.9",
        "cache-control":"no-cache",
        "dnt":"1",
        "origin":"https://www.nasdaq.com",
        "pragma":"no-cache",
        "referer":"https://www.nasdaq.com/market-activity/cryptocurrency/btc",
        "sec-fetch-dest":"empty",
        "sec-fetch-mode":"cors",
        "sec-fetch-site":"same-site",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    })
    j = json.loads(r.text)
    report = (f"币种：{j['data']['companyName']}\n"
    f"今日最高：{j['data']['keyStats']['High']['value']}\n"
    f"今日最低：{j['data']['keyStats']['Low']['value']}\n"
    f"现在价格：{j['data']['primaryData']['lastSalePrice']}\n"
    f"刷新时间：{j['data']['primaryData']['lastTradeTimestamp']}\n"
    f"变动幅度：{j['data']['primaryData']['percentageChange']}")

    print(json.loads(r.text))
    return report
def get_cryptocurrencies():
    r = requests.get(
        f'''https://www.nasdaq.com/market-activity/cryptocurrency''',
        headers={
            "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding":"gzip, deflate, br",
            "accept-language":"zh-CN,zh;q=0.9",
            "cache-control":"no-cache",
            "dnt":"1",
            "pragma":"no-cache",
            "sec-fetch-mode":"navigate",
            "sec-fetch-site":"none",
            "sec-fetch-user":"?1",
            "upgrade-insecure-requests":"1",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }
    )
    res = r.text
        # print(res)
    b = BS(res, 'html.parser')
    ccs = [i['data-symbol'] for i in b('tr', attrs={'data-asset-class':'cryptocurrency'})]
    print(ccs)
    return ccs
# print(make_req2(1))
# print(fetch('ETH'))
print(get_cryptocurrencies())
