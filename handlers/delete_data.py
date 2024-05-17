from aiogram import Router, types
from keyboards.inline_kb.select_kb import delete_worksheet, select_del, deletes
from utils.callbackdata import SelectDelete, SelectDel, SelectDeletes
from utils.fun_gspread import delete_spreadsheet, get_worksheet_list, delete_worksheets
from utils.middleware import sheet_id_middleware


router_delete = Router()

@router_delete.callback_query(SelectDelete.filter())
async def delete(call: types.CallbackQuery, callback_data: SelectDelete):
    select = callback_data.select
    print("Deleting", select)
    sheet_id_middleware.select = select
    await call.message.answer("выбери название таблицы:", reply_markup=delete_worksheet())
    await call.message.edit_reply_markup(reply_markup=None)

@router_delete.callback_query(SelectDel.filter())
async def delete(call: types.CallbackQuery, callback_data: SelectDel):
    name = callback_data.select_sheet
    print("name table", name)
    select = sheet_id_middleware.select
    if name:
        if name == 'back':
            back = await call.message.answer('удалить таблицу или лист в таблице?', reply_markup=deletes())
            await call.message.edit_reply_markup(reply_markup=None)
            return back
        else:
            if select == 'table':
                deleting = await delete_spreadsheet(name.strip())
                if deleting:
                    await call.message.answer(f"Таблица {name} удалена.")
                else:
                    await call.message.answer(f"Таблица {name} не существует.")
            else:
                if select == 'sheet':
                    sheet_id_middleware.name_spreadsheet = name
                    print(name)
                    if name:
                        deleting = get_worksheet_list(name)
                        print('deleting', deleting)
                        if len(deleting) > 1:
                            await call.message.answer(f"Какой лист удалить:", reply_markup=select_del(name))
                        elif len(deleting) == 1:
                            await call.message.answer(f"В этом документе один лист. "
                                                      f"Нельзя удалить все листы в документе.")
                        else:
                            await call.message.answer(f"В таблице {name} нет листов.")
    await call.message.edit_reply_markup(reply_markup=None)

@router_delete.callback_query(SelectDeletes.filter())
async def delete(call: types.CallbackQuery, callback_data: SelectDeletes):
    name = callback_data.select_del
    name_spreadsheet = sheet_id_middleware.name_spreadsheet
    if name == 'back':
        back = await call.message.answer("выбери название таблицы:", reply_markup=delete_worksheet())
        await call.message.edit_reply_markup(reply_markup=None)
        return back
    print("qq", name)
    deleting = delete_worksheets(name_spreadsheet, name)
    if deleting:
        await call.message.answer(f"Лист {name} удален.")
    else:
        await call.message.answer(f"Error")
    await call.message.edit_reply_markup(reply_markup=None)
