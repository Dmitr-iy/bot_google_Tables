from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbackdata import Write, WriteWorksheet, WriteData, WriteUpdate, Admin
from utils.fun_gspread import get_spreadsheet_names, get_sheets_names, get_ws_row


def write_kb():
    builder = InlineKeyboardBuilder()

    names = get_spreadsheet_names()
    print("Writing", names)
    for name in names:
        builder.button(
            text=name,
            callback_data=Write(nam=name).pack()
        )

    builder.adjust(2)
    return builder.as_markup()

def write_name_ws(sheet_id):
    builder = InlineKeyboardBuilder()
    worksheet_names = get_sheets_names(sheet_id)
    print('working ws kb', worksheet_names)
    for name in worksheet_names:
        builder.button(
            text=name,
            callback_data=WriteWorksheet(write_ws=name).pack()
        )

    builder.button(
        text="назад",
        callback_data=WriteWorksheet(write_ws='back').pack()
    )

    builder.adjust(3)
    return builder.as_markup()

def write_ws_data(ws, sheet_id):
    builder = InlineKeyboardBuilder()
    print("sh_id", sheet_id)
    write_view_row1 = get_ws_row(ws, sheet_id)
    print("write_view_row1", write_view_row1)
    for row in write_view_row1:
        builder.button(
            text=row,
            callback_data=WriteData(write_data=row).pack()
        )

    builder.button(
        text="все строки",
        callback_data=WriteData(write_data="all").pack()
    )
    builder.button(
        text="добавить столбец",
        callback_data=WriteData(write_data="add").pack()
    )

    builder.button(
        text="назад",
        callback_data=WriteData(write_data='back').pack()
    )
    builder.adjust(2, 2)
    return builder.as_markup()

def write_yes_no():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="да, изменить",
        callback_data=WriteUpdate(write_="yes").pack()
    )

    builder.button(
        text="нет, не менять",
        callback_data=WriteUpdate(write_="not").pack()
    )

    builder.adjust(1)

    return builder.as_markup()

def kb_admin():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="clear files",
        callback_data=Admin(admin="clear").pack()
    )
    builder.button(
        text="delete messages from users",
        callback_data=Admin(admin="delete").pack()
    )
    builder.adjust(1)
    return builder.as_markup()
