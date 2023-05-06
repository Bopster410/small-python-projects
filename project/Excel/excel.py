import openpyxl as xl

a = xl.load_workbook('test_data/IU4.xlsx')
sheet = a['ИУ4-23Б']

for row in sheet.iter_rows(min_row=3, max_row=sheet.max_row - 2):
    print(f'{row[0].value}: ', end='')
    for cell in row[1:]:
        if cell.value == None:
            print('')
            break
        print(cell.value, end=' ')