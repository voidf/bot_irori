from typing import Tuple
import copy

binocular_operators = {
	'+':50,
	'-':50,
	'*':70,
	'/':70,
	'=':3,
	'==':3,
	'**':90,
	'<<':30,
	'<':3,
	'>>':30,
	'>':3,
	'&':25,
	'&&':3,
	'|':20,
	'||':3,
	'^':22,
	'%':70,
	'//':70,
	'(':1,
	')':100
}

operator_charset = '+-*/<>&|^%()=~'

binocular_calculate_map = {
    '+': lambda x,y:x+y,
    '-': lambda x,y:x-y,
    '*': lambda x,y:x*y,
    '/': lambda x,y:x/y,
    '=': lambda x,y:x is y,
    '==': lambda x,y:x==y,
    '//': lambda x,y:x//y,
    '%': lambda x,y:x%y,
    '&&': lambda x,y:x and y,
    '&': lambda x,y:x&y,
    '||': lambda x,y:x or y,
    '|': lambda x,y:x|y,
    '^': lambda x,y:x^y,
    '**': lambda x,y:x**y,
    '<<': lambda x,y:x<<y,
    '<': lambda x,y:x<y,
    '>>': lambda x,y:x>>y,
    '>': lambda x,y:x>y
}

unary_calculate_map = {
    '-': lambda x:-x,
    '~': lambda x:~x
}


def evaluate_expression(exp: str) -> Tuple[str, str]:
    """处理不带空格和其他空字符的中缀表达式
用例：
    evaluate_expression('114+514')
返回值：
    [str]计算执行顺序表达字符串, [str]计算结果"""
    operators = [] # 除括号和单目外，优先级单调递增
    operands = []
    operands_str = []
    x = []
    xx = []
    xpower = []

    suffix_exp = [] # 放2元组(本体, 类型)罢了

    last_mono = 'ope'
    cur_operator = '' # 只放双目
    float_token = False
    decimal_token = False
    hex_token = False
    octal_token = False
    binary_token = False
    complex_token = False

    def binocular_calculate(f: str, op):
        A = op.pop()
        B = op.pop()
        op.append(binocular_calculate_map[f](B,A))
        print("bino calculated:", op[-1])
    def unary_calculate(f: str, op):
        A = op.pop()
        op.append(unary_calculate_map[f](A))
        print("unary calculated:", op[-1])
    def binocular_concate(f: str, op):
        A = op.pop()
        B = op.pop()
        op.append(f"({B}{f}{A})")
        print("bino concated:", op[-1])
    def unary_concate(f: str, op):
        A = op.pop()
        op.append(f"({f}{A})")
        print("unary concated:", op[-1])

    def handle_operand():
        nonlocal x, xx, suffix_exp, float_token, complex_token, last_mono, decimal_token, xpower
        nonlocal hex_token, octal_token, binary_token
        handled = ''.join(x)
        if float_token:
            handled += '.' + ''.join(xx)
        if decimal_token:
            handled += 'e' + ''.join(xpower)
        if complex_token:
            handled += 'j'
        if handled:
            print(f'Handled operand:{handled}')
            if hex_token:
                t = int(handled, 16)
            elif octal_token:
                t = int(handled, 8)
            elif binary_token:
                t = int(handled, 2)
            elif complex_token:
                t = complex(handled)
            elif float_token or decimal_token or len(handled) > 1000:
                t = float(handled)
            else:
                try:
                    t = int(handled)
                except:
                    t = handled # 考虑未知数
            suffix_exp.append((t, 'operand'))
            last_mono = 'num'
        float_token = False
        complex_token = False
        decimal_token = False
        hex_token = False
        octal_token = False
        binary_token = False
        x = []
        xx = []
        xpower = []


    def calculate_suffix_exp():
        nonlocal operands_str, operands
        operands_str = copy.deepcopy(operands)
        for op, typ in suffix_exp:
            # op, typ = suffix_exp.pop()
            try:
                if typ == 'operand':
                    operands_str.append(f'{op}')
                    operands.append(op)
                elif typ == 'unary':
                    unary_concate(op, operands_str)
                    unary_calculate(op, operands)
                else:
                    binocular_concate(op, operands_str)
                    binocular_calculate(op, operands)
            except:
                operands = ["evaluate failed"]
                
    def maintain_stack():
        nonlocal cur_operator
        if cur_operator != '(':
            while operators:
                if operators[-1][1] == 'unary':
                    suffix_exp.append(operators.pop())
                else:
                    if binocular_operators[operators[-1][0]] >= binocular_operators[cur_operator]:
                        suffix_exp.append(operators.pop())
                    else:
                        break
        operators.append((cur_operator, 'binocular'))
        cur_operator = ''

    for c in exp:
        if c == '-' and decimal_token and not xpower:
            xpower.append(c)
        elif c == 'b' and x == ['0']:
            binary_token = True
            x.append(c)
        elif c == 'o' and x == ['0']:
            octal_token = True
            x.append(c)
        elif c == 'x' and x == ['0']:
            hex_token = True
            x.append(c)
        elif c in 'abcdefABCDEF' and hex_token:
            x.append(c)
            # c in '.je' + string.digits:
        elif c in operator_charset:
            handle_operand()
            if c == ')':
                while operators[-1][0]!='(':
                    suffix_exp.append(operators.pop())
                operators.pop()
                last_mono = 'num'

            elif cur_operator in binocular_operators and c in ('-', '~'):
                maintain_stack()
                operators.append((c, 'unary'))
                last_mono = 'ope'
            elif cur_operator in binocular_operators and c == '(':
                maintain_stack()
                operators.append((c, 'binocular'))
                last_mono = 'ope'
            elif last_mono == 'ope' and c in ('-', '~'):
                operators.append((c, 'unary'))
            elif last_mono == 'ope' and c == '(':
                operators.append((c, 'binocular'))    
            elif cur_operator + c in binocular_operators:
                cur_operator += c
        else:
            if cur_operator:
                maintain_stack()
                last_mono = 'ope'
            if c == '.':
                float_token = True
            elif c == 'j':
                complex_token = True
            elif c == 'e':
                decimal_token = True
            else:
                if decimal_token:
                    xpower.append(c)
                elif float_token:
                    xx.append(c)
                else:
                    x.append(c)
            

    handle_operand()

    if cur_operator:
        maintain_stack()
        operators.append((cur_operator, 'binocular'))

    while operators:
        suffix_exp.append(operators.pop())
    print(suffix_exp)
    extmsg = f'{[i[0] for i in suffix_exp]}'
    calculate_suffix_exp()
    return f'{extmsg}\n{operands_str[0]}', str(operands[0])


def comb(n,b):
    """从n个数里面选b个的方案数"""
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
                res = res * x
            x = x * x
            p>>=1
    else:
        while p:
            if p&1:
                res = res * x % m
            x = x * x % m
            p>>=1
    return res

def A072233_list(n: int, m: int, mod=0) -> list:
    """n个无差别球塞进m个无差别盒子方案数"""
    mod = int(mod)
    f = [[0 for j in range(m+1)] for i in range(n+1)]
    f[0][0] = 1
    for i in range(1, n+1):
        for j in range(1, min(i+1, m+1)): # 只是求到m了话没必要打更大的
            f[i][j] = f[i-1][j-1] + f[i-j][j]
            if mod: f[i][j] %= mod
    return f

def A048993_list(n: int, m: int, mod=0) -> list:
    """第二类斯特林数"""
    mod = int(mod)
    f = [1] + [0 for i in range(m)]
    for i in range(1, n+1):
        for j in range(min(m, i), 0, -1):
            f[j] = f[j-1] + f[j] * j
            if mod: f[j] %= mod
        f[0] = 0
    return f


def A000110_list(m, mod=0):
    """集合划分方案总和，或者叫贝尔数"""
    mod = int(mod)
    A = [0 for i in range(m)]
    # m -= 1
    A[0] = 1
    # R = [1, 1]
    for n in range(1, m):
        A[n] = A[0]
        for k in range(n, 0, -1):
            A[k-1] += A[k]
            if mod: A[k-1] %= mod
        # R.append(A[0])
    # return R
    return A[0]

def exgcd(a,b):
    if not b:
        return 1,0
    y,x = exgcd(b,a%b)
    y -= a//b * x
    return x,y

def getinv(a,m):
    x,y = exgcd(a,m)
    return -1 if x==1 else x%m
    
def orafli(upp):
    primes = []
    marked = [False for i in range(upp+3)]
    # prvs = [i for i in range(upp+3)]
    pref = []
    for i in range(2, upp):
        if not marked[i]:
            primes.append(i)
            pref.append(primes[-1])
        for j in primes:
            if i*j >= upp:
                break
            marked[i*j] = True
            # prvs[i*j] = j
            if i % j == 0:
                break
    return primes, pref

# 树巨结垢相关

def lowbit(x:int): return x&-x

def treearray_update(pos:int,x:int,array:list):
    while pos < len(array):
        array[pos] += x
        pos += lowbit(pos)

def treearray_getsum(pos:int,array:list) -> int:
    ans = 0
    while pos > 0:
        ans += array[pos]
        pos -= lowbit(pos)
    return ans

def calcinvs(array:list):
    """树状数组求逆序对"""
    d = {}
    for k,v in enumerate(sorted(array)):
        d[v] = k+1
    treearray = [0 for i in range(1+len(array))]
    invs = 0
    for i in array:
        invs += treearray_getsum(len(treearray)-1, treearray) - treearray_getsum(d[i], treearray)
        treearray_update(d[i],1,treearray)
    return invs


