from Worker import task
from basicutils.socketutils import *

def teststr(s: str):
    print(f"<<<\t[{s}]")
    res = task.delay(CoreEntity.wrap_strchain(s).json())
    
    resp: CoreEntity = CoreEntity.handle_json(res.get(timeout=3))
    res.forget()
    print(f">>>\t{resp.chain.tostr()}\n")


# Math
teststr('#h #C')
teststr('#C 4 2')
teststr('#h #A')
teststr('#A 4 3')
teststr('#h #K')
teststr('#K 5')
teststr('#h #stat')
teststr('#stat 1 3 2.5')
