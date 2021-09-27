import requests
from bs4 import BeautifulSoup
import basicutils.CONST as C
import datetime
def fetchAtCoderContests() -> dict:
    j = {}
    l = []
    r = requests.get('https://atcoder.jp/contests/',
                     headers=C.AtCoderHeaders, timeout=30)
    s = BeautifulSoup(r.text, 'html.parser')
    try:
        for p, i in enumerate(s.find('h3', string='Active Contests').next_sibling.next_sibling('tr')):
            if p:
                l.append({
                    'length': i('td')[2].text,
                    'ranking_range': i('td')[3].text,
                    'title': i('a')[1].text,
                    'begin': datetime.datetime.strptime(i('a')[0].text, "%Y-%m-%d %H:%M:%S+0900") - datetime.timedelta(hours=1)
                })
    except:
        pass
    j['running'] = l
    l = []
    # 持续时间 排名区间 比赛名 比赛时间
    for p, i in enumerate(s.find('h3', string='Upcoming Contests').next_sibling.next_sibling('tr')):
        if p:
            l.append({
                'length': i('td')[2].text,
                'ranking_range': i('td')[3].text,
                'title': i('a')[1].text,
                'begin': datetime.datetime.strptime(i('a')[0].text, "%Y-%m-%d %H:%M:%S+0900") - datetime.timedelta(hours=1)
            })
    j['upcoming'] = l
    print(j)
    return j


fetchAtCoderContests()