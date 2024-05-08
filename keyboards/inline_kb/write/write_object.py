# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from utils.callbackdata import WriteObject
#

def write_obj():
    pass
#     builder = InlineKeyboardBuilder()
#
#     builder.button(
#         text="название объекта",
#         callback_data=WriteObject(write_obj="name").pack()
#     )
#
#     builder.button(
#         text="дата начала",
#         callback_data=WriteObject(write_obj="date_start").pack()
#     )
#
#     builder.button(
#         text="дата окончания",
#         callback_data=WriteObject(write_obj="date_end").pack()
#     )
#
#     builder.button(
#         text="цена",
#         callback_data=WriteObject(write_obj="price").pack()
#     )
#
#     builder.button(
#         text="расходники",
#         callback_data=WriteObject(write_obj="consumables").pack()
#     )
#
#     builder.button(
#         text="ремонт инструмента",
#         callback_data=WriteObject(write_obj="repair_tools").pack()
#     )
#
#     builder.button(
#         text="амортизация машины",
#         callback_data=WriteObject(write_obj="car").pack()
#     )
#
#     builder.button(
#         text="бензин",
#         callback_data=WriteObject(write_obj="petrol").pack()
#     )
#
#     builder.button(
#         text="зарплата",
#         callback_data=WriteObject(write_obj="salary").pack()
#     )
#
#     builder.button(
#         text="внести во все колонки",
#         callback_data=WriteObject(write_obj="all").pack()
#     )
#
#     builder.adjust(2, 3, 2, 2)
#     return builder.as_markup()
# # /