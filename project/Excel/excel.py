import openpyxl as xl

a = xl.load_workbook('../../test_data/IU4.xlsx')
sheet = a['ИУ4-23Б']

for i in range(3, sheet.max_row - 1):
    print(sheet.cell(row=i, column=1).value, sheet.cell(row=i, column=2).value)