from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbackdata import WritePrice2, WriteConsumables2, WriteTool2, WriteCar, WritePetrol, WriteSalary


def price_update():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="добавить сумму",
        callback_data=WritePrice2(write_price2="+").pack()
    )

    builder.button(
        text="уменьшить сумму",
        callback_data=WritePrice2(write_price2="-").pack()
    )

    builder.button(
        text="полностью изменить",
        callback_data=WritePrice2(write_price2="all").pack()
    )

    builder.adjust(2, 1)

    return builder.as_markup()


def cons_update():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="добавить сумму",
        callback_data=WriteConsumables2(write_consumables2="+").pack()
    )

    builder.button(
        text="уменьшить сумму",
        callback_data=WriteConsumables2(write_consumables2="-").pack()
    )

    builder.button(
        text="полностью изменить",
        callback_data=WriteConsumables2(write_consumables2="all").pack()
    )

    builder.adjust(2, 1)

    return builder.as_markup()

def tool_update():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="добавить сумму",
        callback_data=WriteTool2(write_tool2="+").pack()
    )

    builder.button(
        text="уменьшить сумму",
        callback_data=WriteTool2(write_tool2="-").pack()
    )

    builder.button(
        text="полностью изменить",
        callback_data=WriteTool2(write_tool2="all").pack()
    )

    builder.adjust(2, 1)

    return builder.as_markup()

def car_update():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="добавить сумму",
        callback_data=WriteCar(write_car2="+", write_car="").pack()
    )

    builder.button(
        text="уменьшить сумму",
        callback_data=WriteCar(write_car2="-", write_car="").pack()
    )

    builder.button(
        text="полностью изменить",
        callback_data=WriteCar(write_car2="all", write_car="").pack()
    )

    builder.adjust(2, 1)

    return builder.as_markup()

def petrol_update():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="добавить сумму",
        callback_data=WritePetrol(write_petrol_obj2="+", write_petrol_obj="").pack()
    )

    builder.button(
        text="уменьшить сумму",
        callback_data=WritePetrol(write_petrol_obj2="-", write_petrol_obj="").pack()
    )

    builder.button(
        text="полностью изменить",
        callback_data=WritePetrol(write_petrol_obj2="all", write_petrol_obj="").pack()
    )
    builder.adjust(2, 1)
    return builder.as_markup()


def salary_update():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="добавить сумму",
        callback_data=WriteSalary(write_salary2="+", write_salary="").pack()
    )

    builder.button(
        text="уменьшить сумму",
        callback_data=WriteSalary(write_salary2="-", write_salary="").pack()
    )

    builder.button(
        text="полностью изменить",
        callback_data=WriteSalary(write_salary2="all", write_salary="").pack()
    )
    builder.adjust(2, 1)
    return builder.as_markup()
