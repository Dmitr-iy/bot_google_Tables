import asyncio
from aiogram import types
from aiogram.fsm.context import FSMContext
from utils.fun_gspread import get_all_sheet
from utils.middleware import sheet_id_middleware


# view
async def view_all_list(call: types.CallbackQuery):
    work_sheet = sheet_id_middleware.work_sheet
    sheet_id = sheet_id_middleware.sheet_id
    work_sheet_all_data = get_all_sheet(sheet_id, work_sheet)
    if work_sheet_all_data:
        columns = work_sheet_all_data[0]
        result_text = ""
        for row in work_sheet_all_data[1:]:
            for column, value in zip(columns, row):
                result_text += f"*{column.lower()}*: {value}\n\n"
            result_text += "\n\n"
        if len(result_text) <= 4096:
            await call.message.answer(result_text, parse_mode="Markdown")
        else:
            paragraphs = result_text.split('\n\n')
            chunk_size = 2000
            chunks = []
            chunk = ""
            for paragraph in paragraphs:
                if len(chunk) + len(paragraph) <= chunk_size:
                    chunk += paragraph + "\n\n"
                else:
                    chunks.append(chunk)
                    chunk = paragraph + "\n\n"
            if chunk:
                chunks.append(chunk)

            print(chunks)
            for chunk in chunks:
                await call.message.answer(chunk, parse_mode="Markdown")
                await asyncio.sleep(5)
    else:
        await call.message.answer("в таблице нет данных")

async def get_cells(call: types.CallbackQuery, data):
    if data:
        columns = data[0]
        result_text = ""
        for row in data[1:]:
            for column, value in zip(columns, row):
                result_text += f"*{column.lower()}*: {value}\n"
            result_text += "\n"
        await call.message.answer(result_text, parse_mode="Markdown")
    else:
        await call.message.answer("в таблице нет данных")

# write
async def responses(message: types.Message, state: FSMContext, result, states):
    response = "Найдены следующие объекты, содержащие это слово:\n"
    response += "\n".join(result)
    response += "\nПожалуйста, выбери нужный объект."
    await message.answer(response)
    await state.set_state(states)
