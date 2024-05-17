import gspread
from utils.fun_gspread import gc


def get_cell_data(sheet_id, work_sheet):
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet(work_sheet)
        cell = worksheet.cell(1, 1).value
        return cell
    except gspread.exceptions.APIError as e:
        print(f"Error getting cell data: {e}")
        return None

def get_col1_data(sheet_id, work_sheet):
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet(work_sheet)
        col1 = worksheet.col_values(1)
        return col1
    except gspread.exceptions.APIError as e:
        print(f"Error getting column 1: {e}")
        return None
def write_data_col1(sheet_id, work_sheet, last_row, cell_):
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet(work_sheet)
        current_rows = worksheet.row_count
        if last_row > current_rows:
            worksheet.add_rows(last_row - current_rows)
        worksheet.update(f"A{last_row}:A{last_row}", [[cell_]])
        return True
    except gspread.exceptions.APIError as e:
        print(f"Error updating cell: {e}")
        return False

def cell_number(sheet_id, work_sheet):
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet(work_sheet)
        cell = worksheet.cell(1, 1).value
        return cell
    except gspread.exceptions.APIError as e:
        print(f"Error getting cell: {e}")
        return None

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
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet(work_sheet)
        cell_row = worksheet.find(cell_data)
        row_number = cell_row.row
        cell_col = worksheet.find(data_)
        column_number = cell_col.col
        cell = worksheet.cell(row_number, column_number).value
        return cell
    except gspread.exceptions.APIError as e:
        print(f"Error updating cell: {e}")
        return False

def get_cell_row1(sheet_id, work_sheet):
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet(work_sheet)
        cell = worksheet.row_values(1)
        row_first = [col for col in cell[1:]]
        return row_first
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def write_all_datas(sheet_id, work_sheet, all_datas):
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet(work_sheet)
        all_datas = all_datas.split(",")
        print('all_datas functions', all_datas)
        next_empty_row = len(worksheet.get_all_values()) + 1
        current_rows = worksheet.row_count
        if next_empty_row > current_rows:
            worksheet.add_rows(next_empty_row - current_rows)
        data = [cell if cell != '0' else '' for cell in all_datas]
        print('data: ', data)
        for i, element in enumerate(data, start=1):
            worksheet.update_cell(next_empty_row, i, element)
        return True
    except gspread.exceptions.APIError as e:
        print(f"Error updating cell: {e}")
        return False

def write_new_col(sheet_id, work_sheet, data_col, data_row):
    print('sheet_id', sheet_id)
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet(work_sheet)
        current_rows = worksheet.row_count
        if len(data_row) > current_rows:
            worksheet.add_rows(len(data_row) - current_rows + 1)
        current_cols = worksheet.col_count
        if len(data_col) > current_cols:
            worksheet.add_cols(len(data_col) - current_cols)
        for i, cell in enumerate(data_row, start=1):
            worksheet.update_cell(i+1, 1, cell)
        for j, cell in enumerate(data_col, start=1):
            worksheet.update_cell(1, j, cell)
        return True
    except gspread.exceptions.APIError as e:
        print(f"Error adding columns: {e}")
        return False

def add_column(sheet_id, work_sheet, num_columns):
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet(work_sheet)
        worksheet.add_cols(num_columns)
        return True
    except gspread.exceptions.APIError as e:
        print(f"Error adding columns: {e}")
        return False

def add_column_name(sheet_id, work_sheet, num_columns, column_names):
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet(work_sheet)
        for i in range(num_columns):
            worksheet.update_cell(1, worksheet.col_count - num_columns + 1 + i, column_names[i])
        return True
    except gspread.exceptions.APIError as e:
        print(f"Error adding column names: {e}")
        return False
