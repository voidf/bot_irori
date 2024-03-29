"""爬虫类"""
from dataclasses import dataclass
import enum
import os
import sys

from async_timeout import timeout

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

import basicutils.CONST as GLOBAL

import datetime
from bs4 import BeautifulSoup
import re
import asyncio
import requests
import json
import random
import urllib
import traceback
import hashlib
import urllib
from basicutils.chain import *
from basicutils.network import *
from basicutils.task import *

@dataclass
class Contest():
    id: str
    title: str
    begintime: float
    length: float

def contesttime2str(t: float) -> str:
    return datetime.datetime.strftime(datetime.datetime.fromtimestamp(t), "%m月%d日 %H:%M")


def subscriber(keyword: str, routiner: str, ent: CoreEntity, contest_type: str) -> str:
    """没命中回空字符串"""
    ent.meta['routiner'] = routiner
    if keyword in GLOBAL.unsubscribes:
        resp = requests.delete(
            internal_api('/worker/routiner'),
            json={'ents': ent.json()}
        )
        if resp.status_code!=200:
            return resp.text
        return f"已取消{contest_type}比赛提醒推送"
    elif keyword in GLOBAL.subscribes:
        resp = requests.post(
            internal_api('/worker/routiner'),
            json={'ents': ent.json()}
        )
        if resp.status_code!=200:
            return resp.text
        return f"已订阅{contest_type}比赛提醒推送"
    elif keyword == 'upd':
        ent.meta['call'] = 'upd'
        resp = requests.options(
            internal_api('/worker/routiner'),
            json={'ents': ent.json()}
        )
        if resp.status_code!=200:
            return resp.text
        return f"成功更新{contest_type}比赛推送"
    return ""

def contest_fetcher_common(routiner: str, ent: CoreEntity, contest_type: str, spider: Callable[[None], List[Contest]]):
    attrs = ent.chain.tostr().split(' ')
    li = []

    if attrs:
        ret = subscriber(attrs[0],routiner,ent,contest_type)
        if ret: return ret

    for c in spider():
        hint = [c.title, f"{contesttime2str(c.begintime)}开始，持续{datetime.timedelta(seconds=c.length)!s}"]
        if c.begintime > datetime.datetime.now().timestamp():
            hint.append(f"倒计时{datetime.datetime.fromtimestamp(c.begintime)-datetime.datetime.now()!s}")
        else:
            hint.append(f"已经开始{datetime.datetime.now()-datetime.datetime.fromtimestamp(c.begintime)!s}")

        li.append("\n".join(hint))
    if not li:
        li = '没有即将开始的比赛'
    return '\n\n'.join(li)

def 爬一言(ent: CoreEntity):
    """#一言 [#yy]
    请求一言app，加某些参数会黑化
    """
    dst = ent.chain.tostr()
    for _ in ('f','sl','nm','cao','你妈','屌','mmp','傻逼','妈逼','操'):
        if _ in dst.lower():
            tmp = requests.get('https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn')
            return [Plain(text=tmp.text)]

    tmp = requests.get('https://v1.hitokoto.cn')
    j = json.loads(tmp.text)
    return [Plain(text=j['hitokoto'])]


def 爬OEIS(ent: CoreEntity):
    """#oeis []
    根据给定的逗号隔开的数列在OEIS寻找符合条件的数列，例:#oeis 1,1,4,5,1,4
    """
    s = ent.chain.tostr()

    if s:
        for i in s.split(','):
            if not i.isdigit():
                return [Plain('输入格式需为半角逗号分隔的整数')]
            else:
                r = requests.get(f'http://oeis.org/search?fmt=data&q={s}')
                s = BeautifulSoup(r.text,'html.parser')
                resp = []
                for i in s('table',attrs={'cellpadding':'0','cellspacing':'0','border':'0','width':'100%'}):
                    try:
                        #print(i)
                        t1 = Plain('oeis.org'+i.tr.td.a['href']+'\n')
                        t2 = Plain('$$$'.join(list(i.next_sibling.next_sibling.tt.strings))+'\n\n')
                        resp.append(t1)
                        resp.append(t2)
                    except:
                        pass
                return resp
    else:
        return [Plain('输入格式需为半角逗号分隔的整数')]

def 爬CF(ent: CoreEntity):
    """#CF []
    爬取CodeForces将要开始的比赛的时间表
    可用参数:
        TD  取消提醒
        sub 订阅提醒"""
    def spider() -> List[Contest]:
        li = []
        for i in requests.get('https://codeforces.com/api/contest.list', timeout=30).json()['result']:
            if i['phase'] == 'FINISHED':
                break
            li.append(
                Contest(
                    i['id'],
                    i['name'],
                    i['startTimeSeconds'],
                    i['durationSeconds']
                )
            )
        return li
    return contest_fetcher_common('CodeforcesRoutiner', ent, 'Codeforces', spider)

def 爬AtCoder(ent: CoreEntity):
    """#AT []
    爬取AtCoder将要开始的比赛的时间表
    可用参数:
        TD  取消提醒
        sub 订阅提醒
    """
    def spider() -> List[Contest]:
        l = []
        r = requests.get('https://atcoder.jp/contests/',
                        headers=GLOBAL.AtCoderHeaders, timeout=30)
        s = BeautifulSoup(r.text, 'html.parser')
        try:
            for p, i in enumerate(s.find('h3', string='Active Contests').next_sibling.next_sibling('tr')):
                if p:
                    hours, mins = i('td')[2].text.split(':')
                    l.append(
                        Contest(
                            i('a')[1]['href'],
                            i('a')[1].text, 
                            (datetime.datetime.strptime(i('a')[0].text, "%Y-%m-%d %H:%M:%S+0900") - datetime.timedelta(hours=1)).timestamp(),
                            int(hours) * 3600 + int(mins) * 60
                        )
                    )
        except:
            pass
        # 持续时间 排名区间 比赛名 比赛时间
        for p, i in enumerate(s.find('h3', string='Upcoming Contests').next_sibling.next_sibling('tr')):
            if p:
                hours, mins = i('td')[2].text.split(':')
                l.append(
                    Contest(
                        i('a')[1]['href'],
                        i('a')[1].text, 
                        (datetime.datetime.strptime(i('a')[0].text, "%Y-%m-%d %H:%M:%S+0900") - datetime.timedelta(hours=1)).timestamp(),
                        int(hours) * 3600 + int(mins) * 60
                    )
                )
        return l
    return contest_fetcher_common('AtcoderRoutiner', ent, 'atcoder', spider)

def 爬LaTeX(ent: CoreEntity):
    """#LaTeX [#tex, #latex]
    爬自https://latex.vimsky.com，我不会写LaTeX，炸了说一下我看看
    """
    base = r'\dpi{150} \bg_white \large ' + ent.chain.tostr().replace('+','&plus;')
    lnk = 'https://latex.vimsky.com/test.image.latex.php?fmt=png&dl=0&val='+urllib.parse.quote(urllib.parse.quote(base))
    return Image(url=lnk)

import html

def 爬牛客(ent: CoreEntity):
    """#牛客 [#NC]
    爬取牛客将要开始的比赛的时间表
    可用参数:
        TD  取消提醒
        sub 订阅提醒
    """
    def spider() -> List[Contest]:
        l: List[Contest] = []
        res = requests.get(
            'https://ac.nowcoder.com/acm/contest/vip-index', timeout=30)
        sp = BeautifulSoup(res.text, 'html.parser')
        for item in sp.find_all('div',class_='platform-item js-item'):
            j = json.loads(html.unescape(html.unescape(item['data-json'])))
            l.append(
                Contest(
                    j['contestId'],
                    j['contestName'],
                    j['contestStartTime']/1e3,
                    j['contestDuration']/1e3,
                )
            )
        return l
    return contest_fetcher_common('NowcoderRoutiner', ent, '牛客', spider)

def 爬力扣(ent: CoreEntity):
    """#力扣 [#LC]
    爬取力扣将要开始的比赛的时间表
    可用参数:
        TD  取消提醒
        sub 订阅提醒
    """
    def spider() -> List[Contest]:
        l: List[Contest] = []
        res = requests.post('https://leetcode-cn.com/graphql', json={
            'operationName': None, 
            'variables': {}, 
            'query': '{\n  contestUpcomingContests {\n    containsPremium\n    title\n    cardImg\n    titleSlug\n    description\n    startTime\n    duration\n    originStartTime\n    isVirtual\n    isLightCardFontColor\n    company {\n      watermark\n      __typename\n    }\n    __typename\n  }\n}\n'
        }, timeout=30)
        for item in res.json()['data']['contestUpcomingContests']:
            l.append(
                Contest(
                    item['titleSlug'],
                    item['title'],
                    item['startTime'],
                    item['duration'],
                )
            )
        return l
    return contest_fetcher_common('LeetcodeRoutiner', ent, '力扣', spider)
from urllib.parse import unquote
def 爬洛谷(ent: CoreEntity):
    """#洛谷 [#luogu]
    爬取洛谷将要开始的比赛的时间表
    可用参数:
        TD  取消提醒
        sub 订阅提醒
    """
    def spider() -> List[Contest]: # 洛谷爬虫需要至少带UA，encoding启用压缩，可选
        l: List[Contest] = []
        res = requests.get(
            'https://www.luogu.com.cn/contest/list',
            headers={
                "accept-encoding":"gzip, deflate, br", # br压缩要额外装brotli这个库才能有requests支持
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
            },
            timeout=30)
        
        for item in json.loads(unquote(re.findall(r"""JSON.parse\(decodeURIComponent\("(.*?)"\)\);""", res.text)[0]))['currentData']['contests']['result']:
            if item['endTime'] < datetime.datetime.now().timestamp():
                break
            l.append(
                Contest(
                    item['id'],
                    item['name'],
                    item['startTime'],
                    item['endTime']-item['startTime'],
                )
            )
        return l
    return contest_fetcher_common('LuoguRoutiner', ent, '洛谷', spider)

def 爬歌(ent: CoreEntity):
    """#什么值得听 [#uta, #music]
    根据给定关键词从几个平台爬歌（以后大概不会更新更多平台的咕（危
    """
    keyword = urllib.parse.quote(ent.chain.tostr())
    ans = []
    lnks = []

    try:
        kugoulnk = f'http://songsearch.kugou.com/song_search_v2?keyword={keyword}&page=1'
        r = ses.get(kugoulnk)
        j = json.loads(r.text.strip())
        
        fid = j['data']['lists'][0]['FileHash']
        lnk2 = f'http://trackercdn.kugou.com/i/v2/?key={hashlib.md5(bytes(fid+"kgcloudv2","utf-8")).hexdigest()}&hash={fid}&br=hq&appid=1005&pid=2&cmd=25&behavior=play'
        rr = ses.get(lnk2)
        ans.append('酷狗：')
        ans.append(j['data']['lists'][0]['FileName'])
        ans.append(json.loads(rr.text)['url'][0])
        lnks.append(ans[-1])
        ans.append('')
    except:
        ans.append('酷狗炸了')
        print(traceback.format_exc())

    logger.debug(ans)
    logger.debug(lnks)
    if '-voice' in ent.meta:
        for p, i in enumerate(lnks):
            lnks[p] = Voice(url=i)
    else:
        lnks = []
    return [Plain('\n'.join(ans))] + lnks

from mongoengine import *

def 爬天气(ent: CoreEntity):
    """#天气 [#weather]
    传入需要查询的城市拼音或汉字
    如：
        #天气 shanghai
    可以订阅每日的天气推送：
    用法：
        #天气 <城市名拼音> sub
    注意此处订阅是新添加需要推送的城市，而不是覆写
    如需取消所有推送，请使用：
        #天气 cancel
    """
    def fetchWeather(city: str) -> list:
        search_lnk = 'http://toy1.weather.com.cn/search?cityname=' + city
        # logger.warning(search_lnk)
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
    attrs = ent.chain.tostr().split(' ')
    if not attrs:
        return [Plain('你想问哪个城市的天气？\n')]
    ent.chain.root.clear()
    ent.meta['routiner'] = 'WeatherReportRoutiner'
    if attrs[0] in GLOBAL.unsubscribes:

        resp = requests.delete(
            internal_api('/worker/routiner'),
            json = {'ents': ent.json()}
        )
        return [Plain('不看天气预报是吧')]
    # logger.warning(attrs)
    output = fetchWeather(attrs[0])

    try:
        if attrs[1] in GLOBAL.subscribes:
            ent.meta['city'] = attrs[0]
            resp = requests.post(
                internal_api('/worker/routiner'),
                json = {'ents': ent.json()}
            )
            output.append(f'{attrs[0]}的天气推送已订阅')
    except:
        logger.error(traceback.format_exc())
    return [Plain('\n'.join(output))]

def 爬每日一句(ent: CoreEntity):
    """#每日一句 []
    爬今天的每日一句
    也可以订阅：
    用法：
        #每日一句 sub
    如需取消，请使用：
        #每日一句 cancel"""
    attrs = ent.chain.tostr().split(' ')
    ent.chain.root.clear()
    ent.meta['routiner'] = 'DailySentenceRoutiner'
    if attrs:
        if attrs[0] in GLOBAL.unsubscribes:
            requests.delete(
                internal_api('/worker/routiner'),
                json={'ents': ent.json()}
            )
            return [Plain(f'不学英语是吧')]

    w = datetime.datetime.now().weekday() + 1
    with open(f'Assets/柴郡猫猫/{w}.jpg', 'rb') as f:
        b = f.read()
    output = [Image(base64=base64.b64encode(b))]

    try:
        if attrs and attrs[0] in GLOBAL.subscribes:
            requests.post(
                internal_api('/worker/routiner'),
                json={'ents': ent.json()}
            )
            output.append(Plain(f'成功订阅每日一句推送,回复td退订'))
    except:
        print(traceback.format_exc())
    return output

def 爬what_anime(ent: CoreEntity):
    '''#搜番 []
    爬取whats_anime的番剧信息
    '''
    ret=[]

    
    # def get_prew(ret:list,info_li:list):
    #     if info_li[8]:
    #         ret.append(Plain(f'结果可能包含成人内容……\n'))
    #         return
    #     ret.append(Image(url='https://trace.moe/thumbnail.php?anilist_id={}&file={}&t={}&token={}'.format(info_li[4],info_li[5],info_li[6],info_li[7])))


    # def get_word(info):
    #     firstres=info["docs"][0]
    #     ans='\n'

    #     ans+=f"{firstres['title_chinese']} ({firstres['title']})\n"
    #     if(firstres['episode']): ans+=f"第{firstres['episode']}话\n"
    #     else: ans+='（剧场版）\n'
    #     ans+=f"起止位置：{int(firstres['from'])//60}:{int(firstres['from'])%60} - {int(firstres['to'])//60}:{int(firstres['to'])%60}\n"
    #     ans+=f"相似度：{firstres['similarity']*100:.4f}%\n"

        # return ans
    for pics in ent.chain:
        logger.debug(pics)
        if isinstance(pics, Image):
            pic_url=pics.url
            res=requests.get('https://api.trace.moe/search',params={'url':pic_url},timeout=20)
            if res.status_code==200:
                info=res.json()
                
                docs=info["result"]
                firstres=docs[0]
                ret.append(
                    Plain(
                        f'{firstres["filename"]}\n'
                        f'第{firstres["episode"]}话\n'
                        f"起止位置：{int(firstres['from'])//60}:{int(firstres['from'])%60} - {int(firstres['to'])//60}:{int(firstres['to'])%60}\n"
                        f"相似度：{firstres['similarity']*100:.4f}%\n"
                    )
                )
                ret.append(Image(url=firstres['image']))

                
                #输出文字结果
                # ret.append(Plain(get_word(info)))

            else:
                ret.append(Plain(f'搜索过程中发生了一点问题：{res.status_code}\n'))
    if not ret:
        return [Plain('您没发图哥哥！')]
    return ret

def 搜图(ent: CoreEntity):
    """#搜图 []
    fufu不在线，那交给i宝了
    格式：
        #搜图 [图片1] [图片2] ...
    参数：
        --save=typ 存入图片api，仅管理员能用
        --rec 存入待审库，给管理员过目后可以加入图片api
    """
    from fapi.models.Auth import IroriConfig
    from PIL import Image as Pimg
    ret = []
    config = IroriConfig.objects().first()
    authorized = ent.member in config.auth_masters
    logger.info(f"admin:{authorized}")
    for pic in filter(lambda x:isinstance(x, Image), ent.chain):
        imgio = BytesIO(requests.get(pic.url).content)
        img = Pimg.open(imgio).convert('RGB')
        imgio.truncate(0)
        imgio.seek(0)
        img.save(imgio, format='PNG') # 转png
        r = requests.post('http://saucenao.com/search.php',params={
            'output_type':2,
            'numres':1,
            'db':999,
            'api_key':config.api_keys['saucenao.key']
        },files={
            'file':("image.png", imgio.getvalue())
        })
        if r.status_code!=200:
            ret.append(f'搜到一半，十有八九是寄了：{r.status_code}\n{r.text}')
        else:
            j = r.json()
            logger.debug(j)
            if j['header']['results_returned']>0:
                for i in j['results']:
                    h, d = i['header'], i['data']
                    res = [
                        f"相似度：{h['similarity']}",
                        f"作者：{d.get('member_name', d.get('creator', '<不详>'))}",
                        f"标题：{d.get('jp_name', d.get('title', '<不详>'))}",
                        '\n'.join(d.get('ext_urls', ''))
                    ]
                    ret.append('\n'.join(res))

            else:
                ret.append('无结果')
    return '\n\n'.join((f"#{p+1} {i}" for p,i in enumerate(ret)))

def 开车(ent: CoreEntity):
    """#开车 [#car]
    fufu不在线，那交给i宝了vol.2
    格式:
        #开车 <typ>
        typ可选字段:
            nice   开好车
            ero    开痛车
            kusa   开灵车
            kawaii 开校车
            tank   开战车
    
    """
    from cfg import setu_api
    typ = ent.chain.pop_first_cmd()
    allow = [
        'ero', 
        'kawaii', 
        'nice', 
        'tank',
        'kusa'
    ]
    if not typ:
        typ = 'nice'
    if typ == 'tank':
        return Image(url=setu_api + 'autotank')
    if typ not in allow:
        return f'交警提示：您的车型{typ}不能上路'

    j = requests.get(setu_api + f'random?typ={typ}').json()
    return [
        Image(url=setu_api + f'bin/{j["id"]}'),
        Plain(
f"""{j['title']}
https://www.pixiv.net/artworks/{j['id']}""")]


def 刷CF(ent: CoreEntity):
    """#刷CF []
    爬取给定用户的做题记录。
    用例：#刷CF bot_yaya"""
    attrs = ent.chain.tostr().split(' ')
    usr = attrs[0]
    res = requests.get(f'https://codeforces.com/api/user.status?handle={usr}')

    j = res.json()
    problems = {}
    accept_count = 0
    tried_count = 0

    for i in j['result']:
        na = i.get('problemsetName', '')
        na = i.get('contestId', na)
        ind = i.get('index', '')
        identity = f'{na}{ind}'
        verdict = i.get('verdict', '')
        if identity in problems:
            if problems[identity] == 'OK': continue
            elif verdict == 'OK':
                accept_count += 1
                tried_count -= 1
                problems[identity] = 'OK'
        else:
            if verdict == 'OK':
                accept_count += 1
                problems[identity] = 'OK'
            else:
                tried_count += 1
                problems[identity] = verdict
    return [Plain(
        f"""用户{usr}的CF刷题记录：
    通过{accept_count}题
    试过{tried_count}题"""
    )]

def 对(ent: CoreEntity):
    """#对 []
    给出上句对下句"""
    couplet_hds = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cache-Control":"no-cache",
        "Connection":"keep-alive",
        "DNT":"1",
        "Host":"ai-backend.binwang.me",
        "Origin":"https://ai.binwang.me",
        "Pragma":"no-cache",
        "Referer":"https://ai.binwang.me/couplet/",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-site",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    couplet_lnk = f"https://ai-backend.binwang.me/chat/couplet/{ent.chain.tostr().strip()}"
    resp = requests.get(couplet_lnk, headers=couplet_hds).json()['output']
    return [Plain(resp)]


functionMap = {
}

shortMap = {
}

functionDescript = {
}