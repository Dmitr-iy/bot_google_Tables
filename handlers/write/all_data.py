import datetime
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from data.config import config_settings
from keyboards.inline_kb.write.price_y_n import yes_no_all
from utils.callbackdata import WriteAll
from utils.func_google import read_from_sheet, append_to_sheet
from utils.managers import all_
from utils.state_class import StateWriteAll

router_write_alls = Router()

@router_write_alls.message(StateWriteAll.name_obj_all)
async def router_write_all_name(message: types.Message, state: FSMContext):
    name_obj = message.text
    await state.update_data(name_obj=name_obj)
    data = await state.get_data()
    name_obj = data.get("name_obj")
    print(name_obj)
    result = await read_from_sheet(config_settings.sheet_id.get_secret_value(), 'объекты!A:A')

    if result is None:
        await message.answer("Ошибка чтения данных из таблицы.")
        return
    if name_obj.lower() in [row[0].lower() for row in result]:
        # Если имя объекта уже существует, выведите сообщение об ошибке и завершите обработку
        await message.answer(f"{message.from_user.full_name}\n\nОбъект с таким названием уже существует в таблице. "
                             f"Введи другое название объекта, или в меню выбери команду 'Отменить'"
                             f" для отмены действия.")
        return
    else:
        await message.answer(f"{message.from_user.full_name} Введи дату начала объекта, в формате дд.мм.гг.\n\n"
                             "Если хочешь оставить поле пустым, введи 0. ")
        await state.set_state(StateWriteAll.date_obj)

@router_write_alls.message(StateWriteAll.date_obj)
async def router_write_all_date(message: types.Message, state: FSMContext):
    date = message.text.strip()
    date = (date.replace(",", ".").replace("/", ".").replace(":", ".").
            replace(";", ".").replace(" ", "."))
    try:
        datetime.datetime.strptime(date, "%d.%m.%y")
    except ValueError:
        if date != "0":
            await all_(message)
            return
    if date == "0":
        date = ""
    await state.update_data(date_obj=date)
    print(date, "end")
    await message.answer(f"{message.from_user.full_name}\n\nВведи дату окончания объекта, в формате дд.мм.гг.\n\n"
                         " Если хочешь оставить поле пустым, введи 0.")
    await state.set_state(StateWriteAll.date_obj_end)

@router_write_alls.message(StateWriteAll.date_obj_end)
async def router_write_all_date_end(message: types.Message, state: FSMContext):
    date = message.text.strip()
    data = await state.get_data()
    date_obj = data.get("date_obj")
    print(date_obj)
    date = (date.replace(",", ".").replace("/", ".").replace(":", ".").
            replace(";", ".").replace(" ", "."))
    try:
        datetime.datetime.strptime(date, "%d.%m.%y")
    except ValueError:
        if date != "0":
            await all_(message)
            return
    date_obj_end = date
    print(date_obj_end)
    await state.update_data(date_obj_end=date_obj_end)
    if date_obj_end == "0":
        date_obj_end = ""
    date_obj_datetime = datetime.datetime.strptime(date_obj, "%d.%m.%y") if date_obj else None
    date_obj_end_datetime = datetime.datetime.strptime(date_obj_end, "%d.%m.%y") if date_obj_end else None
    if date_obj_datetime is not None and date_obj_end_datetime is not None:
        if date_obj_datetime > date_obj_end_datetime != "":
            await message.answer(f"{message.from_user.full_name}\n\n"
                                 f"Некорректное значение. Дата начала не может быть позже даты окончания.")
            return
    await state.update_data(date_obj_end=date_obj_end)
    await message.answer(f"{message.from_user.full_name}\n\n"
                         f"Введи цену объекта. Если хочешь оставить поле пустым, введи 0.")
    await state.set_state(StateWriteAll.price_all)

@router_write_alls.message(StateWriteAll.price_all)
async def router_write_all_price(message: types.Message, state: FSMContext):
    all_data = message.text.strip()
    if all_data == "0":
        all_data = ""
    else:
        if "," in all_data:
            all_data = all_data.replace(",", ".")
        try:
            all_data = float(all_data)
        except ValueError:
            await all_(message)
            return
    await state.update_data(price_all=all_data)
    await message.answer(f"{message.from_user.full_name}\n\nвведи накладные расходы объекта.\n\n"
                         "Пример: 0.06; 0.3\n\n Если хочешь оставить поле пустым, введи 0.")
    await state.set_state(StateWriteAll.tax_all)

@router_write_alls.message(StateWriteAll.tax_all)
async def router_write_all_tax(message: types.Message, state: FSMContext):
    all_data = message.text.strip()
    if all_data == "0":
        all_data = ""
    else:
        if "," in all_data:
            all_data = all_data.replace(",", ".")
        try:
            all_data = float(all_data)
        except ValueError:
            await all_(message)
            return
    await state.update_data(tax_all=all_data)
    await message.answer(f"{message.from_user.full_name}\n\n"
                         f"Введи общую стоимость расходников.\n\nЕсли хочешь оставить поле пустым, введи 0.")
    await state.set_state(StateWriteAll.consumables_all)

@router_write_alls.message(StateWriteAll.consumables_all)
async def router_write_all_consumables(message: types.Message, state: FSMContext):
    all_data = message.text.strip()
    if all_data == "0":
        all_data = ""
    else:
        if "," in all_data:
            all_data = all_data.replace(",", ".")
        try:
            all_data = float(all_data)
        except ValueError:
            await all_(message)
            return
    await state.update_data(consumables_all=all_data)
    await message.answer(f"{message.from_user.full_name}\n\n"
                         f"Введи общую стоимость ремонта оборудования.\n\nЕсли хочешь оставить поле пустым, введи 0.")
    await state.set_state(StateWriteAll.repair_tools_all)

@router_write_alls.message(StateWriteAll.repair_tools_all)
async def router_write_all_repair_tools(message: types.Message, state: FSMContext):
    all_data = message.text.strip()
    if all_data == "0":
        all_data = ""
    else:
        if "," in all_data:
            all_data = all_data.replace(",", ".")
        try:
            all_data = float(all_data)
        except ValueError:
            await all_(message)
            return
    await state.update_data(repair_tools_all=all_data)
    await message.answer(f"{message.from_user.full_name}\n\n"
                         f"Введи общую стоимость амортизации машин.\n\nЕсли хочешь оставить поле пустым, введи 0.")
    await state.set_state(StateWriteAll.car_all)

@router_write_alls.message(StateWriteAll.car_all)
async def router_write_all_car(message: types.Message, state: FSMContext):
    all_data = message.text.strip()
    if all_data == "0":
        all_data = ""
    else:
        if "," in all_data:
            all_data = all_data.replace(",", ".")
        try:
            all_data = float(all_data)
        except ValueError:
            await all_(message)
            return
    await state.update_data(car_all=all_data)
    await message.answer(f"{message.from_user.full_name}\n\n"
                         f"Введи общую стоимость затрат на бензин.\n\nЕсли хочешь оставить поле пустым, введи 0.")
    await state.set_state(StateWriteAll.petrol_all)

@router_write_alls.message(StateWriteAll.petrol_all)
async def router_write_all_petrol(message: types.Message, state: FSMContext):
    all_data = message.text.strip()
    if all_data == "0":
        all_data = ""
    else:
        if "," in all_data:
            all_data = all_data.replace(",", ".")
        try:
            all_data = float(all_data)
        except ValueError:
            await all_(message)
            return
    await state.update_data(petrol_all=all_data)
    await message.answer(f"{message.from_user.full_name}\n\n"
                         f"Введи общую стоимость затрат на зарплату.\n\nЕсли хочешь оставить поле пустым, введи 0.")
    await state.set_state(StateWriteAll.salary_all)

@router_write_alls.message(StateWriteAll.salary_all)
async def router_write_all_salary(message: types.Message, state: FSMContext):
    all_data = message.text.strip()
    if all_data == "0":
        all_data = ""
    else:
        if "," in all_data:
            all_data = all_data.replace(",", ".")
        try:
            all_data = float(all_data)
        except ValueError:
            await all_(message)
            return
    await state.update_data(salary_all=all_data)
    data = await state.get_data()
    data_name = data.get("name_obj")
    date_start = data.get("date_obj")
    date_end = data.get("date_obj_end")
    price_all = data.get("price_all")
    tax_all = data.get("tax_all")
    consumables_all = data.get("consumables_all")
    repair_tools_all = data.get("repair_tools_all")
    car_all = data.get("car_all")
    petrol_all = data.get("petrol_all")
    salary_all = data.get("salary_all")
    alls_all = [
        data_name, date_start, date_end, price_all, tax_all,
        consumables_all, repair_tools_all, car_all, petrol_all, salary_all
    ]
    await state.update_data(alls_all=alls_all)
    await message.answer(f"название объекта: {data_name}\n\n"
                         f"дата начала и окончания: {date_start} - {date_end}\n\n"
                         f"сумма объекта: {price_all}\n\nсумма налога: {tax_all}\n\n"
                         f"сумма расходников: {consumables_all}\n\n"
                         f"сумма ремонта: {repair_tools_all}\n\nамортизация авто: {car_all}\n\n "
                         f"расход топлива: {petrol_all}\n\nзарплата: {salary_all}\n\n"
                         f"Вносим эти данные в таблицу?", reply_markup=yes_no_all())
    await state.set_state(StateWriteAll.y_n_all)

@router_write_alls.callback_query(WriteAll.filter(), StateWriteAll.y_n_all)
async def router_write_all_y_n(callback: types.CallbackQuery, state: FSMContext, callback_data: WriteAll):
    callbacks = callback_data.write_alls
    if callbacks == "yes":
        data = await state.get_data()
        alls = data.get("alls_all")
        print("", alls)
        result = await read_from_sheet(config_settings.sheet_id.get_secret_value(), 'объекты!A:J')
        if result is None:
            await callback.message.answer("Ошибка чтения данных из таблицы.")
            return
        last_row = len(result) + 1
        range_ = f'объекты!A{last_row}:J{last_row}'
        values = [alls]
        success = await append_to_sheet(config_settings.sheet_id.get_secret_value(), range_, values)
        if success:
            await callback.message.answer(f'{callback.from_user.full_name}\n\nДанные: "{alls}" внесены в таблицу!')
            await state.clear()
        else:
            await callback.message.answer("Ошибка при добавлении данных в таблицу.")
            return
    else:
        await callback.message.answer("Отменено.")
        await state.clear()
