import os
import requests
import asyncio
import datetime
from mirai import Mirai, Plain, MessageChain, Friend, Face, MessageChain,Group,Image,Member,At
from mirai.face import QQFaces
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import traceback
import random
import string
import functools
import GLOBAL
import json

async def CFLoopRoutiner():
    print('进入回环(CF')
    if not os.path.exists('CF/'):
        os.mkdir('CF/')
    while 1:
        if any([_ for _ in os.listdir('CF/') if _[-4:]!='.png']):
            j = fetchCodeForcesContests()
            for _ in os.listdir('CF/'):
                try:
                    if _[-4:]!='.png':
                        CFNoticeManager(j,gp=int(_))
                except:
                    print('CF爬虫挂了！',traceback.format_exc())
        await asyncio.sleep(86400)

async def ATLoopRoutiner():
    print('进入回环(AT')
    if not os.path.exists('AtCoder/'):
        os.mkdir('AtCoder/')
    while 1:
        if any([_ for _ in os.listdir('AtCoder/') if _[-4:]!='.png']):
            j = fetchAtCoderContests()
            for _ in os.listdir('AtCoder/'):
                try:
                    if _[-4:]!='.png':
                        OTNoticeManager(j['upcoming'],gp=int(_))
                except:
                    print('AT爬虫挂了！',traceback.format_exc())
        await asyncio.sleep(86400)

async def NCLoopRoutiner():
    print('进入回环(NC')
    if not os.path.exists('NowCoder/'):
        os.mkdir('NowCoder/')
    while 1:
        if any([_ for _ in os.listdir('NowCoder/') if _[-4:]!='.png']):
            j = fetchNowCoderContests()
            for _ in os.listdir('NowCoder/'):
                try:
                    if _[-4:]!='.png':
                        OTNoticeManager(j,gp=int(_))
                except:
                    print('NC爬虫挂了！',traceback.format_exc())
        await asyncio.sleep(86400)

async def rmTmpFile(fi:str):
    await asyncio.sleep(60)
    os.remove(fi)

async def contestsBeginNotice(g,contest,ti):
    if ti<0:
        return
    print('进入等待队列，阻塞%f秒'%ti)
    await asyncio.sleep(ti)
    await GLOBAL.app.sendGroupMessage(g,[Plain(text='比赛%s还有不到一个小时就要开始了...'%contest)])

async def CFProblemRender(g,cid,ti):
    FN='CF/%s.png' % cid
    print('在%f秒后渲染比赛'%ti+cid+'的问题图片')
    if cid in GLOBAL.CFRenderFlag or os.path.exists(FN): #有队列在做了
        await asyncio.sleep(ti)
        if not os.path.exists(FN):
            await asyncio.sleep(20)
        await GLOBAL.app.sendGroupMessage(g,[Image.fromFileSystem(FN)])
    else:
        GLOBAL.CFRenderFlag.add(cid)
        await asyncio.sleep(ti)
        base = 'https://codeforces.com/contest/'+cid+'/problems'
        l = renderHtml(base,FN)
        GLOBAL.CFRenderFlag.discard(ti)
        l.append(Image.fromFileSystem(FN))
        await GLOBAL.app.sendGroupMessage(g,l)

async def fuzzT(g,s,e,w):
    for _ in range(s,e):
        if _%10==0:
            await asyncio.sleep(0.2)
        await GLOBAL.app.sendGroupMessage(g,[Plain(f'{chr(_)}{_}{w}')])


async def msgDistributer(**kwargs):
    if 'msg' in kwargs and kwargs['msg']:
        if kwargs.get('typ','P') == 'E':
            seq = [Face(QQFaces[kwargs['msg']])]
        elif kwargs.get('typ','P') == 'I':
            f_n = randstr(8)
            with open(f_n,'wb') as f:
                f.write(kwargs['msg'])
            seq = [Image.fromFileSystem(f_n)]
            # seq = [Image.fromFileSystem(kwargs['msg'])]
        else:
            seq = [Plain(kwargs['msg'])]

        if 'gp' in kwargs:
            await GLOBAL.app.sendGroupMessage(kwargs['gp'],seq)
        else:
            await GLOBAL.app.sendFriendMessage(kwargs['mem'],seq)

def tnow():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=8)

def randstr(l:int) -> str:
    return ''.join(random.sample(string.ascii_letters*l+string.digits*l,l))

def renderHtml(dst_lnk,na):
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-gpu')
    option.add_argument("--window-size=1280,1024")
    option.add_argument("--hide-scrollbars")
    
    driver = webdriver.Chrome(options=option)
    
    driver.get(dst_lnk)
    ostr = []
    ostr.append(Plain(text=driver.title))
    location = driver.execute_script('return window.location.href')
    ostr.append(Plain(text=location))
    
    scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    if scroll_height*scroll_width > GLOBAL.webPngLimit:
        if scroll_width >= GLOBAL.webPngLimit:
            driver.quit()
            ostr.append(Plain(text='我画不了这么鬼畜的页面OxO'))
            return ostr
        else:
            if 'codeforces' in dst_lnk:
                scroll_height = min(GLOBAL.webPngLimit*10//scroll_width,scroll_height)
            else:
                scroll_height = GLOBAL.webPngLimit//scroll_width
    if 'moegirl' in dst_lnk:
        driver.execute_script('''var o=document.querySelectorAll('.heimu');for(var i=0;i<o.length;i++){o[i].style.color="#FFF"}''')
        driver.execute_script('''var o=document.querySelectorAll('a');for(var i=0;i<o.length;i++){o[i].style.color="#0AF"}''')
    driver.set_window_size(scroll_width, scroll_height)
    driver.get_screenshot_as_file(na)
    driver.quit()
    return ostr

def getPlayer(**kwargs):
    if 'gp' in kwargs:
        try:
            player = kwargs['gp'].id + 2**39
        except:
            player = kwargs['gp'] + 2**39
    else:
        try:
            player = kwargs['mem'].id
        except:
            player = kwargs['mem']
    return player

def clearCFFuture(G,key,src):
    CFNoticeQueue = GLOBAL.CFNoticeQueueGlobal.setdefault(src,{})
    try:
        print('清除成功',CFNoticeQueue.pop(key))
    except:
        print('无',G)

def clearOTFuture(G,key,src):

    t = GLOBAL.OTNoticeQueueGlobal.setdefault(src,{})
    try:
        print('清除成功',t.pop(key))
    except:
        print('无',G)

def CFNoticeManager(j,**kwargs):
    try:
        gp = kwargs['gp'].id
    except:
        gp = kwargs['gp']
    fn = f"CF/{gp}"
    with open(fn,'r') as f:
        feat = f.readline().strip()
    CFNoticeQueue = GLOBAL.CFNoticeQueueGlobal.setdefault(gp,{})
    print(j)
    for k,v in j.items():
        timew = None
        if k not in CFNoticeQueue:
            
            if 'routine' in v:
                timew = v['routine'] - tnow() - datetime.timedelta(hours=1)
                asy = asyncio.ensure_future(contestsBeginNotice(gp,v['title'],timew.total_seconds()))
                CFNoticeQueue[k] = asy
                asy.add_done_callback(functools.partial(clearCFFuture,k,gp))
        if timew and feat == 'R' and k + 'RDR' not in CFNoticeQueue:
            asyR = asyncio.ensure_future(CFProblemRender(gp,k,timew.total_seconds()+3640))
            CFNoticeQueue[k + 'RDR']=asyR
            asyR.add_done_callback(functools.partial(clearCFFuture,k + 'RDR',gp))
        elif feat == 'Y' and k + 'RDR' in CFNoticeQueue:
            t = CFNoticeQueue.pop(k + 'RDR')
            t.cancel()

def OTNoticeManager(j,**kwargs):
    try:
        gp = kwargs['gp'].id
    except:
        gp = kwargs['gp']

    OtherOJNoticeQueue = GLOBAL.OTNoticeQueueGlobal.setdefault(gp,{})

    for k in j:
        if k['title'] not in OtherOJNoticeQueue:
            timew = k['begin'] - tnow() - datetime.timedelta(hours=1)
            asy = asyncio.ensure_future(contestsBeginNotice(gp,k['title'],timew.total_seconds()))
            OtherOJNoticeQueue[k['title']] = asy
            asy.add_done_callback(functools.partial(clearOTFuture,k['title'],gp))
    print(OtherOJNoticeQueue)

def fetchCodeForcesContests():
    r = requests.get('https://codeforces.com/contests?complete=true')
    print(r)
    soup = BeautifulSoup(r.text,'html.parser')
    li = {}
    for i in soup('table')[0]('tr'):

        if any(i('td')): #标题 作者 日期 时长 开始倒计时 （爬到的是UTC+3
            contest = li.setdefault(i['data-contestid'],{})
            
            pos = i('td')[0].text.find('Enter')
            if pos!=-1:
                print('正在运行的比赛')
                contest['title'] = i('td')[0].text[:pos-1].strip()
            else:
                try:
                    contest['title'] = i('td')[0].string.strip()
                    contest['authors'] = [au.string.strip() for au in i('td')[1]('a')]
                    contest['routine'] = datetime.datetime.strptime(i('td')[2].a.span.string.strip(),'%b/%d/%Y %H:%M') + datetime.timedelta(hours=5)
                    contest['length'] = i('td')[3].string.strip()
                    contest['countdown'] = i('td')[4].text.strip()
                    
                except:
                    print(traceback.format_exc())
    return li

def fetchAtCoderContests() -> dict:
    j = {}
    l = []
    r = requests.get('https://atcoder.jp/contests/',headers = GLOBAL.AtCoderHeaders)
    s = BeautifulSoup(r.text,'html.parser')
    try:
        for p,i in enumerate(s.find('h3',string='Active Contests').next_sibling.next_sibling('tr')):
            if p:
                l.append({
                'length':i('td')[2].text,
                'ranking_range':i('td')[3].text,
                'title':i('a')[1].text,
                'begin':datetime.datetime.strptime(i('a')[0].text,"%Y-%m-%d %H:%M:%S+0900") - datetime.timedelta(hours=1)
                })
    except:
        pass
    j['running'] = l
    l = []

    for p,i in enumerate(s.find('h3',string='Upcoming Contests').next_sibling.next_sibling('tr')):# 持续时间 排名区间 比赛名 比赛时间
        if p:
            l.append({
                'length':i('td')[2].text,
                'ranking_range':i('td')[3].text,
                'title':i('a')[1].text,
                'begin':datetime.datetime.strptime(i('a')[0].text,"%Y-%m-%d %H:%M:%S+0900") - datetime.timedelta(hours=1)
                })

    j['upcoming'] = l
    print(j)
    return j

def fetchNowCoderContests() -> list:
    l = []
    res = requests.get('https://ac.nowcoder.com/acm/contest/vip-index?&headNav=www')
    bs_res = BeautifulSoup(res.text,'html.parser')
    items = bs_res.find('div',class_='platform-mod js-current')
    for item in items.find_all(class_='platform-item'):
        ans = item.find(class_='platform-item-cont')
        contest_name = ans.find('a',target='_blank').text
        contest_time = ans.find('li',class_='match-time-icon').text
        li = contest_time.split('\n')
        d = datetime.datetime.strptime(li[0],"比赛时间：%Y-%m-%d %H:%M")
        l.append({
            "title":contest_name,
            "begin":d,
            "length":li[2].strip()
        })
    return l

def uploadToChaoXing(fn:str) -> str:
    lnk = 'http://notice.chaoxing.com/pc/files/uploadNoticeFile'
    with open(fn,'rb') as f:
        r = requests.post(lnk,files = {'attrFile':f})
    j = json.loads(r.text)
    return j['att_file']['att_clouddisk']['downPath']

def comb(n,b):
    res = 1
    b = min(b,n-b)
    for i in range(b):
        res=res*(n-i)//(i+1)
    return res

def quickpow(x,p,m = -1):
    res = 1
    if m == -1:
        while p:
            if p&1:
                res = res * a
            a = a*a
            p>>=1
    else:
        while p:
            if p&1:
                res = res * a % mo
            a = a*a%mo
            p>>=1
    return res

def exgcd(a,b):
    if not b:
        return 1,0
    y,x = exgcd(b,a%b)
    y -= a//b * x
    return x,y

def getinv(a,m):
    x,y = exgcd(a,m)
    return x%m
    
