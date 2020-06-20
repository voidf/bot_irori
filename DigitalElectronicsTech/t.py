import json5

s='''
{a:"b\\n\
"}
'''
with open('TTL.json5','r',encoding='utf-8') as f:
    print(json5.load(f))