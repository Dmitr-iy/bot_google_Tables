from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from utils.callbackdata import Write
from utils.func_google import read_from_sheet, sheet
from utils.state_class import StateWriteObject
from keyboards.inline_kb.write.write_object import write_obj


router_write_data = Router()

@router_write_data.callback_query(Write.filter())
async def call_write(call: CallbackQuery, callback_data: Write):
    select = callback_data.write

    if select == "object":
        await call.message.answer("в какую колонку добавить данные?", reply_markup=write_obj())
        await call.message.edit_reply_markup(reply_markup=None)
    elif select == "workers":
        await call.message.answer("")
    elif select == "buy":
        await call.message.answer(" ")
    elif select == "consumables":
        await call.message.answer(" ")
    elif select == "tools":
        await call.message.answer(" ")
    elif select == "budget":
        await call.message.answer("")
