import openpyxl as xl, sys

a = xl.load_workbook(sys.argv[1])
sheet = a['ИУ4-23Б']

for row in sheet.iter_rows(min_row=3, max_row=sheet.max_row - 2):
    print(f'{row[0].value}: ', end='')
    for cell in row[1:]:
        if cell.value == None:
            print('')
            break
        print(cell.value, end=' ')