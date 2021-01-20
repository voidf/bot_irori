import os
import requests
import asyncio
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import traceback
import random
import string
import functools
import GLOBAL
import json
from typing import *
from PIL import Image as PImage
from PIL import ImageFont, ImageDraw
import base64
import importlib
import sys

async def rmTmpFile(fi:str):
    await asyncio.sleep(60)
    os.remove(fi)

def randstr(l: int) -> str: return ''.join(random.choices(string.ascii_letters+string.digits,k=l))

def fetchAtCoderContests() -> dict:
    j = {}
    l = []
    r = requests.get('https://atcoder.jp/contests/',
                     headers=GLOBAL.AtCoderHeaders)
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


def fetchCodeForcesContests():
    r = requests.get('https://codeforces.com/api/contest.list')
    li = {}
    for i in r.json()['result']:
        if i['phase'] == 'FINISHED':
            break
        contest = li.setdefault(i['id'], {})
        contest['title'] = i['name']
        contest['routine'] = datetime.datetime.fromtimestamp(i['startTimeSeconds'])
        contest['length'] = f"{i['durationSeconds']/60}min"
        contest['countdown'] = str(datetime.timedelta(seconds=i['relativeTimeSeconds']))

    # r = requests.get('https://codeforces.com/contests?complete=true')
    # print(r)
    # soup = BeautifulSoup(r.text, 'html.parser')
    # li = {}
    # for i in soup('table')[0]('tr'):
    #     if any(i('td')):  # 标题 作者 日期 时长 开始倒计时 （爬到的是UTC+3
    #         contest = li.setdefault(i['data-contestid'], {})
    #         pos = i('td')[0].text.find('Enter')
    #         if pos != -1:
    #             print('正在运行的比赛')
    #             contest['title'] = i('td')[0].text[:pos-1].strip()
    #         else:
    #             try:
    #                 contest['title'] = i('td')[0].string.strip()
    #                 contest['authors'] = [au.string.strip()
    #                                       for au in i('td')[1]('a')]
    #                 contest['routine'] = datetime.datetime.strptime(
    #                     i('td')[2].a.span.string.strip(), '%b/%d/%Y %H:%M') + datetime.timedelta(hours=5)
    #                 contest['length'] = i('td')[3].string.strip()
    #                 contest['countdown'] = i('td')[4].text.strip()
    #             except:
    #                 print(traceback.format_exc())
    return li


def fetchNowCoderContests() -> list:
    l = []
    res = requests.get(
        'https://ac.nowcoder.com/acm/contest/vip-index?&headNav=www')
    bs_res = BeautifulSoup(res.text, 'html.parser')
    items = bs_res.find('div', class_='platform-mod js-current')
    for item in items.find_all(class_='platform-item'):
        ans = item.find(class_='platform-item-cont')
        contest_name = ans.find('a', target='_blank').text
        contest_time = ans.find('li', class_='match-time-icon').text
        li = contest_time.split('\n')
        d = datetime.datetime.strptime(li[0], "比赛时间：%Y-%m-%d %H:%M")
        l.append({
            "title": contest_name,
            "begin": d,
            "length": li[2].strip()
        })
    return l


def fetchWeather(city: str) -> list:
    search_lnk = 'http://toy1.weather.com.cn/search?cityname=' + city
    j = json.loads(requests.get(search_lnk).text[1:-1])[0]['ref'].split('~')
    output = [f'{j[2]}的天气数据:']
    weather_lnk = f'http://www.weather.com.cn/weather/{j[0]}.shtml'
    b = BeautifulSoup(requests.get(weather_lnk).content, 'html.parser')
    ctr = 0
    pos = 10
    for p, i in enumerate(b('li')):
        if i.text.find('今天') != -1:
            ctr += 1
            if ctr >= 2:
                pos = p
                break
    for i in b('li')[pos:pos+7]:
        t = i('p')
        output.append(
            f'{i.h1.text} {t[0].text} {t[1].text.strip()} {t[2].span["title"]}{t[2].text.strip()}')
    return output


def fetchSentences(d):
    r = requests.get(
        f'http://sentence.iciba.com/index.php?c=dailysentence&m=getTodaySentence&_={int(datetime.datetime.now().timestamp()*1000)}')
    j = json.loads(r.text)
    try:
        rr = requests.get(j['picture'])
        fn = 'tmp' + randstr(4)
        with open(fn, 'wb') as f:
            f.write(rr.content)
        d['img'] = fn
        print(fn)
        asyncio.ensure_future(rmTmpFile(fn))
    except:
        print(f'【每日一句】爬图炸了:{traceback.format_exc()}')
    d.setdefault('plain', []).append(j['content'])
    d.setdefault('plain', []).append(j['note'])



