from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from data.config import config_settings
from utils.func_google import read_from_sheet, append_to_sheet
from utils.state_class import StateWriteObject


router_write_name = Router()
sheet_id = config_settings.sheet_id.get_secret_value()
@router_write_name.message(StateWriteObject.name_)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    data = await state.get_data()
    name = data.get("name")
    result = await read_from_sheet(sheet_id, 'Sheet2!A:A')
    if result is None:
        await message.answer("Ошибка чтения данных из таблицы.")
        return
    if name.lower() in [row[0].lower() for row in result]:
        await message.answer("Объект с таким именем уже существует в таблице.")
        return
    last_row = len(result) + 1
    range_ = f'объекты!A{last_row}:A{last_row}'
    values = [[name]]
    success = await append_to_sheet(sheet_id, range_, values)
    print("", success)
    if success:
        await message.answer(f'Данные: "{name}" внесены в таблицу!')
        await state.clear()
        print("OK")
    else:
        await message.answer("Ошибка при добавлении данных в таблицу.")
        await state.clear()
        print("ERROR")
