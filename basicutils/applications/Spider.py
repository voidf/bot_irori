"""爬虫类"""
import os
import sys

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

import basicutils.CONST as GLOBAL


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

# async def 没救了(*attrs,kwargs={}):
#     r = requests.get(f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{tnow().strftime("%m-%d-%Y")}.csv',proxies=GLOBAL.proxy)
#     if r.status_code==404:
#         print('没有今天的')
#         r = requests.get(f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{(tnow()-datetime.timedelta(days=1)).strftime("%m-%d-%Y")}.csv',proxies=GLOBAL.proxy)
#     if r.status_code==404:
#         print('没有昨天的')
#         r = requests.get(f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{(tnow()-datetime.timedelta(days=2)).strftime("%m-%d-%Y")}.csv',proxies=GLOBAL.proxy)
#         print(f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{(tnow()-datetime.timedelta(days=1)).strftime("%m-%d-%Y")}.csv')
#         #print(r.text)
#     if r.status_code!=200:
#         return [Plain('别看了，没救了')]
#     c = csv.reader(io.StringIO(r.text))
#     s = []
#     d = {}
#     for i in c:
#         if i[0]=='FIPS':
#             t=[]
#             #t.append('国家或地区')
#             #t.append('更具体一点')
#             t.append('累计')
#             t.append('死亡')
#             t.append('治愈')
#             t.append('患者')
#             s.append('\t\t\t'.join(t))
#         else:
#             it = d.setdefault(i[3],[0,0,0,0])
#             it[0]+=int(i[-7])
#             it[1]+=int(i[-6])
#             it[2]+=int(i[-5])
#             it[3]+=int(i[-4])
#     for k,v in sorted(d.items(),key=lambda x: x[1][0],reverse=True):
#         #s.append(f'{k}\t{v[0]}\t{v[1]}\t{v[2]}\t{v[3]}')
#         s.append("""{0}:\n{1:{5}<10.10}{2:{5}<10.10}{3:{5}<10.10}{4:{5}<10.10}""".format(k,str(v[0]),str(v[1]),str(v[2]),str(v[3]),chr(8214)))
#         #s.append("""{0:_<30.30}{1:_<37.37}{2:_<10.10}{3:_<10.10}{4:_<10.10}{5:_<10.10}""".format(i[3],i[2],i[-5],i[-4],i[-3],i[-2]))

#     return [Plain('\n\n'.join(s))]

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

from basicutils.algorithms import randstr

def 爬OIWiki(ent: CoreEntity, kwargs):

    lnk = 'https://oi-wiki.org/'
    query = ent.chain.tostr()
    if query:
        plnk = 'https://search.oi-wiki.org:8443/?s=' + query
        j = json.loads(requests.get(plnk).text)
        ostr = [Plain(text='找到了%d个类似的东西\n'%len(j))]
        if len(j):
            c = j[0]
            ostr.append(Plain(text='直接把%s扔给你了\n'%c['title']))
            suflnk = c['url']
        else:
            ostr.append(Plain(text='无结果'))
            return ostr
    else:
        ostr = []
        if random.choice([True,False]):
            r = requests.get(lnk, headers=GLOBAL.OIWikiHeaders)
            r.encoding = 'utf-8'

            s = BeautifulSoup(r.text, 'html.parser')
            res = s.find('nav', attrs={'data-md-component': 'tabs'})

            hdir = random.choice(res('a')[2:-2])
            subRes = s.find('label',string=hdir.string,attrs={'class':'md-nav__link'})

            hd2 = random.choice(list(subRes.next_siblings)[1]('li',attrs={'class':'md-nav__item'}))
            suflnk = hd2.a['href']
        else:
            lnk = 'https://ctf-wiki.github.io/ctf-wiki/'
            r = requests.get(lnk, headers=GLOBAL.OIWikiHeaders)
            r.encoding = 'utf-8'

            s = BeautifulSoup(r.text, 'html.parser')
            res = s.find('nav', attrs={'data-md-component': 'tabs'})

            hdir = random.choice(res('a')[1:])
            subRes = [i for i in s('label',attrs={'class':'md-nav__link','for':re.compile('nav-[0-9]*$')}) if hdir.string.strip() in i.text][0]

            hd2 = random.choice(list(subRes.next_siblings)[1]('li',attrs={'class':'md-nav__item'}))
            suflnk = hd2.a['href']

    url=lnk+suflnk
    print(url)

    # save_fn=randstr(GLOBAL.randomStrLength)+"tmpLearn"+str(kwargs['gp'].id)+'.png'
    # ostr += await renderHtml(url,save_fn)
    
    # asyncio.ensure_future(rmTmpFile(save_fn),loop=None)
    # ostr.append(generateImageFromFile(save_fn))
    return ostr

async def 爬萌娘(*attrs,kwargs={}):
    lnk = 'https://zh.moegirl.org/Special:%E9%9A%8F%E6%9C%BA%E9%A1%B5%E9%9D%A2'
    if len(attrs):
        keyWord = ' '.join(attrs)
        r = requests.get('https://zh.moegirl.org/index.php?title=Special:搜索&go=前往&search='+keyWord,headers=GLOBAL.moeGirlHeaders)
        r.encoding = 'utf-8'
        s = BeautifulSoup(r.text, 'html.parser')
        res = s.find('ul', attrs={'class': 'mw-search-results'})
        if res is None:
            if len(r.history):
                lnk = r.url
            else:
                tlnk = 'https://zh.moegirl.org/' + keyWord
                if requests.get(tlnk).status_code == 404:
                    return [Plain(text=random.choice(['这不萌娘','在萌娘找不到这玩意']))]
                else:
                    lnk = tlnk
        else:
            lnk = 'https://zh.moegirl.org'+res.find('a')['href']
    save_fn=randstr(GLOBAL.randomStrLength)+"tmpMoe"+str(kwargs['mem'].id)+'.png'
    l = await renderHtml(lnk, save_fn)
    asyncio.ensure_future(rmTmpFile(save_fn),loop=None)
    return l+[generateImageFromFile(save_fn)]

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
        TD  （取消提醒）
        sub （订阅提醒）"""
    attrs = ent.chain.tostr().split(' ')
    ent.chain.__root__.clear()
    ent.meta['routiner'] = 'CodeforcesRoutinuer'
    li = []
    if len(attrs):
        if attrs[0] in GLOBAL.unsubscribes:
            resp = requests.delete(
                server_api('/worker/routiner'),
                json={'ents': ent.json()}
            )
            if resp.status_code!=200:
                return resp.text
            return [Plain('取消本群的CodeForces比赛提醒服务')]
        elif attrs[0] in GLOBAL.subscribes:
            resp = requests.post(
                server_api('/worker/routiner'),
                json={'ents': ent.json()}
            )
            if resp.status_code!=200:
                return resp.text
            li.append(Plain('已订阅Codeforces比赛提醒推送\n'))
    
    li.append(Plain(text='{:<10}\n{:<10}\n{:<10}\n{:<15}\n\n'.format('名称', '开始时间', '比赛时长', '倒计时')))
    resp = requests.get('https://codeforces.com/api/contest.list').json()['result']
    for i in resp:
        if i['phase'] == 'FINISHED':
            break
        li.append(
            Plain(
                '{:<10}\n{:<10}\n{:<10}\n{:<15}\n\n'.format(
                    i['name'], 
                    str(datetime.datetime.fromtimestamp(i['startTimeSeconds'])), 
                    f"{i['durationSeconds'] / 60}min" , 
                    str(datetime.timedelta(seconds=-i['relativeTimeSeconds']))
                )
            )
        )
    if not li:
        li = '没有即将开始的比赛'
    return li

async def 爬AtCoder(*attrs,kwargs={}):
    try:
        gp = kwargs['gp'].id
    except:
        gp = kwargs['gp']

    player = getPlayer(**kwargs)
    ATNoticeQueue = GLOBAL.OTNoticeQueueGlobal.setdefault(gp,{})
            
    if len(attrs):
        if attrs[0] in GLOBAL.unsubscribes:
            ATCoderSubscribe.chk(player).delete()
            return [Plain('取消本群的AtCoder比赛提醒服务')]
    else:
        ATCoderSubscribe.chk(player)
    li = []
    if ATCoderSubscribe.objects(pk=Player.chk(player)):
        ATData = fetchAtCoderContests()
        if ATData['running']:
            li.append(Plain('正在运行的比赛：\n'))
            for cont in ATData['running']:
                li.append(Plain(f"{cont['title']} {cont['ranking_range']} {cont['length']} {cont['begin'].strftime('%Y/%b/%d %H:%M')}\n"))
        li.append(Plain('将来的比赛：\n'))
        for cont in ATData['upcoming']:
            li.append(Plain(f"{cont['title']} {cont['ranking_range']} {cont['length']} {cont['begin'].strftime('%Y/%b/%d %H:%M')}\n"))
            cont['title'] = '【AT】'+cont['title']
        OTNoticeManager(ATData['upcoming'],**kwargs)
        li.append(Plain('已自动订阅AtCoder的比赛提醒服务，取消请使用#AT reset'))
    return li

def 爬LaTeX(ent: CoreEntity):
    """#LaTeX [#tex, #latex]
    爬自https://latex.vimsky.com，我不会写LaTeX，炸了说一下我看看
    """
    base = r'\dpi{150} \bg_white \large ' + ent.chain.tostr().replace('+','&plus;')
    lnk = 'https://latex.vimsky.com/test.image.latex.php?fmt=png&dl=0&val='+urllib.parse.quote(urllib.parse.quote(base))
    return Image(url=lnk)

async def 爬牛客(*attrs,kwargs={}):
    try:
        gp = kwargs['gp'].id
    except:
        gp = kwargs['gp']
    player = getPlayer(**kwargs)
    
    NCNoticeQueue = GLOBAL.OTNoticeQueueGlobal.setdefault(gp,{})
            
    if len(attrs):
        if attrs[0] in GLOBAL.unsubscribes:
            NowCoderSubscribe.chk(player).delete()
            return [Plain('取消本群的牛客比赛提醒服务')]
    else:
        NowCoderSubscribe.chk(player)
    li = []
    if NowCoderSubscribe.objects(pk=Player.chk(player)):
        NCData = fetchNowCoderContests()
        for i in NCData:
            li.append(Plain(i['title']+'\n'))
            li.append(Plain(f"{i['begin']}"+'\t'))
            li.append(Plain(i['length']+'\n\n'))
            i['title'] = '【牛客】' + i['title']

        OTNoticeManager(NCData,**kwargs)
        
        li.append(Plain('已自动订阅牛客的比赛提醒服务，取消请使用#NC reset'))

    return li
        
async def 爬歌(*attrs,kwargs={}):
    keyword = urllib.parse.quote(''.join(attrs))
    ans = []
    lnks = []
    try:
        kuwolnk = f'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={keyword}&pn=1&rn=30'

        ses = requests.session()

        r = ses.get(f'http://kuwo.cn/search/list?key={keyword}')

        r = ses.get(kuwolnk, headers={
            'referer': f'http://www.kuwo.cn/search/list?key={keyword}',
            'csrf': f"{ses.cookies.get('kw_token')}"
        })

        j = json.loads(r.text)
        mid = j['data']['list'][0]['musicrid']

        url = f'http://antiserver.kuwo.cn/anti.s?type=convert_url&format=mp3&response=url&rid={mid}'
        r = requests.get(url,headers = {
            'user-agent': 'okhttp/3.10.0'
        })
        print(r.text)
        ans.append('酷我：')
        ans.append(j['data']['list'][0]['name']+' '+j['data']['list'][0]['artist'])
        ans.append(r.text)
        lnks.append(ans[-1])
        ans.append('')
    except:
        ans.append('酷我炸了')
        print(traceback.format_exc())

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

    try:
        xiamihds = {'referer': 'https://h.xiami.com/'}
        ses = requests.session()
        ses.get('https://www.xiami.com')
        lnk = f'http://api.xiami.com/web?v=2.0&app_key=1&key={keyword}&page=1&limit=20&r=search/songs'
        r = ses.get(lnk,headers=xiamihds)
        j = json.loads(r.text) # 这个是搜音乐信息
        print(f'虾米 => {j}')
        fid = j['data']['songs'][0]['song_id']
        fname = j['data']['songs'][0]['song_name'] + '-' + j['data']['songs'][0]['artist_name']

        lnk2 = f'https://api.xiami.com/web?v=2.0&app_key=1&id={fid}&r=song/detail'
        rr = ses.get(lnk2,headers=xiamihds)
        print(rr.text)
        print(json.loads(rr.text)['data']['song']['listen_file'])
        ans.append('虾米：')
        ans.append(fname)
        ans.append(json.loads(rr.text)['data']['song']['listen_file'])
        lnks.append(ans[-1])
        ans.append('')
    except:
        ans.append('虾米炸了')
        print(traceback.format_exc())
    try:
        hds = {
            'origin': 'http://y.qq.com/',
            'referer': 'http://y.qq.com/',
            # 'cookie': 'uin=; qm_keyst='
        }
        lnk = f'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.center&searchid=46804741196796149&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w={keyword}&g_tk=5381&jsonpCallback=MusicJsonCallback10005317669353331&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
        r = ses.get(lnk)
        j = json.loads(r.text[35:-1])  # 这个是搜音乐信息
        fid = j['data']['song']['list'][0]['mid']
        ffid = j['data']['song']['list'][0]['file']['media_mid']
        fname = j['data']['song']['list'][0]['title'] + '-' + \
            j['data']['song']['list'][0]['singer'][0]['name']

        d = {
            'req_0': {
                'module': 'vkey.GetVkeyServer',
                'method': 'CgiGetVkey',
                'param': {
                    'guid': '7332953645',
                    'loginflag': 1,
                    'filename': [f'M500{ffid}.mp3'],
                    'songmid': [fid],
                    'songtype': [0],
                    'uin': '0',
                    'platform': '20'
                }
            }
        }

        lnk2 = f'https://u.y.qq.com/cgi-bin/musicu.fcg?data={urllib.parse.quote(json.dumps(d))}'
        rr = ses.get(lnk2, headers=hds)
        jj = json.loads(rr.text)['req_0']['data']
        sip = jj['sip'][0]

        if jj['midurlinfo'][0]['purl']:
            ans.append('QQ：')
            ans.append(fname)
            ans.append(sip+jj['midurlinfo'][0]['purl'])
            lnks.append(ans[-1])
            ans.append('')
        else:
            raise NameError('QQ没权限拿歌')
    except:
        ans.append('mhtsl')
        print(traceback.format_exc())
    print(ans)
    print(lnks)
    kwargs['voices'] = lnks
    # if 'gp' in kwargs:
    #     voices = [
    #         GLOBAL.app.uploadVoice(getFileBytes(i)) for i in lnks
    #     ]
    #     return [Plain('\n'.join(ans))]+voices
    return [Plain('\n'.join(ans))]#+[Voice(url=i) for i in lnks]

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
    ent.chain.__root__.clear()
    ent.meta['routiner'] = 'WeatherReportRoutinuer'
    if attrs[0] in GLOBAL.unsubscribes:

        resp = requests.delete(
            server_api('/worker/routiner'),
            json = {'ents': ent.json()}
        )
        return [Plain('不看天气预报是吧')]
    # logger.warning(attrs)
    output = fetchWeather(attrs[0])

    try:
        if attrs[1] in GLOBAL.subscribes:
            ent.meta['city'] = attrs[0]
            resp = requests.post(
                server_api('/worker/routiner'),
                json = {'ents': ent.json()}
            )
            output.append(f'从现在开始每天0点i宝会告诉你{attrs[0]}的天气情况哦！')
    except:
        logging.error(traceback.format_exc())
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
    ent.chain.__root__.clear()
    ent.meta['routiner'] = 'DailySentenceRoutinuer'
    if attrs:
        if attrs[0] in GLOBAL.unsubscribes:
            requests.delete(
                server_api('/worker/routiner'),
                json={'ents': ent.json()}
            )
            return [Plain(f'不学英语是吧')]
    r = requests.get(
        f'http://sentence.iciba.com/index.php?c=dailysentence&m=getTodaySentence&_={int(datetime.datetime.now().timestamp()*1000)}')
    j = json.loads(r.text)
    output = [Plain(j['content']+'\n'+j['note']), Image(url=j['picture']), Voice(url=convert_to_amr('mp3', j['tts']))]
    # , Voice(url=j['tts'])

    print(output)
    try:
        if attrs and attrs[0] in GLOBAL.subscribes:
            requests.post(
                server_api('/worker/routiner'),
                json={'ents': ent.json()}
            )
            output.append(Plain(f'成功订阅每日一句推送,回复td退订'))
    except:
        print(traceback.format_exc())
    return output

# async def 爬ip(*attrs,kwargs={}):
#     if not attrs:
#         return [Plain('没有输入ip哦\n'+SpiderDescript['#ip'])]
#     ip = attrs[0]
#     lnk = f'https://ip.51240.com/{ip}__ip/'

#     r = requests.get(lnk)

#     rr = re.findall(f'''<tr><td height="25" bgcolor="#FFFFFF" style="text-align: center">(.*?)</td><td bgcolor="#FFFFFF" style="text-align: center">(.*?)</td></tr>''' ,r.text)
#     if not rr:
#         rr = re.findall(f'''<tr><td height="25" colspan="2" bgcolor="#FFD7D7" style="text-align: center;color: #F00;">(.*?)</td></tr></table>''',r.text)
#     if not rr:
#         return [Plain('输入有点问题？我找着找着找炸了')]
#     ans = [' '.join(i) for i in rr]
#     return [Plain('\n'.join(ans))]

# async def 反爬ip(*attrs,kwargs={}):
#     if not attrs:
#         return [Plain('没有输入地址哦\n'+SpiderDescript['#addr'])]
#     kw = ' '.join(attrs)
#     lnk = f'https://ip.51240.com/?dz={kw}'

#     r = requests.get(lnk)
#     rr = re.findall(f'''<tr><td height="25" bgcolor="#FFFFFF" style="text-align: center">(.*?)</td><td bgcolor="#FFFFFF" style="text-align: center">(.*?)</td></tr>''' ,r.text)
#     if not rr:
#         rr = re.findall(f'''<tr><td height="25" colspan="2" bgcolor="#FFD7D7" style="text-align: center;color: #F00;">(.*?)</td></tr></table>''',r.text)
#     if not rr:
#         return [Plain('输入有点问题？我找着找着找炸了')]
#     ans = [' '.join(i) for i in rr]
#     return [Plain('\n'.join(ans))]

def 爬what_anime(ent: CoreEntity):
    '''#搜番 []
    爬取whats_anime的番剧信息
    '''
    ret=[]
    def get_info(info):
        docs=info["docs"]
        firstres=docs[0]

        li=[
            firstres['title'],
            firstres['title_chinese'],
            firstres['title_english'],
            firstres['episode'],

            firstres['anilist_id'],
            firstres['filename'],
            firstres['at'],
            firstres['tokenthumb'],

            firstres['is_adult']
        ]
        return li
    
    def get_prew(ret:list,info_li:list):
        if info_li[8]:
            ret.append(Plain(f'结果可能包含成人内容……\n'))
            return
        ret.append(Image(url='https://trace.moe/thumbnail.php?anilist_id={}&file={}&t={}&token={}'.format(info_li[4],info_li[5],info_li[6],info_li[7])))
        #res2=requests.get(f'https://media.trace.moe/video/{info_li[4]}/{info_li[5]}?t={info_li[6]}&token={info_li[7]}',timeout=20)
        
        # if res2.status_code==200:
        #     prew = f"tmpAni{randstr(3)}.png"
        #     #prew=f'tmpVideo_{randstr(3)}.mp4'
        #     with open(prew,'wb') as prew_f:
        #         prew_f.write(res2.content)
        #     asyncio.ensure_future(rmTmpFile(prew))
        #     ret.append(generateImageFromFile(prew))
        # else:
        #     ret.append(Plain(f'抓图过程中发生了一点差错:{res2.status_code}\n'))

    def get_word(info):
        firstres=info["docs"][0]
        ans='\n'

        ans+=f"{firstres['title_chinese']} ({firstres['title']})\n"
        if(firstres['episode']): ans+=f"第{firstres['episode']}话\n"
        else: ans+='（剧场版）\n'
        ans+=f"起止位置：{int(firstres['from'])//60}:{int(firstres['from'])%60} - {int(firstres['to'])//60}:{int(firstres['to'])%60}\n"
        ans+=f"相似度：{firstres['similarity']*100:.4f}%\n"

        return ans
    for pics in ent.chain:
        logger.debug(pics)
        if isinstance(pics, Image):
            pic_url=pics.url
            res=requests.get('https://trace.moe/api/search',params={'url':pic_url},timeout=20)
            if res.status_code==200:
                info=res.json()
                info_li=get_info(info) #用于找图

                #找图
                get_prew(ret,info_li)
                
                #输出文字结果
                ret.append(Plain(get_word(info)))

            else:
                ret.append(Plain(f'搜索过程中发生了一点问题：{res.status_code}'))
    if not ret:
        return [Plain('您没发图哥哥！')]
    return ret

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
    # '#看看病':没救了,
    '#什么值得学':爬OIWiki,
    '#什么值得娘':爬萌娘,
    '#什么值得听':爬歌,
    '#AT':爬AtCoder,
    '#牛客':爬牛客,
    # '#ip':爬ip,
    # '#addr':反爬ip,
    # '#每日一句':爬每日一句,
    '#搜番':爬what_anime
}

shortMap = {
    '#xx':'#什么值得学',
    '#moe':'#什么值得娘',
    '#什么值得d':'#什么值得娘',
    '#什么值得萌':'#什么值得娘',
    # '#什么值得医':'#看看病',
    # '#救命':'#看看病',
    '#NC':'#牛客',
    '#uta':'#什么值得听',
    '#music':'#什么值得听',

}

functionDescript = {
    '#什么值得学':'传参即在OI-Wiki搜索条目，不传参随便从OI或者CTFWiki爬点什么\n例:#什么值得学 后缀自动机【开发笔记：用此功能需要安装https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb，以及从http://npm.taobao.org/mirrors/chromedriver选择好对应版本放进/usr/bin里面，修完依赖启动记得传参--no-sandbox，还要把字体打包扔到/usr/share/fonts/truetype】\n==一条条渲染完了才会发送，老师傅们放过学生机吧TUT==',
    '#什么值得娘':'传参即在萌百爬取搜索结果，不传参即随便从萌娘爬点什么，例:#什么值得娘 リゼ・ヘルエスタ',

    '#看看病':'从jhu看板爬目前各个国家疫情的数据',
    '#AT':
"""
爬取AtCoder将要开始的比赛的时间表
可用参数:
    reset（取消提醒）
""",
    '#牛客':
"""
爬取牛客将要开始的比赛的时间表
感谢@Kevin010304提供的爬虫
可用参数:
    reset（取消提醒）
""",
    '#什么值得听':'根据给定关键词从几个平台爬歌（以后会更新更多平台的咕（危（虾米好像很容易ban人',
    '#ip':'根据给定ip地址查询地理地址。例: #ip 19.19.8.10',
    '#addr':'根据给定地址爬ip。例：#addr 谷歌',
    
}