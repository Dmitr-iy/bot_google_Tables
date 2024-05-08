import gspread
from google.oauth2.service_account import Credentials
from gspread import Spreadsheet, Client
from utils.func_google import SERVICE_ACCOUNT_FILE, SCOPES
from data.config import config_settings


credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)
gc: Client = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
folder_id = config_settings.folder_id.get_secret_value()

def get_spreadsheet_names():
    spreadsheets = gc.list_spreadsheet_files()
    spreadsheet_names = [spreadsheet['name'] for spreadsheet in spreadsheets]
    return spreadsheet_names

async def examination_name(name):
    print(name)
    print(folder_id)
    file_list = gc.list_spreadsheet_files()
    for file in file_list:
        if file['name'].lower() == name.lower():
            return file['id']
    return None

async def create_spreadsheet(name, name_worksheets, sum_rows, sum_cols):
    sh: Spreadsheet = gc.create(name, folder_id=folder_id)
    sh_url: Spreadsheet = gc.open_by_url(sh.url)
    sh.share('kosheld89@gmail.com', perm_type='user', role='writer')
    # open_sh = gc.open_by_key(sh_url.url)
    ws = sh.get_worksheet(0)
    ws.update_title(name_worksheets)
    ws.resize(sum_rows, sum_cols)
    return sh_url.url

async def delete_spreadsheet(name):
    try:
        # Получаем объект таблицы по названию
        spreadsheet = gc.open(name)
        # Удаляем таблицу
        gc.del_spreadsheet(spreadsheet.id)
        return True
    except gspread.SpreadsheetNotFound:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def get_spreadsheet_id(spreadsheet_name):
    return gc.open(spreadsheet_name).id


def get_ws_column(ws, sheet_id):
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.worksheet(ws)
    # Get all values from the worksheet
    all_values = worksheet.get_all_values()
    # Extract data from the first column, skipping the first row
    first_column_data = [row[0] for row in all_values[1:]]
    return first_column_data

def get_sheets_names(sheet_id):
    sheet = gc.open_by_key(sheet_id)
    sheet_names = sheet.worksheets()
    sheet_names = [sheet.title for sheet in sheet_names]
    return sheet_names

def get_ws_row(ws, sheet_id):
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.worksheet(ws)
    values_list = worksheet.row_values(1)
    return values_list

def get_cell(ws, sheet_id):
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.worksheet(ws)
    cell = worksheet.cell(1, 1).value
    return cell

def get_all_sheet(sheet_id, work_sheet):
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.worksheet(work_sheet)
    all_values = worksheet.get_all_values()
    return all_values

def get_sheet_row_object(sheet_id, work_sheet, obj_list):
    print('worksheet', work_sheet)
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.worksheet(work_sheet)
    print('cell', obj_list)
    cell = worksheet.find(obj_list)
    row_number = cell.row
    row_number_obj = worksheet.row_values(row_number)
    row_number_one = worksheet.row_values(1)
    row_object = row_number_one, row_number_obj
    return row_object

def get_sheet_column_object(sheet_id, work_sheet, obj_list):
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.worksheet(work_sheet)
    cell = worksheet.find(obj_list)
    column_number = cell.col
    column_number_obj = worksheet.col_values(column_number)
    column_number_one = worksheet.col_values(1)
    column_object = column_number_one, column_number_obj
    return column_object
