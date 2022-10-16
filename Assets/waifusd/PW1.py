import xlrd, xlwt
wb: xlrd.book.Book = xlrd.open_workbook('cn_cheatsheet.xls')

sheet = wb.sheet_by_name('C8')

wwb = xlwt.Workbook('utf-8')
wst = wwb.add_sheet('C8')


# for sheet in wb.sheets():
ctr = 0
for ci in range(0, sheet.ncols, 2):
    for ri in range(sheet.nrows):
        if sheet.cell(ri, ci).ctype and sheet.cell(ri, ci+1).ctype == 1:
            cv: str = sheet.cell(ri, ci).value
            cv2: str = sheet.cell(ri, ci+1).value
            if 'hair' in cv2:
                if cv.endswith('色头发'):
                    wst.write(ctr, 2, cv.removesuffix('色头发')+'毛')
                    wst.write(ctr, 3, cv2)
                    # sheet.put_cell(ctr, 2, 1, cv.removesuffix('色头发')+'毛', 0)
                    # sheet.put_cell(ctr, 3, 1, cv2, 0)
                    print(cv,cv2)
                    ctr+=1
                elif cv.endswith('发'):
                    wst.write(ctr, 2, cv.removesuffix('发')+'毛')
                    wst.write(ctr, 3, cv2)
                    # sheet.put_cell(ctr, 2, 1, cv.removesuffix('发')+'毛', 0)
                    # sheet.put_cell(ctr, 3, 1, cv2, 0)
                    print(cv,cv2)
                    ctr += 1
        # print(sheet)
        # print(dir(sheet))
wwb.save("O1.xls")
# with open('X1.xls', 'wb') as f:
#     xlrd.dump('O1.xls', f)