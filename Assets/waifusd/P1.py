import xlrd
wb: xlrd.book.Book = xlrd.open_workbook('cn_cheatsheet.xls')

# sheet = wb.sheet_by_name('C8')

d = {}
l = []

# ctr = 0
def fil(src):
    return src.replace('\n', ',').replace('_', ' ').strip().replace(', ', ',').replace(' ,', ',').removesuffix(',').strip().replace('{', '(').replace('}', ')')

for sheet in wb.sheets():
    match sheet.name[0]:
        case 'C':
            for ci in range(0, sheet.ncols, 2):
                if ci+1 >= sheet.ncols:
                    break
                for ri in range(sheet.nrows):
                    # if sheet.cell(ri, ci).ctype and sheet.cell(ri, ci+1).ctype == 1:
                    cv: str = fil(str(sheet.cell(ri, ci).value))
                    cv2: str = fil(str(sheet.cell(ri, ci+1).value))
                    if cv and cv2:
                        v = cv2.split('/')
                        for k in cv.split('/'):
                            if k in d:
                                print(k, d[k], v)
                                for vx in v:
                                    flg = True
                                    for dx in d[k]:
                                        if vx in dx:
                                            flg = False
                                            break
                                    if flg:
                                        d[k].append(vx)
                                print(k, d[k], v)
                                
                            else:
                                d[k] = v
        case 'I':
            for ci in range(sheet.ncols):
                for ri in range(sheet.nrows):
                    # if sheet.cell(ri, ci).ctype and sheet.cell(ri, ci+1).ctype == 1:
                    cv: str = fil(str(sheet.cell(ri, ci).value))
                    if cv:
                        l.append(cv)
print(len(d), len(l))
import pickle
with open('cn_cheatsheet_dict.pkl', 'wb') as f:
    pickle.dump(d, f)
with open('cn_cheatsheet_list.pkl', 'wb') as f:
    pickle.dump(l, f)
# with open('cn_cheatsheet.dict', 'w', encoding='utf-8') as f:
#     for k in d.keys():
#         f.write(k+'\n')
