from aiogram.filters.callback_data import CallbackData


class KbStart(CallbackData, prefix="create"):
    type: str

class KbNewFile(CallbackData, prefix="create_new_file"):
    yes_no_new: str
