from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbackCreate import KbNewFile


def create_file_y_n():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="да",
        callback_data=KbNewFile(yes_no_new="yes").pack()
    )

    builder.button(
        text="нет",
        callback_data=KbNewFile(yes_no_new="not").pack()
    )

    builder.adjust(1)

    return builder.as_markup()
