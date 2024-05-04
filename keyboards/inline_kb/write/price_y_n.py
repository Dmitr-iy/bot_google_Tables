from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbackdata import WritePrice, WritePrice2, WriteTool, WriteCar, WritePetrol, WriteSalary, Write, WriteAll


def name_yes_no():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="да, изменить название",
        callback_data=Write(nam="yes", write="", all_write="").pack()
    )

    builder.button(
        text="нет, не менять название",
        callback_data=Write(nam="not", write="", all_write="").pack()
    )

    builder.adjust(1)

    return builder.as_markup()

def price_yes_no():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="да, изменить цену",
        callback_data=WritePrice(write_price="yes").pack()
    )

    builder.button(
        text="нет, не изменять цену",
        callback_data=WritePrice(write_price="not").pack()
    )

    builder.adjust(1)

    return builder.as_markup()


def cons_yes_no():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="да, изменить расходники",
        callback_data=WritePrice2(write_price2="yes").pack()
    )

    builder.button(
        text="нет, не изменять расходники",
        callback_data=WritePrice2(write_price2="not").pack()
    )

    builder.adjust(1)

    return builder.as_markup()

def tool_yes_no():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="да, изменить сумму рем.",
        callback_data=WriteTool(write_tool="yes").pack()
    )

    builder.button(
        text="нет, не изменять сумму рем.",
        callback_data=WriteTool(write_tool="not").pack()
    )

    builder.adjust(1)

    return builder.as_markup()

def car_yes_no():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="да, изменить сумму.",
        callback_data=WriteCar(write_car="yes", write_car2="").pack()
    )

    builder.button(
        text="нет, не изменять сумму.",
        callback_data=WriteCar(write_car="not", write_car2="").pack()
    )

    builder.adjust(1)

    return builder.as_markup()

def petrol_yes_no():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="да, изменить сумму.",
        callback_data=WritePetrol(write_petrol_obj="yes", write_petrol_obj2="").pack()
    )

    builder.button(
        text="нет, не изменять сумму.",
        callback_data=WritePetrol(write_petrol_obj="yes", write_petrol_obj2="").pack()
    )

    builder.adjust(1)

    return builder.as_markup()

def salary_yes_no():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="да, изменить сумму.",
        callback_data=WriteSalary(write_salary="yes", write_salary2="").pack()
    )

    builder.button(
        text="нет, не изменять сумму.",
        callback_data=WriteSalary(write_salary="not", write_salary2="").pack()
    )

    builder.adjust(1)

    return builder.as_markup()

def yes_no_all():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="да",
        callback_data=WriteAll(write_alls="yes").pack()
    )

    builder.button(
        text="нет",
        callback_data=WriteAll(write_alls="not").pack()
    )

    builder.adjust(1)

    return builder.as_markup()
