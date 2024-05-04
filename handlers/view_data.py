from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram import flags
from keyboards.inline_kb.kb_view.kb_view_sheet_data import view_sheet_column, select_row_colm, view_sheet_row
from keyboards.inline_kb.select_kb import select_ws_view
from utils.callbackdata import Select, ViewObject, SelectSheet, ViewSelect, ViewRow
from utils.fun_gspread import get_spreadsheet_id, get_cell, get_sheet_row_object, get_sheet_column_object
from utils.managers import view_all_list, get_cells
from utils.middleware import sheet_id_middleware


router_view_data = Router()
router_view_data.callback_query.middleware(sheet_id_middleware)

@flags.flag("long_operation")
@router_view_data.callback_query(Select.filter())
async def call_view(call: CallbackQuery, callback_data: Select):
    spreadsheet_name = callback_data.select_view
    print(spreadsheet_name)
    sheet_id = get_spreadsheet_id(spreadsheet_name)
    sheet_id_middleware.sheet_id = sheet_id
    sheet_id_middleware.spreadsheet_name = spreadsheet_name
    print("вывод id", sheet_id)
    await call.message.answer(f"в таблице {spreadsheet_name} выбери лист", reply_markup=select_ws_view(sheet_id))
    await call.message.edit_reply_markup(reply_markup=None)

@flags.flag("long_operation")
@router_view_data.callback_query(SelectSheet.filter())
async def select_view_ws(call: CallbackQuery, callback_data: SelectSheet):
    ws = callback_data.select_sheet
    sheet_id_middleware.work_sheet = ws
    sheet_id = sheet_id_middleware.sheet_id
    spreadsheet_name = sheet_id_middleware.spreadsheet_name
    print("data", sheet_id)
    print('worksheet', ws)
    await call.message.answer(f"в таблице {spreadsheet_name}, листе {ws}, по столбцу или по строке вывести данные",
                              reply_markup=select_row_colm())
    await call.message.edit_reply_markup(reply_markup=None)

@router_view_data.callback_query(ViewSelect.filter())
async def select_workers(call: CallbackQuery, callback_data: ViewSelect):
    sheet_id = sheet_id_middleware.sheet_id
    ws = sheet_id_middleware.work_sheet
    view = callback_data.view
    cell = get_cell(ws, sheet_id)
    sheet_id_middleware.cell = cell
    if view == "row":
        await call.message.answer(f"в листе {ws} выбери данные, либо посмотри данные всей таблицы\n"
                                  f" _шапка таблицы_\n", parse_mode="Markdown",
                                  reply_markup=view_sheet_row(ws, sheet_id))
    else:
        await call.message.answer(f"в листе {ws} выбери данные, либо посмотри данные всей таблицы\n"
                                  f" _{cell}_\n", parse_mode="Markdown",
                                  reply_markup=view_sheet_column(ws, sheet_id))
        await call.message.edit_reply_markup(reply_markup=None)

@router_view_data.callback_query(ViewObject.filter())
async def select_object_row(call: CallbackQuery, callback_data: ViewObject):
    obj_list = callback_data.views
    print("Select", obj_list)
    work_sheet = sheet_id_middleware.work_sheet
    print("work_sheet", work_sheet)
    sheet_id = sheet_id_middleware.sheet_id
    print("sheet_id", sheet_id)
    if obj_list == "all":
        await view_all_list(call)
        await call.message.edit_reply_markup(reply_markup=None)
    else:
        data = get_sheet_row_object(sheet_id, work_sheet, obj_list)
        print('result_row', data)
        await get_cells(call, data)
        await call.message.edit_reply_markup(reply_markup=None)

@router_view_data.callback_query(ViewRow.filter())
async def select_object_column(call: CallbackQuery, callback_data: ViewRow):
    obj_list = callback_data.view_row
    print("Select", obj_list)
    work_sheet = sheet_id_middleware.work_sheet
    print("work_sheet", work_sheet)
    sheet_id = sheet_id_middleware.sheet_id
    print("sheet_id", sheet_id)
    if obj_list == "all":
        await view_all_list(call)
        await call.message.edit_reply_markup(reply_markup=None)
    else:
        data = get_sheet_column_object(sheet_id, work_sheet, obj_list)
        print('result_row', data)
        await get_cells(call, data)
        await call.message.edit_reply_markup(reply_markup=None)
