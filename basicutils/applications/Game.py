"""小游戏类"""
import os
import sys

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from io import BytesIO
from basicutils.media import *
from PIL import Image as PImage
import asyncio
import requests
import numpy
import random
import copy
from basicutils.chain import *
from basicutils.network import *
import basicutils.CONST as GLOBAL
from basicutils.database import *
from mongoengine import *
from fapi.models.Player import *

class Asobi2048Data(RefPlayerBase, Document):
    mat = ListField(ListField(IntField()))


def asobi2048(ent: CoreEntity):
    """#2048 []
    开始2048游戏，wasd控制移动方向，init用于初始化，传参gamestart进入快速操作模式（慎用
    可用参数：
        w:向上滑动
        a:向左滑动
        s:向下滑动
        d:向右滑动
        init [(可选)2~8]:初始化游戏棋盘，加数字可以定制棋盘大小
        gamestart:快速游戏模式，每句话都当做2048游戏的命令处理
    例子：
        #2048 init (初始化游戏棋盘)
        #2048 w (向上滑动)
    """
    attrs = ent.chain.tostr().split(' ')
    player = ent.pid
    f = False
    n = 4

    if not any(attrs):
        return [Plain('请使用#h #2048查看用法')]

    asobientity = Asobi2048Data.chk(player)
    try:
        if attrs[0] == 'init':
            try:
                n=int(attrs[1])
                if n < 2 or n > 8:
                    return [Plain(text='棋盘矩阵只能要2~8阶，太小你玩不了太大我发不了= =')]
            except:
                pass
            raise NameError('2048RESET')
        grids = numpy.array(asobientity.mat)
        n = len(grids)
        
    except:
        grids = numpy.array([[0 for _ in range(n)] for __ in range(n)])
        grids[random.randint(0,n-1)][random.randint(0,n-1)] = random.randint(1,2)*2
    movedGrids=set()
    if attrs[0] in ('上','W','w','ue'):
        for i in range(n):
            for j in range(1,n):
                if grids[j][i]:
                    for k in range(j-1,-1,-1):
                        if grids[k][i]!=0:
                            if grids[j][i] == grids[k][i] and (k,i) not in movedGrids: # 合成
                                grids[k][i] *= 2
                                grids[j][i] = 0
                                f = True
                                movedGrids.add((k,i))
                            elif k+1 != j:
                                grids[k+1][i] = grids[j][i] # 移位
                                grids[j][i] = 0
                                f = True
                            break
                        if k == 0: # 特判移位
                            grids[k][i] = grids[j][i]
                            grids[j][i] = 0
                            f = True
    elif attrs[0] in ('下','S','s','shita'):
        for i in range(n):
            for j in range(n-2,-1,-1):
                if grids[j][i]:
                    for k in range(j+1,n):
                        if grids[k][i]!=0:
                            if grids[j][i] == grids[k][i] and (k,i) not in movedGrids:
                                grids[k][i] *= 2
                                grids[j][i] = 0
                                f = True
                                movedGrids.add((k,i))
                            elif k-1 != j:
                                grids[k-1][i] = grids[j][i]
                                grids[j][i] = 0
                                f = True
                            break
                        if k == n-1:
                            grids[k][i] = grids[j][i]
                            grids[j][i] = 0
                            f = True
    elif attrs[0] in ('左','A','a','hidari'):
        for i in range(n):
            for j in range(1,n,1):
                if grids[i][j]:
                    for k in range(j-1,-1,-1):
                        if grids[i][k]!=0:
                            if grids[i][j] == grids[i][k] and (i,k) not in movedGrids:
                                grids[i][k] *= 2
                                grids[i][j] = 0
                                f = True
                                movedGrids.add((i,k))
                            elif k+1 != j:
                                grids[i][k+1] = grids[i][j]
                                grids[i][j] = 0
                                f = True
                            break
                        if k == 0:
                            grids[i][k] = grids[i][j]
                            grids[i][j] = 0
                            f = True
    elif attrs[0] in ('右','D','d','migi'):
        for i in range(n):
            for j in range(n-2,-1,-1):
                if grids[i][j]:
                    for k in range(j+1,n,1):
                        if grids[i][k]!=0:
                            if grids[i][j] == grids[i][k] and (i,k) not in movedGrids:
                                grids[i][k] *= 2
                                grids[i][j] = 0
                                f = True
                                movedGrids.add((i,k))
                            elif k-1 != j:
                                grids[i][k-1] = grids[i][j]
                                grids[i][j] = 0
                                f = True
                            break
                        if k == n-1:
                            grids[i][k] = grids[i][j]
                            grids[i][j] = 0
                            f = True
    elif attrs[0] in GLOBAL.unsubscribes:
        Sniffer.clear(player,'#2048')
        return [Plain(text=random.choice(['快速游戏模式关闭']))]
    elif attrs[0] in ('快速模式','gamestart'):
        sni: Sniffer = Sniffer.overwrite(player,'#2048')
        sni.add(
            '#2048',
            [TriggerRule('.*')]
        )
        return [Plain(text=random.choice(['快速游戏模式开启，关闭请使用bye']))]
    if f:
        zeromap = []
        for i in range(n):
            for j in range(n):
                if grids[i][j] == 0:
                    zeromap.append((i,j))
        x,y = random.choice(zeromap)
        grids[x][y] = random.randint(1,2)*2
    outputString = []
    asobientity.mat = grids.tolist()
    asobientity.save()
    for i in grids:
        for j in i:
            outputString.append(Plain(text='%6d'%j))
        outputString.append(Plain(text='\n'))
    return outputString



class SlidingPuzzle(Document, RefPlayerBase):
    bg = ImageField()
    mat = ListField(ListField(IntField()))

def asobiSlidingPuzzle(ent: CoreEntity):
    """#华容道 [#滑动拼图, #hrd]
    源自八数码问题，
    简单的滑动拼图还要解释吗（
    可用参数：
        w:向上滑动
        a:向左滑动
        s:向下滑动
        d:向右滑动
        init [(可选)2~6]:初始化游戏棋盘，加数字可以定制棋盘大小
        bg <图片>:换背景
        t:用文本方式打印拼图
    """
    player = ent.pid
    attrs = ent.chain.tostr().split(' ')

    def find1(array):
        for p,i in enumerate(array):
            for q,j in enumerate(i):
                if j == 1:
                    return p,q

    def splitImage(fn:str,n:int,array)->PImage.Image:
        """
        根据传入的array将图片重组
        array得是n*n的numpy.array对象
        返回保存的文件的临时文件路径
        array是1~n^2，注意不是从0开始
        """
        bg = PImage.open(fn).convert('RGBA')
        edge = min(bg.width,bg.height)
        cell = edge // n
        bg = bg.crop((0,0,edge,edge))
        newbg = []
        for i in range(n):
            # tmp = []
            for j in range(n):
                newbg.append(bg.crop((i * cell, j * cell, (i + 1) * cell, (j + 1) * cell)))
            # newbg.append(tmp)

        dst = PImage.new('RGBA',(n*cell,n*cell))

        for i in range(n):
            # tmp = []
            for j in range(n):
                if array[i][j]!=1:
                    dst.paste(newbg[int(array[i][j]-1)],(i * cell, j * cell, (i + 1) * cell, (j + 1) * cell))
        # bio = BytesIO()
        # dst.save(bio, format='PNG')
        # sfn = 'tmp' + randstr(4) + '.png'
        # dst.save(sfn)
        # asyncio.ensure_future(rmTmpFile(sfn))
        return dst

    sp = SlidingPuzzle.chk(player)
    if not sp.bg:
        sp.bg = "Assets/default.png"
    
    if not sp.mat or attrs and attrs[0] == 'init':
        try:
            n=int(attrs[1])
            if n not in range(2,7):
                return [Plain(text='为了宁的游戏体验，棋盘只能要2~6阶内的方阵')]
        except:
            n = 3
        arr = [i for i in range(1,1+n*n)]
        random.shuffle(arr)
        tmp = copy.deepcopy(arr)
        tmp.remove(1)
        invs = calcinvs(tmp)
        k = arr.index(1) // n
        if n&1:
            while invs&1:
                random.shuffle(arr)
                tmp = copy.deepcopy(arr)
                tmp.remove(1)
                invs = calcinvs(tmp)
        else:
            while (invs^(k&1)) & 1:
                random.shuffle(arr)
                tmp = copy.deepcopy(arr)
                tmp.remove(1)
                invs = calcinvs(tmp)
                k = arr.index(1) // n
        print(arr)
        grids = numpy.array(arr)
        grids.resize(n,n)
        sp.mat = grids.tolist()
        sp.save()
        return [
            Plain(f'移动拼图初始化完成\n{grids}'),
            Image(base64=pimg_base64(splitImage(sp.bg,n,grids)))
        ]
        
        
    grids = numpy.array(sp.mat)
    n = len(grids)
    if attrs:
        if attrs[0] in ('下','S','s','shita'):
            x,y = find1(grids)
            if y>0:
                grids[x][y],grids[x][y-1] = grids[x][y-1],grids[x][y]
        elif attrs[0] in ('上','W','w','ue'):
            x,y = find1(grids)
            if y<3:
                grids[x][y],grids[x][y+1] = grids[x][y+1],grids[x][y]

        elif attrs[0] in ('右','D','d','migi'):
            x,y = find1(grids)
            if x>0:
                grids[x][y],grids[x-1][y] = grids[x-1][y],grids[x][y]
        elif attrs[0] in ('左','A','a','hidari'):
            x,y = find1(grids)
            if x<3:
                grids[x][y],grids[x+1][y] = grids[x+1][y],grids[x][y]
        elif attrs[0] in ('txt','t','T','文字'):
            return [Plain(f'{grids}')]
        elif attrs[0] in ('bg','changebackground','换图','换老婆'):
            # if 'pic' in ent.meta and ent.meta['pic']:
            for i in ent.chain:
                if isinstance(i, Image):
                    src = requests.get(i.url).content
                    sp.bg = BytesIO(src)
                    sp.save()
                    return [Plain('图片背景更新成功')]
            return '您没发图捏'
        elif attrs[0] in ('快速模式','gamestart'):
            sni: Sniffer = Sniffer.overwrite(player,'#华容道')
            sni.add(
                '#华容道',
                [TriggerRule('.*')]
            )
            return [Plain(text=random.choice(['老婆快速重组模式，退出请用bye']))]
        elif attrs[0] in GLOBAL.unsubscribes:
            Sniffer.clear(player,'#华容道')
            return [Plain(text=random.choice(['还是慢慢拼老婆吧']))]

    sp.mat = grids.tolist()
    sp.save()
    return [Image(base64=pimg_base64(splitImage(sp.bg,n,grids)))]

