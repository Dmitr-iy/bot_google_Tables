from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from data.config import config_settings
from keyboards.inline_kb.write.price_updat import cons_update
from utils.callbackdata import WriteConsumables, WriteConsumables2
from utils.func_google import read_from_sheet, find_matching_objects, update_sheet
from utils.managers import get_goggles_consumables, responses
from utils.state_class import StateWriteConsumables


router_writer_consumables = Router()

sheet_id = config_settings.sheet_id.get_secret_value()

@router_writer_consumables.message(StateWriteConsumables.name_obj_consumables)
async def get_price(message: types.Message, state: FSMContext):
    name_obj = message.text
    await state.update_data(name_obj=name_obj)

    # объекты, содержащие введенное пользователем слово (без учета регистра)
    matching_objects = await find_matching_objects(name_obj)

    if len(matching_objects) == 0:
        await message.answer("Объект с таким названием не найден.")
    elif len(matching_objects) == 1:
        # Если найден только один объект, продолжаем с этим объектом
        await state.update_data(name_obj=matching_objects[0])
        await get_goggles_consumables(message, state, name_obj)
    else:
        # Если найдено более одного объекта, выводим все варианты пользователю
        states = StateWriteConsumables.name_obj_cons
        await responses(message, state, matching_objects, states)


@router_writer_consumables.callback_query(WriteConsumables.filter(), StateWriteConsumables.yes_no_cons)
async def write_price(callback: types.CallbackQuery, state: FSMContext, callback_data: WriteConsumables):
    callback_dat = callback_data.write_consumables
    await state.update_data(yes_no=callback_dat)
    if callback_dat == "yes":
        await callback.message.answer("как меняем сумму?", reply_markup=cons_update())
        await state.set_state(StateWriteConsumables.consumables__update)
    else:
        await state.clear()
        await callback.message.answer("сумма не изменена")

@router_writer_consumables.callback_query(WriteConsumables2.filter(), StateWriteConsumables.consumables__update)
async def write_price2(callback: types.CallbackQuery, state: FSMContext, callback_data: WriteConsumables2):
    call = callback_data.write_consumables2
    if call == "+":
        await callback.message.answer("Введи сумму которую надо прибавить к цене")
        await state.set_state(StateWriteConsumables.consumables_plus)
    elif call == "-":
        await callback.message.answer("Введи сумму которую надо отнять от цены")
        await state.set_state(StateWriteConsumables.consumables_minus)
    else:
        await callback.message.answer("Введи новую цену")
        await state.set_state(StateWriteConsumables.consumables)

@router_writer_consumables.message(StateWriteConsumables.consumables_plus)
async def get_price_plus(message: types.Message, state: FSMContext):
    cons_plus = message.text
    await state.update_data(cons_plus=cons_plus)
    data = await state.get_data()
    name_obj = data.get("name_obj")
    cons_plus = data.get("cons_plus")

    # Получение номера строки с объектом из таблицы
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)

    if row_number is not None:
        # Получение текущего значения цены
        cons_existing = await read_from_sheet(sheet_id, f'объекты!F{row_number + 1}:F{row_number + 1}')
        existing_cons = cons_existing[0][0]

        # Выполнение операции сложения
        cons_plus_result = float(existing_cons) + float(cons_plus)

        # Запись нового значения цены обратно в таблицу
        range_ = f'объекты!F{row_number + 1}:F{row_number + 1}'
        values = [[cons_plus_result]]
        success = await update_sheet(sheet_id, range_, values)

        if success:
            await message.answer(f"Сумма '{cons_plus_result}' успешно внесена для объекта '{name_obj}'.")
            await state.clear()
        else:
            await message.answer("Ошибка при обновлении данных в таблице.")
            await state.clear()
    else:
        await message.answer("Ошибка: объект не найден в таблице.")
        await state.clear()

@router_writer_consumables.message(StateWriteConsumables.consumables_minus)
async def get_price_minus(message: types.Message, state: FSMContext):
    cons_minus = message.text
    await state.update_data(cons_minus=cons_minus)
    data = await state.get_data()
    name_obj = data.get("name_obj")
    cons_minus = data.get("cons_minus")

    # Получение номера строки с объектом из таблицы
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)

    if row_number is not None:
        # Получение текущего значения цены
        cons_existing = await read_from_sheet(sheet_id, f'объекты!F{row_number + 1}:F{row_number + 1}')
        existing_cons = cons_existing[0][0]

        # Выполнение операции вычитания
        cons_minus_result = float(existing_cons) - float(cons_minus)

        # Запись нового значения цены обратно в таблицу
        range_ = f'объекты!F{row_number + 1}:F{row_number + 1}'
        values = [[cons_minus_result]]
        success = await update_sheet(sheet_id, range_, values)

        if success:
            await message.answer(f"Сумма '{cons_minus_result}' успешно внесена для объекта '{name_obj}'.")
            await state.clear()
        else:
            await message.answer("Ошибка при обновлении данных в таблице.")
            await state.clear()
    else:
        await message.answer("Ошибка: объект не найден в таблице.")
        await state.clear()

@router_writer_consumables.message(StateWriteConsumables.name_obj_cons)
async def get_dat_start(message: types.Message, state: FSMContext):
    name_obj = message.text
    await state.update_data(name_obj=name_obj)
    print(name_obj)
    await get_goggles_consumables(message, state, name_obj)

@router_writer_consumables.message(StateWriteConsumables.consumables)
async def get_price(message: types.Message, state: FSMContext):
    cons = message.text
    await state.update_data(cons=cons)
    data = await state.get_data()
    name_obj = data.get("name_obj")
    # Получение номера строки с объектом из таблицы
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)

    if row_number is not None:
        # Запись нового значения цены обратно в таблицу
        range_ = f'объекты!F{row_number + 1}:F{row_number + 1}'
        values = [[cons]]
        success = await update_sheet(sheet_id, range_, values)

        if success:
            await message.answer(f"Цена '{cons}' успешно внесена для объекта '{name_obj}'.")
            await state.clear()
        else:
            await message.answer("Ошибка при обновлении данных в таблице.")
            await state.clear()
    else:
        await message.answer("Ошибка: объект не найден в таблице.")
        await state.clear()
