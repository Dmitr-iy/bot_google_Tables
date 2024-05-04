from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbackCreate import KbStart


def kb_start():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="таблицу в новом файле",
        callback_data=KbStart(type="create").pack()
    )

    builder.button(
        text="таблицу на новом листе",
        callback_data=KbStart(type="create_sheet").pack()
    )
    builder.adjust(1)
    return builder.as_markup()
