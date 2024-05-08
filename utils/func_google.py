import os
import requests
from googleapiclient.discovery import build
from google.oauth2 import service_account
from typing import List, Any
from data.config import config_settings


SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive'
          ]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()


async def read_from_sheet(sheet_id, range_):
    try:
        result = sheet.values().get(spreadsheetId=sheet_id, range=range_).execute()
        values = result.get('values', [])
        return values
    except Exception as e:
        print(f"An error occurred while reading from the sheet: {e}")
        return None

async def get_sheet_names():
    sheet_metadata = service.spreadsheets().get(spreadsheetId=config_settings.sheet_id2.get_secret_value()).execute()
    sheets = sheet_metadata.get('sheets', [])
    sheet_names = [sheet['properties']['title'] for sheet in sheets]
    return sheet_names

async def append_to_sheet(sheet_id, range_, values):
    body = {'values': values}
    try:
        sheet.values().append(
            spreadsheetId=sheet_id,
            range=range_,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        return True
    except Exception as e:
        print("Error occurred while appending data to sheet:", e)
        return False

async def find_matching_objects(name: str) -> List[str]:
    sheet_id = config_settings.sheet_id.get_secret_value()
    # Прочитайте данные из столбца A на листе "объекты"
    result = await read_from_sheet(sheet_id, 'объекты!A:A')

    if result is None:
        return []  # Если чтение не удалось, вернуть пустой список объектов
        # Преобразуйте результат в одномерный список
    objects = [item for sublist in result for item in sublist]
    # Найдите все объекты, содержащие введенное пользователем слово (без учета регистра)
    matching_objects = [obj for obj in objects if name.lower() in obj.lower()]
    return matching_objects

async def update_sheet(sheet_id: str, range_: str, values: List[List[Any]]) -> bool:
    try:
        # Обновление данных в таблице
        request = service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=range_,
            valueInputOption='RAW',
            body={'values': values}
        )
        response = request.execute()
        return True
    except Exception as e:
        print(f"An error occurred while updating the sheet: {e}")
        return False

async def append_to_sheet1(sheet_id, sheet_name, rows):
    # Convert the list of rows to a JSON-like structure
    data = {"values": rows}

    # Send the request to append the rows to the sheet
    response = requests.post(
        f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{sheet_name}::append",
        json=data,
        headers={
            "Authorization": f"Bearer {config_settings.google_api_key.get_secret_value()}",
            "Content-Type": "application/json",
        },
    )

    # Check if the request was successful
    if response.status_code == 200:
        return True
    else:
        return False

def get_sheets_names(sheet_id):
    try:
        # Получение метаданных таблицы по её ID
        spreadsheet_metadata = service.spreadsheets().get(
            spreadsheetId=sheet_id,
            fields="sheets.properties.title"
        ).execute()

        # Извлечение названий всех листов из метаданных
        sheet_names = [sheet['properties']['title'] for sheet in spreadsheet_metadata['sheets']]

        return sheet_names
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
