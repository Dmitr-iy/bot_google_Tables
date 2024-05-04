from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbackdata import Start


def start_kb():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Начать",
        callback_data=Start(choice="start").pack()
    )

    builder.button(
        text="Инструкции",
        callback_data=Start(choice="help").pack()
    )
    return builder.as_markup()
