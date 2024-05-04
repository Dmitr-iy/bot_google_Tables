from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbackdata import ViewObject


def get_object(objects):
    builder = InlineKeyboardBuilder()
    for obj in objects:
        builder.button(
            text=obj,
            callback_data=ViewObject(views=obj).pack()
        )

    builder.adjust(2)

    return builder.as_markup()
