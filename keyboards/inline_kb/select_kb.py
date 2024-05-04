from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbackdata import Select, SelectDelete, SelectSheet
from utils.fun_gspread import get_spreadsheet_names
from utils.func_google import get_sheets_names


def select_kb():
    builder = InlineKeyboardBuilder()

    names = get_spreadsheet_names()
    for name in names:
        builder.button(
            text=name,
            callback_data=Select(select_view=name, view_sheet="").pack()
        )

    builder.adjust(2)
    return builder.as_markup()

def select_ws_view(sheet_id):
    print("Select", sheet_id)
    builder = InlineKeyboardBuilder()
    sheet_names = get_sheets_names(sheet_id)
    print("Select", sheet_names)
    print("id", sheet_id)
    for name in sheet_names:
        builder.button(
            text=name,
            callback_data=SelectSheet(select_sheet=name, sheet_id='').pack()
        )

    builder.adjust(2)
    return builder.as_markup()

def select_delete_kb():
    builder = InlineKeyboardBuilder()

    names_spreadsheet = get_spreadsheet_names()
    for name in names_spreadsheet:

        builder.button(
            text=name,
            callback_data=SelectDelete(select_del=name).pack()
        )

    builder.adjust(2, 2)

    return builder.as_markup()
