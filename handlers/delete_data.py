from aiogram import Router, types
from utils.callbackdata import SelectDelete
from utils.fun_gspread import delete_spreadsheet

router_delete = Router()

@router_delete.callback_query(SelectDelete.filter())
async def delete(call: types.CallbackQuery, callback_data: SelectDelete):
    name = callback_data.select_del
    print(name)
    deleting = await delete_spreadsheet(name.strip())
    if deleting:
        await call.message.answer(f"Таблица {name} удалена.")
    else:
        await call.message.answer(f"Таблица {name} не существует.")
    # await call.message.delete()
