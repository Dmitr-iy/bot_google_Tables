from aiogram.filters.callback_data import CallbackData


class Start(CallbackData, prefix='start'):
    choice: str

class Select(CallbackData, prefix='select'):
    select_view: str
    # select_sheet: str
    view_sheet: str

class SelectSheet(CallbackData, prefix='select_sheet'):
    select_sheet: str
    sheet_id: str

class SelectDelete(CallbackData, prefix='select_del'):
    select: str

class SelectDel(CallbackData, prefix='select__del'):
    select_sheet: str

class SelectDeletes(CallbackData, prefix='select_deletes'):
    select_del: str

class ViewObject(CallbackData, prefix='views'):
    views: str

class ViewSelect(CallbackData, prefix='view'):
    view: str

class ViewRow(CallbackData, prefix='view_row'):
    view_row: str

class Write(CallbackData, prefix='write'):
    nam: str

class WriteWorksheet(CallbackData, prefix='write_ws'):
    write_ws: str

class WriteData(CallbackData, prefix='write_data'):
    write_data: str

class WriteUpdate(CallbackData, prefix='write_'):
    write_: str

class WriteAll(CallbackData, prefix='write_all'):
    write_alls: str

class KbNewFil(CallbackData, prefix="create_new_fil"):
    select_tabl: str

class KbNewFile(CallbackData, prefix="create_new_file"):
    select_table: str

class KbNewFiles(CallbackData, prefix="create_new_files"):
    select_tables: str

class Admin(CallbackData, prefix="admin"):
    admin: str
