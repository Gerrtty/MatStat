from openpyxl import load_workbook

def read_data():

    zeros_data = []
    ones_data = []
    all_data = []
    boolean_arr = []

    wb = load_workbook('../data.xlsx')
    sheet = wb.get_sheet_by_name('Лист1')

    for i in range(1, 50):
        boolean_arr.append(sheet[f'A{i + 1}'].value)
        all_data.append(sheet[f'L{i + 1}'].value)

    for i in range(len(all_data)):
        if boolean_arr[i] == 0:
            zeros_data.append(all_data[i])
        else:
            ones_data.append(all_data[i])

    return zeros_data, ones_data, boolean_arr, all_data