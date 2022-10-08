# 处理tg导出聊天文件，导出自群组https://t.me/+a590kmLPEhlkM2Ux
import json
import pickle
from collections import Counter

# with open('result.json', 'r', encoding='utf-8') as f:
#     j = json.load(f)

# msgs = j['messages']
# print(len(msgs))

# li = []

# def G(j: dict, x):
#     if not isinstance(j, dict) or x not in j:
#         return None
#     else:
#         return j[x]

# def I(j: list, x):
#     if (not isinstance(j, list)) or (len(j) <= x):
#         return None
#     else:
#         return j[x]

# for i in msgs:
#     if t := G(i, 'text'):
#         if fir := I(t, 0):
#             if cmd := G(fir, 'type'):
#                 if cmd == 'bot_command' and fir['text'] in ('/ai_nsfw_p', '/ai_nsfw_l', '/ai_sfw_p', '/ai_sfw_l'):
#                     if sec := I(t, 1):
#                         if isinstance(sec, str):
#                             if sec := sec.strip():
#                                 li.append(sec)

# print(len(li))
# with open('prompts.pickle', 'wb') as f:
#     pickle.dump(li, f)

# with open('prompts.txt', 'w', encoding='utf-8') as f:
#     f.writelines(li)

buf = []

import re
import string

p = re.compile(r'[0-9A-Za-z\s]+')
with open('prompts.pickle', 'rb') as f:
    li = pickle.load(f)

tokens = Counter()

cs = string.ascii_lowercase + string.ascii_uppercase + string.digits + ' '

for i in li:
    for j in i:
        if j in cs:
            buf.append(j)
        else:
            output = ''.join(buf).strip().lower()
            buf.clear()
            if output:
                tokens[output]+=1
    # r = re.findall(p, i)
    # for j in r:
        # tokens.add(j)
print(len(tokens))
with open('chat_tokens.txt', 'w') as f:
    for x in tokens.most_common():
        f.write(f"{x[1]},{x[0]}\n")
    # assert len(i.strip()) > 0