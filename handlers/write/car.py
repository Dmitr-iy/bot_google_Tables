from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from data.config import config_settings
from keyboards.inline_kb.write.price_updat import car_update
from utils.callbackdata import WriteCar
from utils.func_google import read_from_sheet, find_matching_objects, update_sheet
from utils.managers import responses, get_goggles_car
from utils.state_class import StateWriteCar

router_writer_car = Router()

sheet_id = config_settings.sheet_id.get_secret_value()


@router_writer_car.message(StateWriteCar.name_obj_)
async def get_tool(message: types.Message, state: FSMContext):
    name_obj = message.text
    await state.update_data(name_obj=name_obj)

    # объекты, содержащие введенное пользователем слово (без учета регистра)
    matching_objects = await find_matching_objects(name_obj)

    if len(matching_objects) == 0:
        await message.answer("Объект с таким названием не найден.")
    elif len(matching_objects) == 1:
        # Если найден только один объект, продолжаем с этим объектом
        await state.update_data(name_obj=matching_objects[0])
        await get_goggles_car(message, state, name_obj)
    else:
        # Если найдено более одного объекта, выводим все варианты пользователю
        states = StateWriteCar.name_obj_car
        await responses(message, state, matching_objects, states)

@router_writer_car.callback_query(WriteCar.filter(), StateWriteCar.yes_no_car)
async def write_tool(callback: types.CallbackQuery, state: FSMContext, callback_data: WriteCar):
    callback_dat = callback_data.write_car
    await state.update_data(yes_no=callback_dat)
    if callback_dat == "yes":
        await callback.message.answer("как меняем сумму?", reply_markup=car_update())
        await state.set_state(StateWriteCar.car__update)
    else:
        await state.clear()
        await callback.message.answer("сумма не изменена")

@router_writer_car.callback_query(WriteCar.filter(), StateWriteCar.car__update)
async def write_tools(callback: types.CallbackQuery, state: FSMContext, callback_data: WriteCar):
    call = callback_data.write_car2
    if call == "+":
        await callback.message.answer("Введи сумму которую надо прибавить к сумме")
        await state.set_state(StateWriteCar.car_plus)
    elif call == "-":
        await callback.message.answer("Введи сумму которую надо отнять от суммы")
        await state.set_state(StateWriteCar.car_minus)
    else:
        await callback.message.answer("Введи новую сумму")
        await state.set_state(StateWriteCar.car)

@router_writer_car.message(StateWriteCar.car_plus)
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
        existing = await read_from_sheet(sheet_id, f'объекты!H{row_number + 1}:H{row_number + 1}')
        print(existing, "existing")
        if existing:
            existing_ = existing[0][0]
            print('', existing_, type(existing_))
            # Выполнение операции сложения
            plus_result = float(existing_) + float(plus)

            # Запись нового значения цены обратно в таблицу
            range_ = f'объекты!H{row_number + 1}:H{row_number + 1}'
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

@router_writer_car.message(StateWriteCar.car_minus)
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
        existing = await read_from_sheet(sheet_id, f'объекты!H{row_number + 1}:H{row_number + 1}')
        print(existing, "existing")
        if existing:
            existing_ = existing[0][0]
            print(existing_)
            # Выполнение операции вычитания
            minus_result = float(existing_) - float(minus)
            # Запись нового значения цены обратно в таблицу
            range_ = f'объекты!H{row_number + 1}:H{row_number + 1}'
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

@router_writer_car.message(StateWriteCar.name_obj_car)
async def get_name_obj(message: types.Message, state: FSMContext):
    name_obj = message.text
    await state.update_data(name_obj=name_obj)
    print(name_obj)
    await get_goggles_car(message, state, name_obj)

@router_writer_car.message(StateWriteCar.car)
async def get_tool(message: types.Message, state: FSMContext):
    tool = message.text
    await state.update_data(tool=tool)
    data = await state.get_data()
    name_obj = data.get("name_obj")
    # Получение номера строки с объектом из таблицы
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)

    if row_number is not None:
        # Запись нового значения цены обратно в таблицу
        range_ = f'объекты!H{row_number + 1}:H{row_number + 1}'
        values = [[tool]]
        success = await update_sheet(sheet_id, range_, values)

        if success:
            await message.answer(f"Сумма '{tool}' успешно внесена для объекта '{name_obj}'.")
            await state.clear()
        else:
            await message.answer("Ошибка при обновлении данных в таблице.")
            await state.clear()
    else:
        await message.answer("Ошибка: объект не найден в таблице.")
        await state.clear()
