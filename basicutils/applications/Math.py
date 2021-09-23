"""数学类(重构完毕)"""
from basicutils.database import *
import os
# if __name__ == '__main__':
    # os.chdir('..')
import basicutils.CONST as GLOBAL
from basicutils.quine_mccluskey import qmccluskey
import asyncio
import numpy
import math
import copy
import functools
import traceback
import http.client
import statistics
import time
import datetime
# from Utils import *
# from Sniffer import *
from basicutils.algorithms import *
from basicutils.chain import *
from basicutils.network import *

'''
否.......... !
合取........ &
可兼或...... |
异或.... ^
由...可得... >
当且仅当.... =
'''
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

def CalC(ent: CoreEntity):
    """#组合数 [#C]
    两个参数计算组合数，一个参数计算阶乘
    例:
        #C 9 7
        计算组合数C(9,7)
        #C 20
        计算阶乘20!
    """
    attrs = ent.chain.tostr().split(' ')
    if len(attrs)==3:
        a,b=(int(i) for i in attrs[1:3])
        if a<b:
            a,b=b,a
        c = 1
        for i in range(a-b,a):
            c*=i+1
        return str(c)
    elif len(attrs)==2:
        a,b=(int(i) for i in attrs[:2])
        if a<b:
            a,b=b,a
        return [Plain(text=str(comb(a,b)))]
    elif len(attrs)==1:
        b=int(attrs[0])
        return [Plain(text=str(math.factorial(b)))]

def CalA(ent: CoreEntity):
    """#排列数 [#A]
    计算排列数，例:#A 3 3
    """
    ent.chain = MessageChain.auto_merge("A ", ent.chain)
    return CalC(ent)

def CalKatalan(ent: CoreEntity):
    """#K []
    计算Katalan数，例:#K 4,公式：C(2n,n)-C(2n,n-1)"""
    attrs = ent.chain.tostr().split(' ')
    try:
        if len(attrs):
            a = int(attrs[0])
            return [Plain(str(comb(2*a,a)//(a+1)))]
        else:
            return []
    except Exception as e:
        return [Plain(str(e))]

def 统计姬from104(ent: CoreEntity):
    """#统计 [#stat]
    焊接自104空间的统计代码，接受空格分隔的浮点参数，返回样本中位数，平均数，方差等信息，例:#统计 11.4 51.4 19.19 8.10
    """
    attrs = ent.chain.tostr().split(' ')
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

def QM化简器(ent: CoreEntity):
    """#QM []
    用QM法化简逻辑式，将给定的布尔表达式化简成最简与或式（NP完全问题，规模过大会爆炸）
    用法：
        #QM <原式的逗号隔开的最小项表示> [--dc=无关项的最小项表示] [--var=化简后显示字母]
        #QM <原式的逻辑式表示> [--dc=无关项的最小项表示] [--var=化简后显示字母]
    例:
        #QM 1,4,2,8,5,7 --var=a,b,c,d
        #QM b'd+a'bc'+a'bcd' --dc=1,2 --var=a,b,c,d"""
    v = ent.chain.tostr().split(' ')
    if v[0].count(',') >= 1: # 最小项输入

        return [Plain(quine_mccluskey.qmccluskey.maid(
            minterms=v[0].split(','), 
            argsdont_cares=meta.get('-dc', ''),
            argsvariables=meta.get('-var', '')
        ))]

    else:
        return [Plain(quine_mccluskey.qmccluskey.maid(
            argssop=v[0], 
            argsdont_cares=meta.get('-dc', ''),
            argsvariables=meta.get('-var', '')
        ))]

def 打印真值表(ent: CoreEntity):
    """#真值表 []
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
    """
    s = FindTruth(ent.chain.tostr())
    return [Plain('\n'.join(s.outPut))]

def 逆元(ent: CoreEntity):
    """#inv []
    求给定的x在模m意义下的逆元（exgcd\n用法：#inv <x> <m>
    """
    attrs = ent.chain.tostr().split(' ')
    return [Plain(str(getinv(int(attrs[0]),int(attrs[1]))))]

def 欧拉函数(ent: CoreEntity):
    """#phi []
    求给定值的欧拉函数
    :param x: 待求值x
    :return:
        int: φ(x)
    """
    attrs = ent.chain.tostr().split(' ')
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

def 孙子定理(ent: CoreEntity):
    """#CRT [#crt]
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
    il = ent.chain.tostr().strip().split()
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

def 计算器(ent: CoreEntity):
    """#计算器 [#calc]
    计算中缀表达式
    :param exp: 待求表达式（python风格）exp
    :return:
        Union[int, float, complex]: result"""

    attrs = ent.chain.tostr().split(' ')

    player = ent.player
    if attrs[0] in GLOBAL.subscribes:
        Sniffer.overwrite(player, '#计算器', r'^[abcdefABCDEFoxj.0-9\s+-/*&^<>~=|%\(\)]+$')
        return [Plain('遇到可运算表达式直接输出结果')]
    elif attrs[0] in GLOBAL.unsubscribes:
        Sniffer.remove(player, '#计算器')
        return [Plain('禁用快速计算')]
    exp, res = evaluate_expression(''.join(attrs).replace(' ','').strip())
    return [Plain(f"{exp} = {res}")]

def 逆波兰(ent: CoreEntity):
    """#逆波兰 [#nbl]
    计算逆波兰表达式
    :param exp: 待求表达式（默认空格分隔）exp
    :return:
        Union[int, float, complex]: result"""
    attrs = ent.chain.tostr().split(' ')
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

def 老线代bot了(ent: CoreEntity):
    """#线代 []
    线代工具箱，底层是numpy，能算一些矩阵相关
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
    """
    attrs = ent.chain.tostr().split(' ')

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

def 离散闭包用工具(ent: CoreEntity):
    """#encap []
    根据所给二元组表分析关系。例子：#encap a,b a,c a,d
    """
    attrs = ent.chain.tostr().split(' ')
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

def 球盒(ent: CoreEntity):
    """#球盒 []
    求解把n个球放进m个盒子里面有多少种方案的问题。
    必须指定盒子和球以及允不允许为空三个属性。
    用法：
        #球盒 <盒子相同？(0/1)><球相同？(0/1)><允许空盒子？(0/1)> n m
    用例：
        #球盒 110 20 5
    上述命令求的是盒子相同，球相同，不允许空盒子的情况下将20个球放入5个盒子的方案数。"""
    # 参考https://www.cnblogs.com/sdfzsyq/p/9838857.html的算法
    attrs = ent.chain.tostr().split(' ')
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

def 十转(ent: CoreEntity):
    """#十转 []
    十进制转换为其他进制工具：
    输入格式：
        #十转 <目标进制> <源十进制数>
    例：
        #十转 5 261"""
    attrs = ent.chain.tostr().split(' ')
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

def 划分数个数(ent: CoreEntity):
    """#B []
    计算给定集合的划分的方案数，可以用-m选项提供求模数。用例#B 233 -m=10086s
    """
    attrs = ent.chain.tostr().split(' ')
    return [Plain(A000110_list(int(attrs[0]), meta.get('-m', 0)))]

def 素数前缀和(ent: CoreEntity):
    """#min25 []
    用min_25筛求素数的个数，分布式系统性能测试用
    用法：
        #min25 x
        命令返回小于等于x的所有素数的个数
    """
    attrs = ent.chain.tostr().split(' ')
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

def 模糊推荐(ent: CoreEntity):
    """#算命 []
    用法：
        #算命 <想法(字符串)> <心愿值(整数)>
    """
    wish, cnt = ent.chain.tostr().split(' ')
    X = float(cnt)
    import skfuzzy as fuzz 
    from skfuzzy import control as ctrl
    # import numpy
    #定义模糊控制变量
    X_craving_range=numpy.arange(0,101,1)
    X_recomend_range=numpy.arange(0,101,1)
    y_result_range=numpy.arange(0,101,1)
    craving=ctrl.Antecedent(X_craving_range,'craving')
    recomend=ctrl.Antecedent(X_recomend_range,'recomend')
    result=ctrl.Consequent(y_result_range,'result')
    #生成模糊隶属度函数

    #我的欲望模糊
    #craving.automf(3)
    craving['s']=fuzz.trimf(craving.universe,[0,0,25])
    craving['m']=fuzz.trimf(craving.universe,[0,25,75])
    craving['l']=fuzz.trimf(craving.universe,[70,100,100])
    # #ibao的推荐\
    #recomend.automf
    recomend['s']=fuzz.trimf(recomend.universe,[0,0,25])
    recomend['m']=fuzz.trimf(recomend.universe,[0,25,75])
    recomend['l']=fuzz.trimf(recomend.universe,[70,100,100])
    # #结果d
    result['s']=fuzz.trimf(result.universe,[0,0,25])
    result['m']=fuzz.trimf(result.universe,[0,35,75])
    result['l']=fuzz.trimf(result.universe,[75,100,100])
    # result['l'].view()
    #定义模糊规则
    #输出为不的规则

    rule1=ctrl.Rule(craving['s']&recomend['s'] | craving['m']&recomend['s'] | craving['s']&recomend['m'],result['s'])
    #输出为海星的规则
    rule2=ctrl.Rule(craving['l']&recomend['s'] | craving['m']&recomend['m'] | craving['l']&recomend['m'],result['m'])
    #输出为强烈推荐的规则
    rule3=ctrl.Rule(craving['l']&recomend['m'] | craving['m']&recomend['l'] | craving['l']&recomend['l'],result['l'])
    #系统和环境运行初始化
    # rule1.view()
    resulting_ctrl=ctrl.ControlSystem([rule1,rule2,rule3])
    resulting=ctrl.ControlSystemSimulation(resulting_ctrl)

    #输入
    ibaosay=random.randint(1,101)
    # wish=input("请输入你的想法：")
    # count=input("请输入你的心愿值：")
    # X=int(count)
    resulting.input['craving']=X
    resulting.input['recomend']=ibaosay
    resulting.compute()
    ret = []
    ret.append(f'关于{wish},ibao推荐值为:{ibaosay}')
    res = resulting.output["result"]
    ret.append(f'综合考虑推荐数为:{res}')
    # print(ibaosay)
    # print('综合考虑推荐数为:',end="")
    # print(resulting.output['result'])
    if(res<40):
        ret.append("这边不建议亲呢")
    elif(res>60):
        ret.append("这边强烈建议亲亲去哦")
    else:
        ret.append("亲再考虑一下吧 亲")
    return '\n'.join(ret)