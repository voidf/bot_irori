from mirai import Mirai, Plain, MessageChain, Friend, Face, MessageChain,Group,Image,Member,At
from mirai.face import QQFaces
from bs4 import BeautifulSoup
from PIL import ImageFont,ImageDraw
from PIL import Image as PImage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import asyncio
import requests
import json5
import json
import numpy
import random
import os
import base64
import qrcode
import io
import string
import math
import urllib
import copy
import ctypes
import functools
import traceback
import http.client
import statistics
import csv
import hashlib
import zlib
import time
import datetime
import urllib
import mido
import GLOBAL
import shutil
from Utils import *


def asobi2048(*attrs,**kwargs):
    player = getPlayer(**kwargs)
    f = False
    n = 4
    if not os.path.exists('2048/'):
        os.mkdir('2048/')
    try:
        if attrs[0] == 'init':
            try:
                n=int(attrs[1])
                if n < 2 or n > 8:
                    return [Plain(text='棋盘矩阵只能要2~8阶，太小你玩不了太大我发不了= =')]
            except:
                pass
            raise NameError('2048RESET')
        grids = numpy.loadtxt(f'2048/{player}mat.txt')
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
    elif attrs[0].lower() in ('terminate','quit','exit','seeyou','bye','sayonara','sayounara','madane','yamero','停','关','やめろ'):
        del GLOBAL.QuickCalls[player]
        return [Plain(text=random.choice(['我错了我不会条条都回了','快速游戏模式关闭']))]
    elif attrs[0] in ('快速模式','gamestart'):
        GLOBAL.QuickCalls[player] = (asobi2048)
        return [Plain(text=random.choice(['开始切咧，让我闭嘴大声yamero','快速游戏模式开启，关闭请使用bye']))]
    if f:
        zeromap = []
        for i in range(n):
            for j in range(n):
                if grids[i][j] == 0:
                    zeromap.append((i,j))
        x,y = random.choice(zeromap)
        grids[x][y] = random.randint(1,2)*2
    outputString = []
    numpy.savetxt(f'2048/{player}mat.txt',grids,fmt='%d')
    for i in grids:
        for j in i:
            outputString.append(Plain(text='%6d'%j))
        outputString.append(Plain(text='\n'))
    return outputString

def asobiPolyline(*attrs,**kwargs):
    player = getPlayer(**kwargs)
    n=1000
    m = {
        1:(0,-1), # 左
        2:(-1,0), # 上
        3:(0,1), # 右
        4:(1,0) # 下
    }
    if not os.path.exists('Polyline/'):
        os.mkdir('Polyline/')
    try:
        if attrs[0] == 'init':
            try:
                n=int(attrs[1])
                if n < 2 or n > 2000:
                    return [Plain(text='为了宁的游戏体验，地图只能要2~2000阶内的方阵')]
            except:
                pass
            raise NameError('PolylineRESET')
        grids = numpy.loadtxt(f'''Polyline/{player}mat.txt''')
        n = len(grids)
        with open(f'''Polyline/{player}ans.txt''','r') as fr:
            s = fr.readline().strip().split(' ')
            ctr = int(fr.readline().strip())
        op = numpy.array([int(s[0]),int(s[1])])
        ed = numpy.array([int(s[2]),int(s[3])])
    except: #进行初始化操作
        grids = numpy.zeros([n,n])
        op = (random.randint(0,n-1),random.randint(0,n-1))
        polylen = random.randint(1,(n-1)*n)
        print(polylen)

        p = numpy.array(op)
        op = numpy.array(op)
        rush = 0
        for i in range(polylen):
            if rush:
                rush-=1
            else:
                movement = random.randint(1,4)
                rush = random.randint(1,int(min(n,(polylen-i))**0.5))
                
            tmp = numpy.array(m[movement]) + p
            if i % 10000 == 0:
                print(rush)
                print(i)
                print(p)
                print(grids[p[0]][p[1]])
            if tmp[0] in range(n) and tmp[1] in range(n) and grids[tmp[0]][tmp[1]] == 0:
                valid = True
                grids[p[0]][p[1]] = movement
                p = tmp
            else:
                tm = copy.deepcopy(m)
                tm.pop(movement)
                valid = False
                while len(tm):
                    movement = random.choice(list(tm))
                    tmp = numpy.array(tm[movement]) + p
                    if tmp[0] in range(n) and tmp[1] in range(n) and grids[tmp[0]][tmp[1]] == 0:
                        grids[p[0]][p[1]] = movement
                        p = tmp
                        valid = True
                        break
                    tm.pop(movement)
                    #print(tm.pop(movement))
                #print('out')
                if valid == False:
                    print('getBreakSignal')
                    polylen = i
                    ed = p
                    break
        if valid:
            ed = p
        numpy.savetxt(f'''Polyline/{player}mat.txt''',grids,fmt='%d')
        with open(f'''Polyline/{player}ans.txt''','w') as fw:
            fw.write(f'{op[0]} {op[1]} {ed[0]} {ed[1]}\n0')
        ctr = 0
        return [Plain(text=f'折线初始化完毕,长度{polylen},flag状态{valid}')]
    if attrs[0] == '!':
        try:
            x,y,X,Y = (int(_)-1 for _ in attrs[1:])
            
            if (x==op[0] and y==op[1] and X==ed[0] and Y==ed[1]) or (x==ed[0] and y==ed[1] and X==op[0] and Y==op[1]):
                return [Plain(text=f'正确，目前查询次数{ctr}')]
            else:
                return [Plain(text='错啦！')]
        except Exception as e:
            return [Plain(text=f'输入格式错误，info:{e}')]
    elif attrs[0] == '?':
        try:
            x,y,X,Y = (int(_)-1 for _ in attrs[1:])
            if x>X:
                x,X=X,x
            if y>Y:
                y,Y=Y,y
            if X>=n or Y>=n or x<0 or y<0:
                return [Plain(text='查询越界')]
            ctr+=1
            with open(f'''Polyline/{player}ans.txt''','w') as fw:
                fw.write(f'{op[0]} {op[1]} {ed[0]} {ed[1]}\n')
                fw.write(str(ctr))
            penetrateCtr = 0
            for i in range(x,X+1): #统计列
                if y:
                    if grids[i][y-1] == 3:
                        penetrateCtr += 1
                if y != n:
                    if grids[i][y] == 1:
                        penetrateCtr += 1
                if Y+1:
                    if grids[i][Y] == 3:
                        penetrateCtr += 1
                if Y+1 != n:
                    if grids[i][Y+1] == 1:
                        penetrateCtr += 1
            for i in range(y,Y+1): #统计行
                if x:
                    if grids[x-1][i] == 4:
                        penetrateCtr += 1
                if x != n:
                    if grids[x][i] == 2:
                        penetrateCtr += 1
                if X+1:
                    if grids[X][i] == 4:
                        penetrateCtr += 1
                if X+1 != n:
                    if grids[X+1][i] == 2:
                        penetrateCtr += 1
            return [Plain(text=f'穿界次数:{penetrateCtr}，查询次数:{ctr}')]
        except Exception as e:
            return [Plain(text=f'输入格式错误，info:{e}')]
    elif attrs[0] == 'render':
        col = 255
        try:
            col = int(attrs[1])
        except:
            pass
        for pi,i in enumerate(grids):
            for pj,j in enumerate(i):
                if j:
                    grids[pi][pj] = col
        renderedPng = PImage.fromarray(grids).convert('L')
        fn = f'''Polyline/{player}.png'''
        with open(fn,'wb') as fw:
            renderedPng.save(fw)
        asyncio.ensure_future(rmTmpFile(fn))
        return [Image.fromFileSystem(fn)]
    else:
        return [Plain(text='命令错误')]

def asobiSlidingPuzzle(*attrs,**kwargs):
    player = getPlayer(**kwargs)

    def find1(array):
        for p,i in enumerate(array):
            for q,j in enumerate(i):
                if j == 1:
                    return p,q

    def splitImage(fn:str,n:int,array)->str:
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

        sfn = 'tmp' + randstr(4) + '.png'
        dst.save(sfn)
        asyncio.ensure_future(rmTmpFile(sfn))
        return sfn


    if not os.path.exists('SlidingPuzzle/'):
        os.mkdir('SlidingPuzzle/')

    if not os.path.exists(f'''SlidingPuzzle/{player}BG'''):
        shutil.copy('default.png',f'''SlidingPuzzle/{player}BG''')

    
    if not os.path.exists(f'''SlidingPuzzle/{player}.txt''') or attrs and attrs[0] == 'init':
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
        numpy.savetxt(f'''SlidingPuzzle/{player}.txt''',grids,fmt='%d')
        return [
            Plain(f'移动拼图初始化完成\n{grids}'),
            Image.fromFileSystem(splitImage(f'''SlidingPuzzle/{player}BG''',n,grids))
        ]
        
        
    grids = numpy.loadtxt(f'''SlidingPuzzle/{player}.txt''')
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
            if 'pic' in kwargs and kwargs['pic']:
                src = requests.get(kwargs['pic'].url).content
                with open(f'''SlidingPuzzle/{player}BG''','wb') as f:
                    f.write(src)
                return [Plain('图片背景更新成功')]
        elif attrs[0] in ('快速模式','gamestart'):
            GLOBAL.QuickCalls[player] = (asobiSlidingPuzzle)
            return [Plain(text=random.choice(['老婆快速重组模式，退出请用bye']))]
        elif attrs[0].lower() in ('terminate','quit','exit','seeyou','bye','sayonara','sayounara','madane','yamero','停','关','やめろ'):
            del GLOBAL.QuickCalls[player]
            return [Plain(text=random.choice(['还是慢慢拼老婆吧']))]

    numpy.savetxt(f'''SlidingPuzzle/{player}.txt''',grids,fmt='%d')
    return [Image.fromFileSystem(splitImage(f'''SlidingPuzzle/{player}BG''',n,grids))]


GameMap = {
    '#2048':asobi2048,
    '#折线':asobiPolyline,
    '#华容道':asobiSlidingPuzzle
}
GameShort = {'#zx':'#折线','#hdpt':'#华容道'}

GameDescript = {
    '#2048':
"""
开始2048游戏，wasd控制移动方向，init用于初始化，传参gamestart进入快速操作模式（慎用
可用参数：
    w:向上滑动
    a:向左滑动
    s:向下滑动
    d:向右滑动
    init [(可选)2~8]:初始化游戏棋盘，加数字可以定制棋盘大小
    gamestart:快速游戏模式，每句话都当做2048游戏的命令处理
""",
    '#折线':
"""
来自教授的题目模拟，服务器随机生成一个折线，你可以查询格子x,y到X,Y之间的矩形区域被折线穿过多少次
游戏目标是猜出这条折线的起点和终点
格式：
    #折线 ? <x> <y> <X> <Y> （询问格子x,y到X,Y的穿界次数）
    #折线 ! <x> <y> <X> <Y> （回答起点和终点），
    #折线 render （可视化折线）
""",
    '#华容道':
"""
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
}