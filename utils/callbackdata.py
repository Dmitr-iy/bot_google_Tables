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
    select_del: str

class ViewObject(CallbackData, prefix='views'):
    views: str

class ViewSelect(CallbackData, prefix='view'):
    view: str

class ViewRow(CallbackData, prefix='view_row'):
    view_row: str

class Write(CallbackData, prefix='write'):
    write: str
    nam: str
    all_write: str

class WriteObject(CallbackData, prefix='write_obj'):
    write_obj: str

class WritePrice(CallbackData, prefix='write_price'):
    write_price: str

class WritePrice2(CallbackData, prefix='write_price'):
    write_price2: str

class WriteConsumables(CallbackData, prefix='write_consumables'):
    write_consumables: str

class WriteConsumables2(CallbackData, prefix='write_consumables'):
    write_consumables2: str

class WriteTool(CallbackData, prefix='write_tool'):
    write_tool: str

class WriteTool2(CallbackData, prefix='write_tool'):
    write_tool2: str

class WriteCar(CallbackData, prefix='write_car'):
    write_car: str
    write_car2: str

class WritePetrol(CallbackData, prefix='write_petrol_obj'):
    write_petrol_obj: str
    write_petrol_obj2: str

class WriteSalary(CallbackData, prefix='write_salary'):
    write_salary: str
    write_salary2: str

class WriteAll(CallbackData, prefix='write_all'):
    write_alls: str
