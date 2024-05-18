from aiogram import Router, types, flags
from aiogram.fsm.context import FSMContext
from keyboards.inline_kb.kb_new_file import create_file_y_n, select_table, kb_start
from utils.callbackdata import KbNewFile, KbNewFil, KbNewFiles
from utils.fun_gspread import create_spreadsheet, examination_name, create_worksheet, get_spreadsheet_id, \
    get_worksheet_list
from utils.middleware import sheet_id_middleware
from utils.state_class import StateCreate, StateWriteNew


router_new_table = Router()

@router_new_table.callback_query(KbNewFile.filter())
async def get_kb_start(call: types.CallbackQuery, callback_data: KbNewFile, state: FSMContext):
    select = callback_data.select_table
    sheet_id_middleware.select = select
    if select == "create":
        await call.message.answer(f"{call.from_user.full_name}\n\nвведи название таблицы")
        await state.set_state(StateCreate.name)
    else:
        if select == 'create_sheet':
            await call.message.answer(f"{call.from_user.full_name}\n\nвыбери таблицу, в которую добавить новый лист",
                                      reply_markup=select_table())
    await call.message.edit_reply_markup(reply_markup=None)

@router_new_table.callback_query(KbNewFil.filter())
async def get_kb_new_file(call: types.CallbackQuery, callback_data: KbNewFil, state: FSMContext):
    select_ = callback_data.select_tabl
    sheet_id_middleware.select_ = select_
    if select_ == "back":
        await call.answer("создать: ", reply_markup=kb_start())
        await call.message.edit_reply_markup(reply_markup=None)
        return
    else:
        await call.message.answer(f"{call.from_user.full_name}\n\nвведи название листа")
        await state.set_state(StateCreate.name_worksheets)
    await call.message.edit_reply_markup(reply_markup=None)

@router_new_table.message(StateCreate.name)
async def new_table(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    file_ex = await examination_name(name)
    if file_ex is not None:
        await message.answer(f"Таблица {name} уже существует.")
        return
    else:
        await message.answer(f"В таблицу {name} автоматически будет добавлен новый лист, как его назвать?")
        await state.set_state(StateCreate.name_worksheets)

@router_new_table.message(StateCreate.name_worksheets)
async def name_worksheet(message: types.Message, state: FSMContext):
    name_ws = message.text
    await state.update_data(name_ws=name_ws)
    sheet_id_middleware.work_sheet = name_ws
    select = sheet_id_middleware.select
    data = await state.get_data()
    name = data.get("name")
    name_worksheets = data.get("name_ws")
    if select == 'create':
        await message.answer(f"В таблицу {name} добавлен лист {name_worksheets}!\n\n"
                             f"какое кол-во строк в листе: {name_worksheets}")
    else:
        table = sheet_id_middleware.select_
        result = get_worksheet_list(name=table)
        if result:
            if name_worksheets in result:
                await message.answer(f"Таблица {table} уже содержит лист {name_worksheets}\n\nвведи другое название")
                return
            else:
                await message.answer(f"В таблицу {table} добавлен лист {name_worksheets}\n\n"
                                     f"какое кол-во строк в листе: {name_worksheets}")
    await state.set_state(StateCreate.sum_rows)

@router_new_table.message(StateCreate.sum_rows)
async def num_rows(message: types.Message, state: FSMContext):
    sum_rows = message.text
    await state.update_data(sum_rows=sum_rows)
    data = await state.get_data()
    name_worksheets = data.get("name_ws")
    await message.answer(f"какое кол-во столбцов в листе: {name_worksheets}")
    await state.set_state(StateCreate.sum_cols)

@flags.flag('long_operation')
@router_new_table.message(StateCreate.sum_cols)
async def num_cols(message: types.Message, state: FSMContext):
    sum_cols = message.text
    await state.update_data(sum_cols=sum_cols)
    data = await state.get_data()
    name = data.get("name")
    name_worksheets = data.get("name_ws")
    sum_rows = data.get("sum_rows")
    sum_cols = data.get("sum_cols")
    select = sheet_id_middleware.select
    if select == 'create':
        await message.answer('идет создание таблицы...', sleep=2)
        url = await (create_spreadsheet(name, name_worksheets, sum_rows, sum_cols))
        print('url', url)
        sheet_id_middleware.sheet_id = url
        print('sheet_id', sheet_id_middleware.sheet_id)
        await message.answer(f"Таблица {name} создана, в нее добавлен лист {name_worksheets}\n\n"
                             f"кол-во строк в листе: {sum_rows}\n\n"
                             f"кол-во столбцов в листе: {sum_cols}\n\n"
                             f"<a href='https://docs.google.com/spreadsheets/d/{url}/edit#gid=0'>Ссылка на таблицу</a>"
                             f"\n\n"
                             f"данные будем сейчас вносить в таблицу?",
                             reply_markup=create_file_y_n(), parse_mode="HTML")
    else:
        table = sheet_id_middleware.select_
        await message.answer('идет создание листа...', sleep=2)
        create = create_worksheet(table, name_worksheets, sum_rows, sum_cols)
        print('create', create)
        if create:
            sheet_id = get_spreadsheet_id(spreadsheet_name=table)
            print('sheet_id', sheet_id)
            sheet_id_middleware.sheet_id = sheet_id
            await message.answer(f"В таблицу {table} добавлен лист {name_worksheets}\n\n"
                                 f"кол-во строк в листе: {sum_rows}\n\n"
                                 f"кол-во столбцов в листе: {sum_cols}\n\n"
                                 f"данные будем сейчас вносить в таблицу?",
                                 reply_markup=create_file_y_n())
    await state.set_state(StateCreate.yes_no_news)

@router_new_table.callback_query(KbNewFiles.filter(), StateCreate.yes_no_news)
async def yes_no_news(call: types.CallbackQuery, callback_data: KbNewFiles, state: FSMContext):
    callbacks = callback_data.select_tables
    if callbacks == "yes":
        await call.message.answer(f"Сначала нужно заполнить 'шапку' таблицы.\n"
                                  f"введи название столбцов через запятую, "
                                  f"если название какого-то столбца не нужно - введи 0\n"
                                  f"если не надо добавлять названия столбцов введи '-'")
        await state.set_state(StateWriteNew.col)
    else:
        await call.message.answer(f"когда понадобится добавить данные, в меню выбери команду 'Записать'")
        await state.clear()
    await call.message.edit_reply_markup(reply_markup=None)
