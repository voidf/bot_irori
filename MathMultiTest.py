"""数学类"""
import os
import GLOBAL
import quine_mccluskey.qmccluskey
import numpy
import math
import copy
import ctypes
import functools
import traceback
import statistics

from GLOBAL import logging

from Utils import *
# importMirai()

'''
否.......... !
合取........ &
可兼或...... |
异或.... ^
由...可得... >
当且仅当.... =
'''

from pydantic import BaseModel

class FindTruth:

    def __init__(self,inputMono):
        #存储字母及其真值
        self.Dic = {}
        self.Lis = []
        self.li = []
        self.outPut = []
        #输入表达式
        self.__In(inputMono)
        #输出真值表
        self.__Out()
        self._print()

    #输入
    def __In(self,inputMono):
        #得到表达式Str
        self.Str = inputMono
        #筛出字母集合
        self.Set = set(self.Str).difference(set("()!&|>=^"))
        
    #求公式结果
    def __Sum(self, Str):
        i = 0 #字符位置
        s = -1#式子真值
        while i < len(Str):
            c = Str[i]
        #单操作符'！'要做特殊的分类处理
            if c == "!":
            #右边是字母
                if Str[i+1] in self.Set:
                    c = Str[i+1]
                    i = i + 1
                    s0 = self.__Add('!',self.Dic[c])   
            #右边是左括号
                else:
                    end = self.__Pei(i+1, Str)
                    s0 = self.__Add('!', self.__Sum(Str[i+1:end+1]))
                    i = end
        #字母
            elif c in self.Set:
                s0 = self.Dic[c]
        #其它运算符
            elif c in set("&|>=^"):
                operat = c
        #左括号
            elif c == '(':
                end = self.__Pei(i, Str)
                s0 = self.__Sum(Str[i+1:end])
                i = end
        #运算结果
            if s == -1:
                s = s0
                s0 = -1
            elif operat != 0 and s0 != -1:
                s1 = s
                s = self.__Add(operat, s, s0)
                operat = 0
                s0 = -1
            i = i + 1
        return s
    #配对左右括号
    def __Pei(self, cur, Str):
        kflag = 1  # 左括号的数目
        while not kflag == 0:
            cur = cur + 1
            if Str[cur] == '(':
                kflag = kflag + 1
            elif Str[cur] == ')':
                kflag = kflag - 1
        return cur    
    #运算操作
    def __Add(self, operator, a, b = -1):#b默认为-1时，表示是单操作符号' ! '
        if operator == '!':
            boo = not a
        elif operator == '&':
            boo = a and b
        elif operator == '|':
            boo = a or b
        elif operator == '^':
            boo = ((not a) or (not b)) and (a or b)
        elif operator == '>':
            boo = (not a) or b
        elif operator == '=':
            boo = ((not a) and (not b)) or (a and b)
        else:
            self.outPut.append("there is no such operator")
        if boo:
            return 1
        else:
            return 0
    #输出
    def __Out(self):
        #将字母放入dict和List
        S = ''
        for c in sorted(self.Set):
            self.Dic[c] = 0
            self.Lis.append(c)
            S = S + c + ' '
        self.outPut.append(f"{S} {self.Str}")
        self.__Count(0)
    #构造2^n的序列
    def __Count(self, i):
        #是结尾，打印 + 运算
        
        if i == len(self.Lis):
            #self.Lis.sort()
            S = ''
            Minmal = 0
            #self.li = []
            for idx,l in enumerate(self.Lis):
                S = S + str(self.Dic[l]) + ' '
                Minmal += self.Dic[l] * 2**(len(self.Lis) - idx - 1)

            res = self.__Sum(self.Str)
            if res:
                self.li.append(str(Minmal))
            self.outPut.append(f"{S} {res} {Minmal}")
            return
        #不是结尾，递归赋值
        self.Dic[self.Lis[i]] = 0
        self.__Count(i+1)
        self.Dic[self.Lis[i]] = 1
        self.__Count(i+1)

    def _print(self):
        self.outPut.append(','.join(self.li))

class Plain(BaseModel):
    type: str = "Plain"
    text: str
    def __init__(self, text: str, *_, **__) -> NoReturn:
        """实例化一个 Plain 消息元素, 用于承载消息中的文字.

        Args:
            text (str): 元素所包含的文字
        """
        super().__init__(text=text)

def read_matrix_matlab(s):
    row = s.split(';')
    if not row[-1]:
        row.pop()
    li = [i.split(',') for i in row]
    for i,ii in enumerate(li):
        for j,jj in enumerate(ii):
            if '/' in li[i][j]:
                u,d = jj.split('/')
                li[i][j] = float(u) / float(j)
            else:
                li[i][j] = float(li[i][j])
    return numpy.matrix(li)

def CalC(*attrs, kwargs={}):
    try:
        if len(attrs)==3:
            a,b=(int(i) for i in attrs[1:3])
            if a<b:
                a,b=b,a
            c = 1
            for i in range(a-b,a):
                c*=i+1
            return [Plain(text=str(c))]
        elif len(attrs)==2:
            a,b=(int(i) for i in attrs[:2])
            if a<b:
                a,b=b,a
            return [Plain(text=str(comb(a,b)))]
        elif len(attrs)==1:
            b=int(attrs[0])
            return [Plain(text=str(math.factorial(b)))]
        else:
            return []
    except Exception as e:
        return [Plain(str(e))]

def CalA(*attrs,kwargs={}):
    return CalC('A',*attrs,kwargs=kwargs)

def CalKatalan(*attrs,kwargs={}):
    try:
        if len(attrs):
            a = int(attrs[0])
            return [Plain(str(comb(2*a,a)//(a+1)))]
        else:
            return []
    except Exception as e:
        return [Plain(str(e))]

def 统计姬from104(*attrs, kwargs={}):
    l=[float(x) for x in attrs]
    s = 0
    for i in l:
        s+=i**2
    s/=len(l)
    ostr = []
    ostr.append(Plain(f"Mean 平均数:{statistics.mean(l)}\n"))
    ostr.append(Plain(f"Mean Square 平方均值:{s}\n"))
    if len(l) & 1 == 0:
        d = 0

        # print(l)
        # print(len(l)>>1)
        for p, i in enumerate(l[len(l)>>1:]):
            d+=i-l[p]
        d/=(len(l)>>1)**2
        ostr.append(Plain(f"Mean of Successional Difference 逐差均值:{s}\n"))

    
    ostr.append(Plain(f"Median 中位数:{statistics.median(l)}\n"))
    ostr.append(Plain(f"Low Median 低中位数:{statistics.median_low(l)}\n"))
    ostr.append(Plain(f"High Median 高中位数:{statistics.median_high(l)}\n"))
    ostr.append(Plain(f"Sample Variance 样本方差:{statistics.variance(l)}\n"))
    ostr.append(Plain(f"Sample Standard Deviation 样本标准差:{statistics.stdev(l)}\n"))
    ostr.append(Plain(f"Variance 总体方差:{statistics.pvariance(l)}\n"))
    ostr.append(Plain(f"Standard Deviation 总体标准差:{statistics.pstdev(l)}\n"))
    return ostr

def QM化简器(*attrs, kwargs={}):
    """用QM法化简逻辑式，将给定的布尔表达式化简成最简与或式（NPC问题，规模过大会爆炸）
用法：
    #QM <原式的逗号隔开的最小项表示> [--dc=无关项的最小项表示] [--var=化简后显示字母]
    #QM <原式的逻辑式表示> [--dc=无关项的最小项表示] [--var=化简后显示字母]
例:
    #QM 1,4,2,8,5,7 --var=a,b,c,d
    #QM b'd+a'bc'+a'bcd' --dc=1,2 --var=a,b,c,d"""
    v = attrs
    if v[0].count(',') >= 1: # 最小项输入

        return [Plain(quine_mccluskey.qmccluskey.maid(
            minterms=v[0].split(','), 
            argsdont_cares=kwargs.get('-dc', ''),
            argsvariables=kwargs.get('-var', '')
        ))]

    else:
        return [Plain(quine_mccluskey.qmccluskey.maid(
            argssop=v[0], 
            argsdont_cares=kwargs.get('-dc', ''),
            argsvariables=kwargs.get('-var', '')
        ))]

def 打印真值表(*attrs, kwargs={}):
    s = FindTruth(' '.join(attrs))
    return [Plain('\n'.join(s.outPut))]

def 逆元(*attrs, kwargs={}): return [Plain(str(getinv(int(attrs[0]),int(attrs[1]))))]

def 欧拉函数(*attrs, kwargs={}):
    """求给定值的欧拉函数
    :param x: 待求值x
    :return:
        int: φ(x)
    """
    x = int(attrs[0])
    res = x
    upp = x**0.5
    for i in range(2, int(upp)+1):
        if x % i == 0:
            res = (res // i) * (i - 1)
            while x % i == 0:
                x //= i
    if x > 1:
        res = (res // x) * (x - 1)
    if x == int(attrs[0]):
        return [Plain(f'{x}是质数\n{res}')]
    return [Plain(f'{res}')]

def 孙子定理(*attrs, kwargs={}):
    il = ' '.join(attrs).strip().split()
    li = []
    for i in il:
        if i.isdigit():
            li.append(int(i))
    if len(li)&1:
        return [Plain('输入不合法')]
    else:
        r = li.pop()
        f = li.pop()
        while li:
            C1 = li.pop()
            M1 = li.pop()
            M2 = f
            C2 = r
            G = math.gcd(M2, M1)
            L = M1*M2//G
            if (C1-C2)%G:
                return [Plain('输入数据无解')]
            f = L
            r = ((getinv(M2//G, M1//G) * (C1 - C2) // G) % (M1 // G) * M2 + C2) % f
        return [Plain(str(r))]

# def 计算器(*attrs, kwargs={}):
#     """计算中缀表达式
#     :param exp: 待求表达式（python风格）exp
#     :return:
#         Union[int, float, complex]: result"""
#     player = getPlayer(**kwargs)
#     if attrs[0] in GLOBAL.subscribes:
#         overwriteSniffer(player, '#计算器', r'^[abcdefABCDEFoxj.0-9\s+-/*&^<>~=|%\(\)]+$')
#         return [Plain('遇到可运算表达式直接输出结果')]
#     elif attrs[0] in GLOBAL.unsubscribes:
#         removeSniffer(player, '#计算器')
#         return [Plain('禁用快速计算')]
#     exp, res = evaluate_expression(''.join(attrs).replace(' ','').strip())
#     return [Plain(f"{exp} = {res}")]

def 逆波兰(*attrs, kwargs={}):
    """计算逆波兰表达式
    :param exp: 待求表达式（默认空格分隔）exp
    :return:
        Union[int, float, complex]: result"""
    player = getPlayer(**kwargs)
    op1 = []
    op2 = []
    for i in attrs:
        if i in binocular_calculate_map:
            A = op2.pop()
            B = op2.pop()
            op2.append(f'({B}{i}{A})')
        else:
            op2.append(i)
    try:
        for i in attrs:
            if i in binocular_calculate_map:
                A = op1.pop()
                B = op1.pop()
                op1.append(binocular_calculate_map[i](B,A))
            else:
                if 'j' in i:
                    op1.append(complex(i))
                elif '.' in i or 'e' in i:
                    op1.append(float(i))
                elif 'x' in i:
                    op1.append(int(i, 16))
                elif 'o' in i:
                    op1.append(int(i, 8))
                elif 'b' in i:
                    op1.append(int(i, 2))
                else:
                    op1.append(int(i))
    except:
        op1 = ['evaluate failed.']
    print(op1, op2)
    return [Plain(f'{op1[0]}\n{op2[0]}')]

逆波兰.SHORTS = ['#nbl']

def 老线代bot了(*attrs, kwargs={}):
    print(attrs)
    if attrs[0] in ('乘','*','mul'):
        A = read_matrix_matlab(attrs[1])
        B = read_matrix_matlab(attrs[2])
        return [Plain(f'{A*B}')]
    elif attrs[0] in ('加','+','add'):
        A = read_matrix_matlab(attrs[1])
        B = read_matrix_matlab(attrs[2])
        return [Plain(f'{A+B}')]
    elif attrs[0] in ('减','-','sub'):
        A = read_matrix_matlab(attrs[1])
        B = read_matrix_matlab(attrs[2])
        return [Plain(f'{A-B}')]
    elif attrs[0] in ('解方程','solve'):
        A = read_matrix_matlab(attrs[1])
        B = read_matrix_matlab(attrs[2])
        if len(B) == 1:
            B = B.T
        return [Plain(f'{numpy.linalg.solve(A,B)}')]
    elif attrs[0] in ('叉','cross','叉乘','叉积'):
        A = read_matrix_matlab(attrs[1])
        B = read_matrix_matlab(attrs[2])
        A = numpy.array(A)[0]
        B = numpy.array(B)[0]
        return [Plain(f'{numpy.cross(A,B)}')]
    elif attrs[0] in ('点','dot','点乘','点积'):
        A = read_matrix_matlab(attrs[1])
        B = read_matrix_matlab(attrs[2])
        A = numpy.array(A)[0]
        B = numpy.array(B)[0]
        return [Plain(f'{numpy.dot(A,B)}')]
    elif attrs[0] in ('逆','求逆','inv','I'):
        A = read_matrix_matlab(attrs[1])
        return [Plain(f'{A.I}')]
    elif attrs[0] in ('转','转置','transpose','T'):
        A = read_matrix_matlab(attrs[1])
        return [Plain(f'{A.T}')]
    elif attrs[0] in ('行列式','det'):
        A = read_matrix_matlab(attrs[1])
        return [Plain(f'{numpy.linalg.det(A)}')]
    elif attrs[0] in ('特征值','eig'):
        A = read_matrix_matlab(attrs[1])
        return [Plain(f'{numpy.linalg.eig(A)}')]
    elif attrs[0] in ('秩','rank'):
        A = read_matrix_matlab(attrs[1])
        return [Plain(f'{numpy.linalg.matrix_rank(A)}')]
    else:
        return [Plain('没有命中的决策树，看看#h #线代？')]

def 离散闭包用工具(*attrs, kwargs={}):
    m = {} # 数转名
    r = {} # 名转数
    def addval(v):
        if v not in r:
            r[v] = len(m)
            m[len(m)] = v
        return r[v]
    def rendermatrix(mt: numpy.array) -> str:
        ans = []
        for i, ii in enumerate(mt):
            for j, jj in enumerate(ii):
                if jj:
                    ans.append(f'{m[i]},{m[j]}')
        return f'{mt.astype(numpy.int16)}\n{" ".join(ans)}'

    conn = []
    input_char = []
    for i in attrs:
        f, t = i.split(',')
        input_char.append(f)
        input_char.append(t)
    for i in sorted(input_char): addval(i) # 搞成字典序可能好一些
    for i in attrs:
        f, t = i.split(',')
        conn.append((r[f], r[t]))

    mat = numpy.zeros((len(m), len(m)), dtype=bool)
    for f, t in conn:
        mat[f][t] = 1
    rmat = copy.deepcopy(mat) # 自反
    smat = copy.deepcopy(mat) # 对称
    tmat = copy.deepcopy(mat) # 传递

    自反 = True
    反自反 = True
    对称 = True
    反对称 = True
    传递 = True

    for i, ii in enumerate(mat):
        for j, jj in enumerate(ii):
            if i == j:
                if jj: 反自反 = False
                else: 自反 = False
                rmat[i][j] = 1
            else:
                if jj:
                    if mat[j][i]: 反对称 = False
                    else: 对称 = False
                    smat[j][i] = 1
    tmp = copy.deepcopy(mat)
    powerlist = []
    s = set()
    while tmp.tostring() not in s:
        s.add(tmp.tostring())
        powerlist.append(tmp)
        tmp = tmp.dot(mat)
    for i in powerlist:
        tmat |= i
    if not (tmat == mat).all(): 传递 = False
    renderer = f"""基本性质：
    自反:{自反}
    反自反:{反自反}
    对称:{对称}
    反对称:{反对称}
    传递:{传递}

{m}

{rendermatrix(mat)}

r(R)即自反闭包：
{rendermatrix(rmat)}

s(R)即对称闭包：
{rendermatrix(smat)}

t(R)即传递闭包：
{rendermatrix(tmat)}
"""
    return [Plain(renderer)]

def 球盒(*attrs, kwargs={}):
    """求解把n个球放进m个盒子里面有多少种方案的问题。
必须指定盒子和球以及允不允许为空三个属性。
用法：
    #球盒 <盒子相同？(0/1)><球相同？(0/1)><允许空盒子？(0/1)> n m
用例：
    #球盒 110 20 5
    上述命令求的是盒子相同，球相同，不允许空盒子的情况下将20个球放入5个盒子的方案数。"""
    # 参考https://www.cnblogs.com/sdfzsyq/p/9838857.html的算法
    if len(attrs)!=3:
        return '不是这么用的！请输入#h #球盒'
    n, m = map(int, attrs[1:3])
    if attrs[0] == '110':
        f = A072233_list(n, m)
        return f[n][m]
    elif attrs[0] == '111':
        f = A072233_list(n, m)
        return sum(f[-1])
    elif attrs[0] == '100':
        return A048993_list(n, m)[-1]
    elif attrs[0] == '101':
        return sum(A048993_list(n, m))
    elif attrs[0] == '010':
        return comb(n-1, m-1)
    elif attrs[0] == '011':
        return comb(n+m-1, m-1)
    elif attrs[0] == '000': # 求两个集合的满射函数的个数可以用
        return A048993_list(n, m)[-1] * math.factorial(m)
    elif attrs[0] == '001':
        return m**n
    else:
        return f"解析不了的属性：{attrs[0]}，我们只吃长度为3的01串喵"

def 十转(*attrs, kwargs={}):
    """十进制转换为其他进制工具：
输入格式：
    #十转 <目标进制> <源十进制数>
例：
    #十转 5 261"""
    l = []
    b = int(attrs[0])
    x = int(attrs[1])
    if x==0:
        return 0
    while x:
        l.append(str(x%b))
        x//=b
    l.reverse()
    return f"{l}\n{''.join(l)}"

def 划分数个数(*attrs, kwargs={}): return [Plain(A000110_list(int(attrs[0]), kwargs.get('-m', 0)))]
    
def 素数前缀和(*attrs, kwargs={}):
    """min_25筛"""
    tot = 0


    n = int(attrs[0])
    sqr = int(n**0.5)

    primes, primepref = orafli(sqr+2)

    w = [0] * (sqr + 3) * 2
    g = [0] * (sqr + 3) * 2
    
    ind1 = [0] * (sqr + 3)
    ind2 = [0] * (sqr + 3)

    def valposition(x: int, n: int) -> int:
        return ind1[x] if x <= sqr else ind2[n//x]
    def setval(x: int, n: int, tot: int):
        if x<=sqr:
            ind1[x] = tot
        else:
            ind2[n//x] = tot

    l = 1
    while l <= n:
        r = n // (n // l)
        tot += 1
        w[tot] = n // l

        setval(n//l, n, tot)
        g[tot] = n // l - 1

        l = r + 1

    for p, i in enumerate(primes):
        j = 1
        while j <= tot and i * i <= w[j]:
            g[j] -= g[valposition(w[j]//i, n)] - p
            j += 1
    return [Plain(text=str(g[1]))]


    

def 空函数(*attrs, kwargs={}):
    return None




functionMap = {
    # '#QM':QM化简器,
    '#C':CalC,
    '#A':CalA,
    '#K':CalKatalan,
    '#统计':统计姬from104,
    '#inv':逆元,
    '#phi':欧拉函数,
    '#CRT':孙子定理,
    '#线代':老线代bot了,
    '#真值表':打印真值表,
    '#encap':离散闭包用工具,
    '#B': 划分数个数,
    '#min25': 素数前缀和
}
shortMap = {'#stat':'#统计'}
functionDescript = {
    '#K':'计算Katalan数，例:#K 4,公式：C(2n,n)-C(2n,n-1)',
    '#A':'计算排列数，例:#A 3 3',
    '#encap':'根据所给二元组表分析关系。例子：#encap a,b a,c a,d',
    '#统计':'焊接自104空间的统计代码，接受空格分隔的浮点参数，返回样本中位数，平均数，方差等信息，例:#统计 11.4 51.4 19.19 8.10',
    '#B': '计算给定集合的划分的方案数，可以用-m选项提供求模数。用例#B 233 -m=10086',
    '#phi': '算欧拉函数',
    '#C':
'''
两个参数计算组合数，一个参数计算阶乘
例:
    #C 9 7
    计算组合数C(9,7)
    #C 20
    计算阶乘20!
''',
    '#线代':
"""线代工具箱，底层是numpy，能算一些矩阵相关
用法：
    #线代 <操作命令> <矩阵1> <矩阵2>
    #线代 <操作命令> <矩阵1>
    #线代 <操作命令> <向量1> <向量2>
    #线代 <操作命令> <向量1>
二目（需要两个参数）操作命令包括：
    乘，加，减，解方程，叉乘，点乘
单目操作命令包括：
    求逆，转置，行列式，特征值，秩
输入矩阵格式仿照matlab：
如1,1,4;5,1,4代表矩阵
    [1 1 4]
    [5 1 4]
例:
    #线代 乘 1,1,4;5,1,4;9,3,1 1,9,1;9,1,9;8,1,0
""",
    '#真值表':
"""
用给定的逻辑式生成真值表，注意除了非运算外其他运算同级
即从左到右计算，如需要请加括号
    非 !
    与 &
    或 |
    异或 ^
    由...可得... >
    当且仅当.... =
例:
    #真值表 !A|(B^C)
""",
    '#inv':'求给定的x在模m意义下的逆元（exgcd\n用法：#inv <x> <m>',
    '#CRT':
"""
用中国剩余定理解剩余方程
输入格式：
    模数1 余数1 模数2 余数2 ...
当然如果你愿意可以以回车或者空格-回车交替这样分隔输入
又如：
    模数1 余数1
    模数2 余数2
    ...
如果有解，返回值是满足所有剩余方程的最小结果
"""
}

ProcessCNT = 9
import multiprocessing
from multiprocessing import Pool, Manager, Process, Semaphore
from multiprocessing.dummy import Pool as Pool2
import functools
import queue
from dataclasses import dataclass

@dataclass
class PendingTask():
    pid: int
    cmd: str
    args: list

@dataclass
class Operation():
    opr: str
    pid: int = 0

def task_monitor(func, *args, **kwargs):
    tle = kwargs.get('tle', None)
    p = Pool2(1)
    res = p.apply_async(func, args=args)
    pid = kwargs['pid']
    # print(kwargs)
    try:
        out = res.get(tle)
        # kwargs['worker'].release()

        tmpd = kwargs['pcb'][pid]
        tmpd['status'] = 'done'
        kwargs['pcb'].update({pid:tmpd})
        # kwargs['pcb'][pid].update(status='done')
        
        # print(kwargs)
        print(pid, '执行完毕, 结果：', out)
        kwargs['op'].put(Operation('R'))
        return out
    except:
        traceback.print_exc()
        # kwargs['worker'].release()

        tmpd = kwargs['pcb'][pid]
        tmpd['status'] = 'timeout'
        kwargs['pcb'].update({pid:tmpd})

        print(pid, '执行超时')
        kwargs['op'].put(Operation('R'))



# operation_queue是指令队列
# K(pid): kill
# J(pid): join
# R: try run
# Q: quit
def callmanager(
    operation_queue: multiprocessing.Queue, 
    tasks_queue: multiprocessing.Queue,
    pcb: dict,
    worker: Semaphore): # 实际上实现了原语
    # with Pool(ProcessCNT, maxtasksperchild=1) as pool:
    process_map = {}
    

    while 1:
        operation = operation_queue.get(block=True)
        for k, v in list(pcb.items()):
            if v['status'] not in ('pending', 'running'):
                pcb.pop(k)
                if k in process_map:
                    process_map[k].kill()
                    process_map[k].join()
                    process_map.pop(k)
                    worker.release()

        if operation.opr == 'R':
            if not worker.acquire(block=False):
                continue
            else:
                try:
                    task = tasks_queue.get(block=False)
                    pid = task.pid
                    # worker.acquire(block=False)
                    # pid = generate_pid()
                    print(pid, '开始任务')
                    pcb[pid].update(status="running")

                    tmpd = pcb[pid]
                    tmpd['status'] = 'running'
                    pcb.update({pid:tmpd})

                    wrapper = functools.partial(task_monitor, functionMap.get(task.cmd, 空函数))
                    process_map[pid] = Process(
                        target=wrapper,
                        args=task.args,
                        kwargs={
                            'tle': 100,
                            'worker': worker,
                            'op': operation_queue,
                            'pcb': pcb,
                            'pid': pid
                        }
                    )
                    process_map[pid].start()
                except queue.Empty:
                    worker.release()
        elif operation.opr == 'K':
            pid = operation.pid
            if pid not in pcb:
                print('找不到对应pid的进程……')
                continue
            else:
                if pcb[pid]['status'] == 'pending':
                    pcb.pop(pid)
                elif pcb[pid]['status'] == 'running':
                    process_map[pid].kill()

                    tmpd = pcb[pid]
                    tmpd['status'] = 'killed'
                    pcb.update({pid:tmpd})
        elif operation.opr == 'J':
            pid = operation.pid
            if pid not in pcb:
                print('找不到对应pid的进程……')
                continue
            else:
                if pcb[pid]['status'] == 'pending':
                    # pcb.pop(pid)
                    print('join失败：进程还未被创建')
                else:
                    process_map[pid].join()
        elif operation.opr == 'Q':
            for k, v in list(pcb.items()):
                if v['status'] in ('running',):
                    print('丢弃进程', k)
                    if k in process_map:
                        process_map[k].kill()
                        process_map[k].join()
                        process_map.pop(k)
                        worker.release()
            break



                



if __name__ == "__main__":

    with Manager() as manager:
        pcb = manager.dict()
        worker = Semaphore(ProcessCNT)
        tasks_queue = multiprocessing.Queue()
        operation_queue = multiprocessing.Queue()
        atomic_process = Process(
            target=callmanager,
            args=(
                operation_queue,
                tasks_queue,
                pcb,
                worker
            )
        )
        atomic_process.start()
        
        def generate_pid():
            pid = random.randint(1, 1<<16)
            while pid in pcb:
                pid = random.randint(1, 1<<16)
            return pid
        #min25 100000000000

        while 1:
            # try:
            raw = input('>>>').split()
            # tobepop = []

            if len(raw)<1:
                continue
            cmd, *args = raw
            if cmd in GLOBAL.unsubscribes + ('q', 'quit'):
                # loopback.kill()

                # atomic_process.kill()
                
                operation_queue.put(Operation('Q'))
                atomic_process.join()
                break
            elif cmd == 'ps':
                print(*sorted(pcb.items()), sep='\n')
                continue
            elif cmd == 'eval':
                print(eval(' '.join(args)))
                continue
            elif cmd == 'kill':
                operation_queue.put(Operation('K', int(args[0])))
                continue
            elif cmd == 'join':
                operation_queue.put(Operation('J', int(args[0])))
                continue
            else:
                pid = generate_pid()
                pcb[pid] = {
                    'status':'pending',
                    'command':' '.join(raw)
                }
                tasks_queue.put(
                    PendingTask(pid, cmd, list(args))
                )
                operation_queue.put(Operation('R'))

            # elif cmd == 'kill':
            #     pid = int(args[0])
            #     if pid not in processing:
            #         print('找不到这个进程')
            #     else:
            #         if processing[pid][0] == 'done':
            #             pp.pop(pid).join()
            #             processing.pop(pid)
            #         else:
            #             if processing[pid][0] == 'running':
            #                 worker.release()
            #             pp.pop(pid).kill()
            #             # tmpp = pp.pop(pid)
            #             # tmpp.kill()
            #             # print(tmpp)
            #             processing.pop(pid)
            #     continue

            # pd = availables.pop
            # pid = random.randint(0,1<<16)
            # while pid in processing:
            #     pid = random.randint(0,1<<16)

            # processing[pid] = {
            #     'status':'pending',
            #     'command':' '.join(raw),
            #     #pool.apply_async(callmanager, args=args, kwds={'pid': pid, 'processing': processing}, callback=回调, error_callback=回调)
            # }
            # pp[pid] = Process(target=callmanager, args=(cmd, pid, processing, worker, *args))
            # pp[pid].start()
            # pp[pid].
            
            # pool.apply_async(
            #     callmanager, 
            #     args=raw, 
            #     kwds={'pid': pid, 'processing': processing}, 
            #     callback=回调, 
            #     error_callback=错误回调
            # )
                # except KeyboardInterrupt:
                #     logging.error(traceback.format_exc())
