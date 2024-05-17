from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.callbackdata import KbNewFile, KbNewFil, KbNewFiles
from utils.fun_gspread import get_spreadsheet_names


def create_file_y_n():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="да",
        callback_data=KbNewFiles(select_tables="yes").pack()
    )

    builder.button(
        text="нет",
        callback_data=KbNewFiles(select_tables="not").pack()
    )

    builder.adjust(1)

    return builder.as_markup()

def select_table():
    builder = InlineKeyboardBuilder()

    names_spreadsheet = get_spreadsheet_names()
    for name in names_spreadsheet:
        builder.button(
            text=name,
            callback_data=KbNewFil(select_tabl=name).pack()
        )

    builder.adjust(2, 2)

    return builder.as_markup()

def kb_start():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="таблицу в новом файле",
        callback_data=KbNewFile(select_table="create").pack()
    )

    builder.button(
        text="таблицу на новом листе",
        callback_data=KbNewFile(select_table="create_sheet").pack()
    )
    builder.adjust(1)
    return builder.as_markup()
