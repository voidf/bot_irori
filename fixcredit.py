import re
import os

for i in os.listdir('credits/'):
    print(i)
    mx = 500
    with open('credits/'+i,'r') as f:
        for res in re.findall(r'[0-9]+',f.read()):
            print('\t',res)
            mx = max(mx, int(res))
    with open('credits/'+i,'w') as f:
        f.write(f"{mx}")

