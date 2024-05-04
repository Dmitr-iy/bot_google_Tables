from aiogram import Router, types, flags
from aiogram.fsm.context import FSMContext
from keyboards.inline_kb.kb_create.kb_new_file import create_file_y_n
from utils.callbackCreate import KbNewFile
from utils.fun_gspread import create_spreadsheet, examination_name
from utils.state_class import StateCreate


router_new_table = Router()

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
    data = await state.get_data()
    name = data.get("name")
    name_worksheets = data.get("name_ws")
    await message.answer(f"В таблицу {name} добавлен лист {name_worksheets}!\n\n"
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
    await message.answer('идет создание таблицы...', sleep=2)
    url = await (create_spreadsheet(name, name_worksheets, sum_rows, sum_cols))
    await message.answer(f"Таблица {name} создана, в нее добавлен лист {name_worksheets}\n\n"
                         f"кол-во строк в листе: {sum_rows}\n\n"
                         f"кол-во столбцов в листе: {sum_cols}\n\n"
                         f"<a href='https://docs.google.com/spreadsheets/d/{url}/edit#gid=0'>Ссылка на таблицу</a>\n\n"
                         f"данные будем сейчас вносить в таблицу?",
                         reply_markup=create_file_y_n())
    await state.set_state(StateCreate.yes_no_news)

    @router_new_table.callback_query(KbNewFile.filter(), StateCreate.yes_no_news)
    async def yes_no_news(call: types.CallbackQuery, callback_data: KbNewFile, state: FSMContext):
        callbacks = callback_data.yes_no_new
        if callbacks == "yes":
            await call.message.answer(f"все готово, в меню выбери команду 'Записать'")
            await state.clear()
        else:
            await call.message.answer(f"когда понадобится добавить данные, в меню выбери команду 'Записать'")
            await state.clear()





