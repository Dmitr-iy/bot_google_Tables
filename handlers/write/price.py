from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from data.config import config_settings
from keyboards.inline_kb.write.price_updat import price_update
from utils.callbackdata import WritePrice, WritePrice2
from utils.func_google import read_from_sheet, find_matching_objects, update_sheet
from utils.managers import get_goggles_price, responses
from utils.state_class import StateWritePrice

router_writer_price = Router()
sheet_id = config_settings.sheet_id.get_secret_value()

@router_writer_price.message(StateWritePrice.name_obj_price)
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
        await get_goggles_price(message, state, name_obj)
    else:
        # Если найдено более одного объекта, выводим все варианты пользователю
        states = StateWritePrice.obj_price
        await responses(message, state, matching_objects, states)

@router_writer_price.callback_query(WritePrice.filter(), StateWritePrice.yes_no)
async def write_price(callback: types.CallbackQuery, state: FSMContext, callback_data: WritePrice):
    callback_dat = callback_data.write_price
    await state.update_data(yes_no=callback_dat)
    if callback_dat == "yes":
        await callback.message.answer("как меняем цену?", reply_markup=price_update())
        await state.set_state(StateWritePrice.price__update)
    else:
        await state.clear()
        await callback.message.answer("цена не изменена")

@router_writer_price.callback_query(WritePrice2.filter(), StateWritePrice.price__update)
async def write_price2(callback: types.CallbackQuery, state: FSMContext, callback_data: WritePrice2):
    call = callback_data.write_price2
    if call == "+":
        await callback.message.answer("Введи сумму которую надо прибавить к цене")
        await state.set_state(StateWritePrice.price_plus)
    elif call == "-":
        await callback.message.answer("Введи сумму которую надо отнять от цены")
        await state.set_state(StateWritePrice.price_minus)
    else:
        await callback.message.answer("Введи новую цену")
        await state.set_state(StateWritePrice.price)

@router_writer_price.message(StateWritePrice.price_plus)
async def get_price_plus(message: types.Message, state: FSMContext):
    prices_plus = message.text
    await state.update_data(price_plus=prices_plus)
    data = await state.get_data()
    name_obj = data.get("name_obj")
    price_plus = data.get("price_plus")

    # Получение номера строки с объектом из таблицы
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)

    if row_number is not None:
        # Получение текущего значения цены
        price_existing = await read_from_sheet(sheet_id, f'объекты!D{row_number + 1}:D{row_number + 1}')
        existing_price = price_existing[0][0]

        # Выполнение операции сложения
        price_plus_result = float(existing_price) + float(price_plus)

        # Запись нового значения цены обратно в таблицу
        range_ = f'объекты!D{row_number + 1}:D{row_number + 1}'
        values = [[price_plus_result]]
        success = await update_sheet(sheet_id, range_, values)

        if success:
            await message.answer(f"Цена '{price_plus_result}' успешно внесена для объекта '{name_obj}'.")
            await state.clear()
        else:
            await message.answer("Ошибка при обновлении данных в таблице.")
            await state.clear()
    else:
        await message.answer("Ошибка: объект не найден в таблице.")
        await state.clear()

@router_writer_price.message(StateWritePrice.price_minus)
async def get_price_minus(message: types.Message, state: FSMContext):
    prices_minus = message.text
    await state.update_data(price_minus=prices_minus)
    data = await state.get_data()
    name_obj = data.get("name_obj")
    price_minus = data.get("price_minus")

    # Получение номера строки с объектом из таблицы
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)

    if row_number is not None:
        # Получение текущего значения цены
        price_existing = await read_from_sheet(sheet_id, f'объекты!D{row_number + 1}:D{row_number + 1}')
        existing_price = price_existing[0][0]

        # Выполнение операции вычитания
        price_minus_result = float(existing_price) - float(price_minus)

        # Запись нового значения цены обратно в таблицу
        range_ = f'объекты!D{row_number + 1}:D{row_number + 1}'
        values = [[price_minus_result]]
        success = await update_sheet(sheet_id, range_, values)

        if success:
            await message.answer(f"Цена '{price_minus_result}' успешно внесена для объекта '{name_obj}'.")
            await state.clear()
        else:
            await message.answer("Ошибка при обновлении данных в таблице.")
            await state.clear()
    else:
        await message.answer("Ошибка: объект не найден в таблице.")
        await state.clear()

@router_writer_price.message(StateWritePrice.obj_price)
async def get_all_price(message: types.Message, state: FSMContext):
    name_obj = message.text
    await state.update_data(name_obj=name_obj)
    print(name_obj)

    await get_goggles_price(message, state, name_obj)

@router_writer_price.message(StateWritePrice.price)
async def get_price(message: types.Message, state: FSMContext):
    price = message.text
    await state.update_data(price=price)
    data = await state.get_data()
    name_obj = data.get("name_obj")

    # Получение номера строки с объектом из таблицы
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)

    if row_number is not None:
        # Запись нового значения цены обратно в таблицу
        range_ = f'объекты!D{row_number + 1}:D{row_number + 1}'
        values = [[price]]
        success = await update_sheet(sheet_id, range_, values)

        if success:
            await message.answer(f"Цена '{price}' успешно внесена для объекта '{name_obj}'.")
            await state.clear()
        else:
            await message.answer("Ошибка при обновлении данных в таблице.")
            await state.clear()
    else:
        await message.answer("Ошибка: объект не найден в таблице.")
        await state.clear()
