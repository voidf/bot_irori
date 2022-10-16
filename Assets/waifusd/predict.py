import jieba
import pickle
import random
import re
with open('cn_cheatsheet_dict.pkl', 'rb') as f:
    d = pickle.load(f)

jieba.load_userdict('cn_cheatsheet.dict')

inp = '给爷来张贫乳白毛萝莉兽耳娘，不要男的，1280c720分辨率'

c = list(jieba.cut(inp))


# def get_resolution(src): return re.compile(r'([0-9]+)[x\*]([0-9]+)').search(src).groups()
# print(get_resolution(inp))

# negtokens = ['不要', '别']

# tokens = [
#     [], []
# ]
# hint_position = 0


# for sp in c:
#     if sp in negtokens:
#         hint_position = 1
#     else:
#         if v := d.get(sp):
#             tokens[hint_position].append(v)

print(c)
