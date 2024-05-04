from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from data.config import config_settings
from utils.func_google import read_from_sheet, append_to_sheet, find_matching_objects
from utils.managers import responses
from utils.state_class import StateWriteDate


router_writer_date_start = Router()
sheet_id = config_settings.sheet_id.get_secret_value()

@router_writer_date_start.message(StateWriteDate.name_obj)
async def get_date_start(message: types.Message, state: FSMContext):
    name_obj = message.text
    await state.update_data(name_obj=name_obj)

    # Найдем объекты, содержащие введенное пользователем слово (без учета регистра)
    matching_objects = await find_matching_objects(name_obj)

    if len(matching_objects) == 0:
        await message.answer("Объект с таким названием не найден.")
    elif len(matching_objects) == 1:
        # Если найден только один объект, продолжаем с этим объектом
        await state.update_data(name_obj=matching_objects[0])

        result = await read_from_sheet(sheet_id, 'объекты!A:A')

        if result is None:
            # Если чтение не удалось, выведите сообщение об ошибке и завершите обработку
            await message.answer("Ошибка чтения данных из таблицы.")
            return

        row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)
        date_start_existing = await read_from_sheet(sheet_id, f'объекты!B{row_number + 1}:B{row_number + 1}')
        if date_start_existing:
            existing_date_start = date_start_existing[0][0]
            await message.answer(f"У объекта '{name_obj}' уже есть дата начала: '{existing_date_start}'.")
            await state.clear()
        else:
            await message.answer("Введите дату начала.")
            await state.set_state(StateWriteDate.date_start)
    else:
        # Если найдено более одного объекта, выводим все варианты пользователю
        states = StateWriteDate.obj
        await responses(message, state, matching_objects, states)

@router_writer_date_start.message(StateWriteDate.obj)
async def get_dat_start(message: types.Message, state: FSMContext):
    name_obj = message.text
    await state.update_data(name_obj=name_obj)
    print(name_obj)

    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    print(result)

    if result is None:
        await message.answer("Ошибка при чтении данных из таблицы.")
        await state.clear()
        return

    row_number = next((i for i, sublist in enumerate(result) if name_obj in str(sublist)))

    if row_number is not None:
        date_start_existing = await read_from_sheet(sheet_id, f'объекты!B{row_number + 1}:B{row_number + 1}')
        if date_start_existing:
            existing_date_start = date_start_existing[0][0]
            await message.answer(f"У объекта '{name_obj}' уже есть дата начала: '{existing_date_start}'.")
            await state.clear()
        else:
            await message.answer("Введите дату начала.")
            await state.set_state(StateWriteDate.date_start)
    else:
        await message.answer("Объект с таким названием не найден.")
        await state.clear()

@router_writer_date_start.message(StateWriteDate.date_start)
async def get_start(message: types.Message, state: FSMContext):
    date_start = message.text
    await state.update_data(date_start=date_start)
    data = await state.get_data()
    name_obj = data.get("name_obj")
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    if result is None:
        # Если чтение не удалось, выведите сообщение об ошибке и завершите обработку
        await message.answer("Ошибка чтения данных из таблицы.")
        return

    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)

    if row_number is not None:
        range_ = f'объекты!B{row_number + 1}:B{row_number + 1}'
        values = [[date_start]]
        success = await append_to_sheet(sheet_id, range_, values)
        if success:
            await message.answer(f"Дата начала '{date_start}' успешно внесена для объекта '{name_obj}'.")
            await state.clear()
        else:
            await message.answer("Ошибка при добавлении данных в таблицу.")
            await state.clear()
    else:
        await message.answer(f"Объект '{name_obj}' не найден в таблице.")
        await state.clear()
