from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbackdata import Write
from utils.fun_gspread import get_spreadsheet_names


def write_kb():
    builder = InlineKeyboardBuilder()

    names = get_spreadsheet_names()
    for name in names:
        builder.button(
            text=name,
            callback_data=Write(write="write", nam=name, all_write="").pack()
        )

    builder.adjust(3)
    return builder.as_markup()

    # builder.button(
    #     text="объекты",
    #     callback_data=Write(write="object", nam="", all_write="").pack()
    # )
    #
    # builder.button(
    #     text="сотрудники",
    #     callback_data=Write(write="workers", nam="", all_write="").pack()
    # )
    #
    # builder.button(
    #     text="покупки",
    #     callback_data=Write(write="buy", nam="", all_write="").pack()
    # )
    #
    # builder.button(
    #     text="расходники",
    #     callback_data=Write(write="consumables", nam="", all_write="").pack()
    # )
    #
    # builder.button(
    #     text="инструменты",
    #     callback_data=Write(write="tools", nam="", all_write="").pack()
    # )
    #
    # builder.button(
    #     text="бюджет",
    #     callback_data=Write(write="budget", nam="", all_write="").pack()
    # )

