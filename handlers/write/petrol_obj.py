from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from data.config import config_settings
from keyboards.inline_kb.write.price_updat import petrol_update
from utils.callbackdata import WritePetrol
from utils.func_google import read_from_sheet, find_matching_objects, update_sheet
from utils.managers import responses, get_goggles_petrol
from utils.state_class import StateWritePetrol

router_writer_petrol = Router()

sheet_id = config_settings.sheet_id.get_secret_value()


@router_writer_petrol.message(StateWritePetrol.name_obj_petrol)
async def get_petrol(message: types.Message, state: FSMContext):
    name_obj = message.text
    await state.update_data(name_obj=name_obj)

    # объекты, содержащие введенное пользователем слово (без учета регистра)
    matching_objects = await find_matching_objects(name_obj)

    if len(matching_objects) == 0:
        await message.answer("Объект с таким названием не найден.")
    elif len(matching_objects) == 1:
        # Если найден только один объект, продолжаем с этим объектом
        await state.update_data(name_obj=matching_objects[0])
        await get_goggles_petrol(message, state, name_obj)
    else:
        # Если найдено более одного объекта, выводим все варианты пользователю
        states = StateWritePetrol.name_obj_petrol_
        await responses(message, state, matching_objects, states)

@router_writer_petrol.callback_query(WritePetrol.filter(), StateWritePetrol.yes_no_petrol)
async def write_petrol(callback: types.CallbackQuery, state: FSMContext, callback_data: WritePetrol):
    callback_dat = callback_data.write_petrol_obj
    await state.update_data(yes_no=callback_dat)
    if callback_dat == "yes":
        await callback.message.answer("как меняем сумму?", reply_markup=petrol_update())
        await state.set_state(StateWritePetrol.petrol__update)
    else:
        await state.clear()
        await callback.message.answer("сумма не изменена")

@router_writer_petrol.callback_query(WritePetrol.filter(), StateWritePetrol.petrol__update)
async def writer_petrol(callback: types.CallbackQuery, state: FSMContext, callback_data: WritePetrol):
    call = callback_data.write_petrol_obj2
    if call == "+":
        await callback.message.answer("Введи сумму которую надо прибавить к сумме")
        await state.set_state(StateWritePetrol.petrol_plus)
    elif call == "-":
        await callback.message.answer("Введи сумму которую надо отнять от суммы")
        await state.set_state(StateWritePetrol.petrol_minus)
    else:
        await callback.message.answer("Введи новую сумму")
        await state.set_state(StateWritePetrol.petrol)

@router_writer_petrol.message(StateWritePetrol.petrol_plus)
async def get_plus(message: types.Message, state: FSMContext):
    plus = message.text
    await state.update_data(plus=plus)
    data = await state.get_data()
    name_obj = data.get("name_obj")
    plus = data.get("plus")
    print(plus, "plus", name_obj)

    # Получение номера строки с объектом из таблицы
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)
    print(row_number, "row_number", result)

    if row_number is not None:
        # Получение текущего значения цены
        existing = await read_from_sheet(sheet_id, f'объекты!I{row_number + 1}:I{row_number + 1}')
        print(existing, "existing")
        if existing:
            existing_ = existing[0][0]
            print('', existing_, type(existing_))
            # Выполнение операции сложения
            plus_result = float(existing_) + float(plus)

            # Запись нового значения цены обратно в таблицу
            range_ = f'объекты!I{row_number + 1}:I{row_number + 1}'
            values = [[plus_result]]
            success = await update_sheet(sheet_id, range_, values)

            if success:
                await message.answer(f"Сумма '{plus_result}' успешно внесена для объекта '{name_obj}'.")
                await state.clear()
            else:
                await message.answer("Ошибка при обновлении данных в таблице.")
                await state.clear()
        else:
            await message.answer("Ошибка: данные не найдены в таблице.")
            await state.clear()
    else:
        await message.answer("Ошибка: объект не найден в таблице.")
        await state.clear()

@router_writer_petrol.message(StateWritePetrol.petrol_minus)
async def get_minus(message: types.Message, state: FSMContext):
    minus = message.text
    await state.update_data(minus=minus)
    data = await state.get_data()
    name_obj = data.get("name_obj")
    minus = data.get("minus")
    # Получение номера строки с объектом из таблицы
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)
    if row_number is not None:
        # Получение текущего значения цены
        existing = await read_from_sheet(sheet_id, f'объекты!I{row_number + 1}:I{row_number + 1}')
        print(existing, "existing")
        if existing:
            existing_ = existing[0][0]
            print(existing_)
            # Выполнение операции вычитания
            minus_result = float(existing_) - float(minus)
            # Запись нового значения цены обратно в таблицу
            range_ = f'объекты!I{row_number + 1}:I{row_number + 1}'
            values = [[minus_result]]
            success = await update_sheet(sheet_id, range_, values)
            if success:
                await message.answer(f"Сумма '{minus_result}' успешно внесена для объекта '{name_obj}'.")
                await state.clear()
            else:
                await message.answer("Ошибка при обновлении данных в таблице.")
                await state.clear()
        else:
            await message.answer("Ошибка: данные не найдены в таблице.")
            await state.clear()
    else:
        await message.answer("Ошибка: объект не найден в таблице.")
        await state.clear()

@router_writer_petrol.message(StateWritePetrol.name_obj_petrol_)
async def get_name_obj(message: types.Message, state: FSMContext):
    name_obj = message.text
    await state.update_data(name_obj=name_obj)
    print(name_obj)
    await get_goggles_petrol(message, state, name_obj)

@router_writer_petrol.message(StateWritePetrol.petrol)
async def get_tool(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    data = await state.get_data()
    name_obj = data.get("name_obj")
    # Получение номера строки с объектом из таблицы
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)

    if row_number is not None:
        # Запись нового значения цены обратно в таблицу
        range_ = f'объекты!I{row_number + 1}:I{row_number + 1}'
        values = [[text]]
        success = await update_sheet(sheet_id, range_, values)

        if success:
            await message.answer(f"Сумма '{text}' успешно внесена для объекта '{name_obj}'.")
            await state.clear()
        else:
            await message.answer("Ошибка при обновлении данных в таблице.")
            await state.clear()
    else:
        await message.answer("Ошибка: объект не найден в таблице.")
        await state.clear()
