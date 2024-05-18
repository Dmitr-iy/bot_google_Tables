from aiogram.fsm.state import StatesGroup, State


class StateWriteObject(StatesGroup):
    name_ = State()
    name_yes_n = State()
    name_update = State()

class StateWriteDate(StatesGroup):
    name_obj = State()
    date_start = State()
    obj = State()
    name_obj_end = State()
    obj_end = State()
    date_end = State()

class StateWritePrice(StatesGroup):
    name_obj_price = State()
    obj_price = State()
    yes_no = State()
    price__update = State()
    price_plus = State()
    price_minus = State()
    price = State()

class StateWriteConsumables(StatesGroup):
    name_obj_consumables = State()
    name_obj_cons = State()
    yes_no_cons = State()
    consumables__update = State()
    consumables_plus = State()
    consumables_minus = State()
    consumables = State()

class StateWriteRepairTools(StatesGroup):
    name_obj_repair_tools = State()
    name_obj_tools = State()
    yes_no_repair_tools = State()
    repair_tools__update = State()
    repair_tools_plus = State()
    repair_tools_minus = State()
    repair_tools = State()

class StateWriteCar(StatesGroup):
    name_obj_ = State()
    name_obj_car = State()
    yes_no_car = State()
    car__update = State()
    car_plus = State()
    car_minus = State()
    car = State()

class StateWritePetrol(StatesGroup):
    name_obj_petrol = State()
    name_obj_petrol_ = State()
    yes_no_petrol = State()
    petrol__update = State()
    petrol_plus = State()
    petrol_minus = State()
    petrol = State()

class StateWriteSalary(StatesGroup):
    name_obj_salary = State()
    name_obj_salary_ = State()
    yes_no_salary = State()
    salary__update = State()
    salary_plus = State()
    salary_minus = State()
    salary = State()

class StateWriteData(StatesGroup):
    cell_1 = State()
    cell_range_name_obj = State()
    cell_range_data_cell = State()
    cell_update = State()
class StateWriteAll(StatesGroup):
    cell_1_all = State()
    cell_2_all = State()

class StateCreate(StatesGroup):
    name = State()
    name_worksheets = State()
    sum_rows = State()
    sum_cols = State()
    yes_no_news = State()

class StateWriteNew(StatesGroup):
    col = State()
    row = State()
    column = State()

class StateMessage(StatesGroup):
    message_text = State()
