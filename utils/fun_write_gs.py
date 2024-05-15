import gspread
from utils.fun_gspread import gc


def get_cell_data(sheet_id, work_sheet):
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.worksheet(work_sheet)
    cell = worksheet.cell(1, 1).value
    return cell

def get_col1_data(sheet_id, work_sheet):
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.worksheet(work_sheet)
    col1 = worksheet.col_values(1)
    return col1

def write_data_col1(sheet_id, work_sheet, last_row, cell_):
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.worksheet(work_sheet)
    worksheet.update(f"A{last_row}:A{last_row}", [[cell_]])
    return True

def cell_number(sheet_id, work_sheet):
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.worksheet(work_sheet)
    cell = worksheet.cell(1, 1).value
    return cell

def write_range_data(sheet_id, work_sheet, range_name_obj, data_, cell_data):
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.worksheet(work_sheet)
    cell_row = worksheet.find(range_name_obj)
    row_number = cell_row.row
    print("row_number: ", row_number)
    cell_col = worksheet.find(data_)
    column_number = cell_col.col
    print("column_number: ", column_number)
    try:
        save = worksheet.update_cell(row_number, column_number, cell_data)
        if save:
            return True
    except gspread.exceptions.APIError as e:
        print(f"Error updating cell: {e}")
        return False

def examination_cell(sheet_id, work_sheet, cell_data, data_):
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.worksheet(work_sheet)
    cell_row = worksheet.find(cell_data)
    row_number = cell_row.row
    print("row_number: ", row_number)
    cell_col = worksheet.find(data_)
    column_number = cell_col.col
    cell = worksheet.cell(row_number, column_number).value
    print("cell: ", cell)
    return cell

def get_cell_row1(sheet_id, work_sheet):
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.worksheet(work_sheet)
    cell = worksheet.row_values(1)
    row_first = [col for col in cell[1:]]
    return row_first

def write_all_datas(sheet_id, work_sheet, all_datas):
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.worksheet(work_sheet)
    all_datas = all_datas.split(",")
    print('all_datas functions', all_datas)
    next_empty_row = len(worksheet.get_all_values()) + 1
    data = [cell if cell != '0' else '' for cell in all_datas]
    print('data: ', data)
    for i, element in enumerate(data, start=1):
        worksheet.update_cell(next_empty_row, i, element)
    return True
