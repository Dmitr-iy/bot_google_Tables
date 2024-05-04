from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbackdata import ViewObject, ViewSelect, ViewRow
from utils.fun_gspread import get_ws_column, get_ws_row


def view_sheet_column(ws, sheet_id):
    builder = InlineKeyboardBuilder()
    print("view_", ws)
    print("view_", sheet_id)
    result = get_ws_column(ws, sheet_id)
    print(result)
    for row in result:
        builder.button(
            text=row,
            callback_data=ViewObject(views=row).pack()
        )

    builder.button(
        text="весь лист",
        callback_data=ViewObject(views="all").pack()
    )

    builder.button(
        text="по строке ",
        callback_data=ViewObject(views="column").pack()
    )

    builder.adjust(1, 2, 1)
    return builder.as_markup()

def view_sheet_row(ws, sheet_id):
    builder = InlineKeyboardBuilder()
    result = get_ws_row(ws, sheet_id)
    for row in result:
        builder.button(
            text=row,
            callback_data=ViewRow(view_row=row).pack()
        )

    builder.button(
        text="весь лист",
        callback_data=ViewRow(view_row="all").pack()
    )

    builder.button(
        text="по столбцу",
        callback_data=ViewSelect(view="column").pack()
    )

    builder.adjust(1, 2, 1)
    return builder.as_markup()

def select_row_colm():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="по столбцу",
        callback_data=ViewSelect(view="column").pack()
    )

    builder.button(
        text="по строке",
        callback_data=ViewSelect(view="row").pack()
    )

    builder.adjust(1)

    return builder.as_markup()
