from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from utils.callbackCreate import KbStart
from utils.state_class import StateCreate

router_start_created = Router()

@router_start_created.callback_query(KbStart.filter())
async def get_kb_start(call: types.CallbackQuery, callback_data: KbStart, state: FSMContext):
    select = callback_data.type
    if select == "create":
        await call.message.answer(f"{call.from_user.full_name}\n\nвведи название таблицы")
        await state.set_state(StateCreate.name)
    else:
        await call.message.answer(f"{call.from_user.full_name}\n\nвыбери таблицу, в которую добавить новый лист")

