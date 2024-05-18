import logging
import os
import gspread
from google.oauth2.service_account import Credentials
from gspread import Spreadsheet, Client, WorksheetNotFound
from data.config import config_settings


SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive'
          ]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)
gc: Client = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
folder_id = config_settings.folder_id.get_secret_value()

def get_spreadsheet_names():
    try:
        spreadsheets = gc.list_spreadsheet_files()
        spreadsheet_names = [spreadsheet['name'] for spreadsheet in spreadsheets]
        return spreadsheet_names
    except Exception as e:
        logging.exception(e)

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
    sh_url: Spreadsheet = gc.open_by_key(sh.id)
    sh.share(f'{config_settings.email_admin}', perm_type='user', role='writer')
    sh.share(f'{config_settings.email_user}', perm_type='user', role='writer')
    ws = sh.get_worksheet(0)
    ws.update_title(name_worksheets)
    ws.resize(sum_rows, sum_cols)
    return sh_url.id

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
    try:
        spreadsheet = gc.open(spreadsheet_name)
        return spreadsheet.id
    except gspread.SpreadsheetNotFound as e:
        logging.error(f"Spreadsheet not found: {e}")

def get_ws_column(ws, sheet_id):
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet(ws)
        all_values = worksheet.get_all_values()
        first_column_data = [row[0] for row in all_values[1:]]
        return first_column_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_sheets_names(sheet_id):
    try:
        sheet = gc.open_by_key(sheet_id)
        sheet_names = sheet.worksheets()
        sheet_names = [sheet.title for sheet in sheet_names]
        return sheet_names
    except gspread.SpreadsheetNotFound as e:
        logging.error(f"Spreadsheet not found: {e}")

def get_ws_row(ws, sheet_id):
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet(ws)
        values_list = worksheet.row_values(1)
        return values_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_cell(ws, sheet_id):
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet(ws)
        cell = worksheet.cell(1, 1).value
        return cell
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_all_sheet(sheet_id, work_sheet):
    sheet = gc.open_by_key(sheet_id)
    try:
        worksheet = sheet.worksheet(work_sheet)
        all_values = worksheet.get_all_values()
        return all_values
    except WorksheetNotFound as e:
        logging.error(f"Worksheet '{work_sheet}' not found in spreadsheet '{sheet_id}': {e}")
        return None

def get_sheet_row_object(sheet_id, work_sheet, obj_list):
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet(work_sheet)
        cell = worksheet.find(obj_list)
        row_number = cell.row
        row_number_obj = worksheet.row_values(row_number)
        row_number_one = worksheet.row_values(1)
        row_object = row_number_one, row_number_obj
        return row_object
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_sheet_column_object(sheet_id, work_sheet, obj_list):
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet(work_sheet)
        cell = worksheet.find(obj_list)
        column_number = cell.col
        column_number_obj = worksheet.col_values(column_number)
        column_number_one = worksheet.col_values(1)
        column_object = column_number_one, column_number_obj
        return column_object
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_worksheet_list(name):
    try:
        sheet = gc.open(name)
        worksheets = sheet.worksheets()
        worksheets = [worksheet.title for worksheet in worksheets]
        return worksheets
    except gspread.SpreadsheetNotFound:
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def delete_worksheets(name_spreadsheet, name):
    try:
        sheet = gc.open(name_spreadsheet)
        worksheet = sheet.worksheet(name)
        sheet.del_worksheet(worksheet)
        return True
    except gspread.SpreadsheetNotFound:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def create_worksheet(table, name_spreadsheet, sum_rows, sum_cols):
    try:
        sheet = gc.open(table)
        sheet.add_worksheet(title=name_spreadsheet, rows=sum_rows, cols=sum_cols)
        return True
    except gspread.SpreadsheetNotFound:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
