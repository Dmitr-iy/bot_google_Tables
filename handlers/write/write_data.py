from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.inline_kb.write_kb import write_name_ws, write_ws_data, write_yes_no
from utils.callbackdata import Write, WriteWorksheet, WriteData, WriteUpdate
from utils.fun_gspread import get_sheets_names, get_spreadsheet_id, get_ws_row, get_cell
from utils.fun_write_gs import get_cell_data, get_col1_data, write_data_col1, write_range_data, examination_cell
from utils.middleware import sheet_id_middleware
from utils.state_class import StateWriteAll, StateWriteData

router_write_data = Router()

@router_write_data.callback_query(Write.filter())
async def call_write(call: CallbackQuery, callback_data: Write):
    spreadsheet_name = callback_data.nam
    print("spreadsheet", spreadsheet_name)
    sheet_id = get_spreadsheet_id(spreadsheet_name)
    sheet_id_middleware.sheet_id = sheet_id
    sheet_id_middleware.spreadsheet_name = spreadsheet_name
    print("spreadsheet_id", sheet_id)
    await call.message.answer(f"в таблице _'{spreadsheet_name}'_ выбери лист", parse_mode="Markdown",
                              reply_markup=write_name_ws(sheet_id))
    await call.message.edit_reply_markup(reply_markup=None)

@router_write_data.callback_query(WriteWorksheet.filter())
async def call_write(call: CallbackQuery, callback_data: WriteWorksheet):
    ws = callback_data.write_ws
    sheet_id = sheet_id_middleware.sheet_id
    spreadsheet_name = sheet_id_middleware.spreadsheet_name
    sheet_id_middleware.work_sheet = ws
    print("data", sheet_id)
    if ws == "back":
        await call.message.delete()
        # await call.message.edit_reply_markup(reply_markup=None)
    else:
        # write_view_row1 = get_ws_row(ws, sheet_id)
        # print("write_view_row1", write_view_row1)
        await call.message.answer(f"в таблице _'{spreadsheet_name}'_, листе _'{ws}'_, можно записать данные:\n\n",
                                  reply_markup=write_ws_data(ws, sheet_id), parse_mode="Markdown")
        await call.message.edit_reply_markup(reply_markup=None)

@router_write_data.callback_query(WriteData.filter())
async def call_write(call: CallbackQuery, callback_data: WriteData, state: FSMContext):
    data_ = callback_data.write_data
    sheet_id = sheet_id_middleware.sheet_id
    sheet_id_middleware.data_ = data_
    work_sheet = sheet_id_middleware.work_sheet
    if data_ == "all":
        cell_1 = get_cell_data(sheet_id, work_sheet)
        await call.message.answer(f"Введи _*'{cell_1}'*_", parse_mode="Markdown")
        await state.set_state(StateWriteAll.cell_1_all)
    # await call.message.delete()
    elif data_ == "back":
        pass
    else:
        ws = work_sheet
        cell_ = get_cell(ws, sheet_id)
        if data_ in cell_:
            await call.message.answer(f"Введи _*'{data_}'*_", parse_mode="Markdown")
            await state.set_state(StateWriteData.cell_1)
        else:
            result = get_col1_data(sheet_id, work_sheet)
            print("result: ", result)
            sheet_id_middleware.cell = cell_
            columns = result[1:]
            result_text = ""
            for column in columns:
                result_text += f"*{column}*\n"
            result_text += "\n"
            await call.message.answer(f"Чтобы записать данные _'{data_}'_ сначала введи _'{cell_}'_,\n\n"
                                      f" вот что есть:\n{result_text}",
                                      parse_mode="Markdown")
            await state.set_state(StateWriteData.cell_range_name_obj)

@router_write_data.message(StateWriteData.cell_1)
async def write_data(message, state: FSMContext):
    cell_ = message.text
    await state.update_data(cell_=cell_)
    data = await state.get_data()
    cell_ = data.get("cell_")
    print('cell_: ', cell_)
    sheet_id = sheet_id_middleware.sheet_id
    print("sheet_id: ", sheet_id)
    work_sheet = sheet_id_middleware.work_sheet
    print("work_sheets: ", work_sheet)
    result = get_col1_data(sheet_id, work_sheet)
    print("result: ", result)
    if result is None:
        await message.answer(f"{message.from_user.full_name}\n\nВ этой таблице нет данных. ")
        return
    if cell_.lower() in [row.lower() for row in result]:
        await message.answer(f"{message.from_user.full_name}\n\nВ этой колонке данные с названиями _'объектов'_ данных."
                             f"Эти названия должны быть уникальными. \n\nТакое название уже существует."
                             f"Введи другое название объекта, или в меню выбери команду 'Отменить'"
                             f" для отмены действия.", parse_mode="Markdown")
        return
    else:
        last_row = len(result) + 1
        saved = write_data_col1(sheet_id, work_sheet, last_row, cell_)
        print("saved: ", saved)
        if saved:
            await message.answer(f"{message.from_user.full_name}\n\nДанные успешно записаны.")
            await state.clear()
        else:
            await message.answer(f"{message.from_user.full_name}\n\nДанные не записаны.")
            await state.clear()

@router_write_data.message(StateWriteData.cell_range_name_obj)
async def write_data(message, state: FSMContext):
    range_name_obj = message.text
    # cell_ = sheet_id_middleware.cell
    await state.update_data(range_name_obj=range_name_obj)
    sheet_id = sheet_id_middleware.sheet_id
    print("sheet_id: ", sheet_id)
    work_sheet = sheet_id_middleware.work_sheet
    result = get_col1_data(sheet_id, work_sheet)
    print("result: ", result)
    if range_name_obj.lower() in [row.lower() for row in result]:
        await state.update_data(range_name_obj=range_name_obj)
        data_ = sheet_id_middleware.data_
        examination = examination_cell(sheet_id, work_sheet, range_name_obj, data_)
        print("examination: ", examination)
        if examination:
            await message.answer(f'"_{data_}_" для "_{range_name_obj}_" уже есть: "_{examination}_".'
                                 f'\nЗаменить?', parse_mode="Markdown", reply_markup=write_yes_no())
            await state.set_state(StateWriteData.cell_update)
        else:
            await message.answer(f"{message.from_user.full_name}\n\nДля _'{range_name_obj}'_ введи {data_}.",
                                 parse_mode="Markdown")
            await state.set_state(StateWriteData.cell_range_data_cell)
    else:
        await message.answer(f"{message.from_user.full_name}\n\nНет такого {range_name_obj} в этом листе. Введи другое")
        return

@router_write_data.callback_query(WriteUpdate.filter(), StateWriteData.cell_update)
async def write_yes_n(call: CallbackQuery, callback_data: WriteUpdate, state: FSMContext):
    selected = callback_data.write_
    if selected == "yes":
        data_ = sheet_id_middleware.data_
        data = await state.get_data()
        range_name_obj = data.get("range_name_obj")
        await call.message.answer(f"{call.from_user.full_name}\n\nДля _'{range_name_obj}'_ введи {data_}.",
                                  parse_mode="Markdown")
        await state.set_state(StateWriteData.cell_range_data_cell)
    else:
        await call.message.answer("Отменено.")
        await state.clear()
        await call.message.edit_reply_markup(reply_markup=None)

@router_write_data.message(StateWriteData.cell_range_data_cell)
async def write_data(message, state: FSMContext):
    cell_data = message.text
    print('cell_data: ', cell_data)
    await state.update_data(cell_data=cell_data)
    data = await state.get_data()
    range_name_obj = data.get("range_name_obj")
    print('range_name_obj: ', range_name_obj)
    data_ = sheet_id_middleware.data_
    print('data_: ', data_)
    # cell_ = data.get("cell_")
    # print("range_name_obj: ", range_name_obj)
    sheet_id = sheet_id_middleware.sheet_id
    work_sheet = sheet_id_middleware.work_sheet
    result = write_range_data(sheet_id, work_sheet, range_name_obj, data_, cell_data)
    print("result: ", result)
    if result:
        await message.answer(f"{message.from_user.full_name}\n\nДанные успешно записаны.")
        await state.clear()
    else:
        await message.answer(f"{message.from_user.full_name}\n\nДанные не записаны.")
        await state.clear()

@router_write_data.message(StateWriteAll.cell_1_all)
async def write_all(message, state: FSMContext):
    pass

