import asyncio

from aiogram import types
from aiogram.fsm.context import FSMContext
from data.config import config_settings
from keyboards.inline_kb.write.price_y_n import price_yes_no, cons_yes_no, tool_yes_no, car_yes_no, petrol_yes_no, \
    salary_yes_no
from utils.fun_gspread import get_all_sheet
from utils.func_google import read_from_sheet, find_matching_objects
from utils.middleware import sheet_id_middleware
from utils.state_class import StateWritePrice, StateWriteConsumables, StateWriteRepairTools, StateWriteCar, \
    StateWritePetrol, StateWriteSalary


# async def google_manager(message: types.Message, state: FSMContext, name_obj: str, states: str, google: dict):
#     # объекты, содержащие введенное пользователем слово (без учета регистра)
#     matching_objects = await find_matching_objects(name_obj)
#
#     if len(matching_objects) == 0:
#         await message.answer("Объект с таким названием не найден.")
#     elif len(matching_objects) == 1:
#         # Если найден только один объект, продолжаем с этим объектом
#         await state.update_data(name_obj=matching_objects[0])
#
#     else:
#         # Если найдено более одного объекта, выводим все варианты пользователю
#         response = "Найдены следующие объекты, содержащие это слово:\n"
#         response += "\n".join(matching_objects)
#         response += "\nПожалуйста, выбери нужный объект."
#         await state.set_state(states)
#         await message.answer(response)


async def get_goggles_price(message: types.Message, state: FSMContext, name_obj: str):
    sheet_id = config_settings.sheet_id.get_secret_value()
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    if result is None:
        await message.answer("Ошибка чтения данных из таблицы.")
        return
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)
    if row_number is None:
        await message.answer(f"Объект '{name_obj}' не найден в таблице. Проверь правильность ввода и повтори")
        return
    price_existing = await read_from_sheet(sheet_id, f'объекты!D{row_number + 1}:D{row_number + 1}')
    if price_existing:
        existing_price = price_existing[0][0]
        await message.answer(f"У объекта '{name_obj}' уже есть цена: '{existing_price}'.\n"
                             f"надо изменить цену?", reply_markup=price_yes_no())
        await state.set_state(StateWritePrice.yes_no)
    else:
        await message.answer("Введи цену.")
        await state.set_state(StateWritePrice.price)


async def get_goggles_consumables(message: types.Message, state: FSMContext, name_obj: str):
    sheet_id = config_settings.sheet_id.get_secret_value()
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    if result is None:
        await message.answer("Ошибка чтения данных из таблицы.")
        return
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)
    if row_number is None:
        await message.answer(f"Объект '{name_obj}' не найден в таблице. Проверь правильность ввода и повтори")
        return
    cons_existing = await read_from_sheet(sheet_id, f'объекты!F{row_number + 1}:F{row_number + 1}')
    if cons_existing:
        existing_cons = cons_existing[0][0]
        await message.answer(f"У объекта '{name_obj}' уже есть данные о сумме расходников: '{existing_cons}'.\n"
                             f"надо изменить сумму?", reply_markup=cons_yes_no())
        await state.set_state(StateWriteConsumables.yes_no_cons)
    else:
        await message.answer("Введи сумму.")
        await state.set_state(StateWriteConsumables.consumables)

async def get_goggles_repair_tools(message: types.Message, state: FSMContext, name_obj: str):
    sheet_id = config_settings.sheet_id.get_secret_value()
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    if result is None:
        await message.answer("Ошибка чтения данных из таблицы.")
        return
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)
    if row_number is None:
        await message.answer(f"Объект '{name_obj}' не найден в таблице. Проверь правильность ввода и повтори")
        return
    tool_existing = await read_from_sheet(sheet_id, f'объекты!G{row_number + 1}:G{row_number + 1}')
    if tool_existing:
        existing_tool = tool_existing[0][0]
        print(existing_tool)
        await message.answer(f"У объекта '{name_obj}' уже есть данные о сумме ремонта оборудования: '{existing_tool}'."
                             f"надо изменить сумму?", reply_markup=tool_yes_no())
        await state.set_state(StateWriteRepairTools.yes_no_repair_tools)
    else:
        await message.answer("Введи сумму.")
        await state.set_state(StateWriteRepairTools.repair_tools)

async def get_goggles_car(message: types.Message, state: FSMContext, name_obj: str):
    sheet_id = config_settings.sheet_id.get_secret_value()
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    if result is None:
        await message.answer("Ошибка чтения данных из таблицы.")
        return
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)
    if row_number is None:
        await message.answer(f"Объект '{name_obj}' не найден в таблице. Проверь правильность ввода и повтори")
        return
    existing = await read_from_sheet(sheet_id, f'объекты!H{row_number + 1}:H{row_number + 1}')
    if existing:
        existing_ = existing[0][0]
        print(existing_)
        await message.answer(f"У объекта '{name_obj}' уже есть данные о сумме амортизации машины: '{existing_}'."
                             f"надо изменить сумму?", reply_markup=car_yes_no())
        await state.set_state(StateWriteCar.yes_no_car)
    else:
        await message.answer("Введи сумму.")
        await state.set_state(StateWriteCar.car)

async def get_goggles_petrol(message: types.Message, state: FSMContext, name_obj: str):
    sheet_id = config_settings.sheet_id.get_secret_value()
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    if result is None:
        await message.answer("Ошибка чтения данных из таблицы.")
        return
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)
    if row_number is None:
        await message.answer(f"Объект '{name_obj}' не найден в таблице. Проверь правильность ввода и повтори")
        return
    existing = await read_from_sheet(sheet_id, f'объекты!I{row_number + 1}:I{row_number + 1}')
    if existing:
        existing_ = existing[0][0]
        print(existing_)
        await message.answer(f"У объекта '{name_obj}' уже есть данные о сумме амортизации машины: '{existing_}'."
                             f"надо изменить сумму?", reply_markup=petrol_yes_no())
        await state.set_state(StateWritePetrol.yes_no_petrol)
    else:
        await message.answer("Введи сумму.")
        await state.set_state(StateWritePetrol.petrol)

async def get_goggles_salary(message: types.Message, state: FSMContext, name_obj: str):
    sheet_id = config_settings.sheet_id.get_secret_value()
    result = await read_from_sheet(sheet_id, 'объекты!A:A')
    if result is None:
        await message.answer("Ошибка чтения данных из таблицы.")
        return
    row_number = next((i for i, sublist in enumerate(result) if name_obj.lower() in str(sublist).lower()), None)
    if row_number is None:
        await message.answer(f"Объект '{name_obj}' не найден в таблице. Проверь правильность ввода и повтори")
        return
    existing = await read_from_sheet(sheet_id, f'объекты!J{row_number + 1}:J{row_number + 1}')
    if existing:
        existing_ = existing[0][0]
        print(existing_)
        await message.answer(f"У объекта '{name_obj}' уже есть данные о сумме амортизации машины: '{existing_}'."
                             f"надо изменить сумму?", reply_markup=salary_yes_no())
        await state.set_state(StateWriteSalary.yes_no_salary)
    else:
        await message.answer("Введи сумму.")
        await state.set_state(StateWriteSalary.salary)

async def responses(message: types.Message, state: FSMContext, matching_objects, states):
    response = "Найдены следующие объекты, содержащие это слово:\n"
    response += "\n".join(matching_objects)
    response += "\nПожалуйста, выбери нужный объект."
    await message.answer(response)
    await state.set_state(states)

async def all_(message: types.Message):
    await message.answer(f"{message.from_user.full_name} Некорректное значение."
                         f" Введите числовое значение без символов. \n\n"
                         "Если хочешь оставить поле пустым, введи 0.")

#view
async def view_all_list(call: types.CallbackQuery):
    work_sheet = sheet_id_middleware.work_sheet
    sheet_id = sheet_id_middleware.sheet_id
    work_sheet_all_data = get_all_sheet(sheet_id, work_sheet)
    if work_sheet_all_data:
        columns = work_sheet_all_data[0]
        result_text = ""
        for row in work_sheet_all_data[1:]:
            for column, value in zip(columns, row):
                result_text += f"*{column.lower()}*: {value}\n\n"
            result_text += "\n\n"
        if len(result_text) <= 4096:
            await call.message.answer(result_text, parse_mode="Markdown")
        else:
            paragraphs = result_text.split('\n\n')
            chunk_size = 2000
            chunks = []
            chunk = ""
            for paragraph in paragraphs:
                if len(chunk) + len(paragraph) <= chunk_size:
                    chunk += paragraph + "\n\n"
                else:
                    chunks.append(chunk)
                    chunk = paragraph + "\n\n"
            if chunk:
                chunks.append(chunk)

            print(chunks)
            for chunk in chunks:
                await call.message.answer(chunk, parse_mode="Markdown")
                await asyncio.sleep(5)
    else:
        await call.message.answer("в таблице нет данных")

async def get_cells(call: types.CallbackQuery, data):
    if data:
        columns = data[0]
        result_text = ""
        for row in data[1:]:
            for column, value in zip(columns, row):
                result_text += f"*{column.lower()}*: {value}\n"
            result_text += "\n"
        await call.message.answer(result_text, parse_mode="Markdown")
    else:
        await call.message.answer("в таблице нет данных")
