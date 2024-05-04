from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from utils.callbackdata import WriteObject
from utils.state_class import StateWriteObject, StateWriteDate, StateWritePrice, StateWriteConsumables, \
    StateWriteRepairTools, StateWriteCar, StateWritePetrol, StateWriteSalary, StateWriteAll

router_write_object = Router()

@router_write_object.callback_query(WriteObject.filter())
async def call_write(call: CallbackQuery, callback_data: WriteObject, state: FSMContext):
    select = callback_data.write_obj
    print(select, "!=WriteObject")
    if select == "name":
        await call.message.answer("введи имя")
        await call.message.edit_reply_markup(reply_markup=None)
        await state.set_state(StateWriteObject.name_)
    elif select == "date_start":
        await call.message.answer("сначала введи название объекта для которого вы хотите добавить дату начала")
        await call.message.edit_reply_markup(reply_markup=None)
        await state.set_state(StateWriteDate.name_obj)
    elif select == "date_end":
        await call.message.answer("сначала введи название объекта для которого вы хотите добавить дату окончания")
        await call.message.edit_reply_markup(reply_markup=None)
        await state.set_state(StateWriteDate.name_obj_end)
    elif select == "price":
        await call.message.answer("сначала введи название объекта для которого хочешь добавить цену объекта")
        await call.message.edit_reply_markup(reply_markup=None)
        await state.set_state(StateWritePrice.name_obj_price)
    elif select == "consumables":
        await call.message.answer("сначала введи название объекта для которого хочешь добавить сумму расходников")
        await call.message.edit_reply_markup(reply_markup=None)
        await state.set_state(StateWriteConsumables.name_obj_consumables)
    elif select == "repair_tools":
        await call.message.answer("сначала введи название объекта"
                                  " для которого хочешь добавить сумму ремонта оборудования")
        await call.message.edit_reply_markup(reply_markup=None)
        await state.set_state(StateWriteRepairTools.name_obj_repair_tools)
    elif select == "car":
        await call.message.answer("сначала введи название объекта"
                                  " для которого хочешь добавить сумму амортизации машины")
        await call.message.edit_reply_markup(reply_markup=None)
        await state.set_state(StateWriteCar.name_obj_)
    elif select == "petrol":
        await call.message.answer("сначала введи название объекта"
                                  " для которого хочешь добавить сумму амортизации машины")
        await call.message.edit_reply_markup(reply_markup=None)
        await state.set_state(StateWritePetrol.name_obj_petrol)
    elif select == "salary":
        await call.message.answer(("сначала введи название объекта"
                                  " для которого хочешь добавить сумму зарплаты"))
        await call.message.edit_reply_markup(reply_markup=None)
        await state.set_state(StateWriteSalary.name_obj_salary)
    else:
        await call.message.answer("Сначала введи название объекта")
        await call.message.edit_reply_markup(reply_markup=None)
        await state.set_state(StateWriteAll.name_obj_all)
