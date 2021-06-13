from GLOBAL import *
from database_utils import *

import os


for i in os.listdir('credits/'):
    print(i)
    with open(f"credits/{i}", 'r') as f:
        c =int(f.read().strip())
        ent = CreditLog.chk(i)
        ent.credit = c
        ent.save()