from aiogram import Router, F
from aiogram.filters import Command, StateFilter
import os
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.inline_kb.kb_create.kb_new_file import kb_start
from keyboards.inline_kb.select_kb import select_kb, deletes
from keyboards.inline_kb.write_kb import write_kb


router_commands = Router()

@router_commands.message(Command(commands=["start"]))
async def get_start(message: Message):
    allowed_chat_ids = [int(chat_id) for chat_id in os.environ.get('allowed_chat_ids', '').split(',')]
    chat_id = message.chat.id
    if chat_id in allowed_chat_ids:
        await message.answer(f"Привет{message.from_user.full_name}, в меню выбери команду."
                             f" Для ознакомления с инструкциями нажми инструкции.")
    else:
        await message.answer("У вас нет доступа к этому боту.")

@router_commands.message(Command(commands=["help"]))
async def get_help(message: Message):
    await message.answer("инструкции")

@router_commands.message(Command(commands=["view"]))
async def get_view(message: Message):
    await message.answer("в какой таблице посмотреть данные: ", reply_markup=select_kb())

@router_commands.message(Command(commands=["write"]))
async def get_write(message: Message):
    await message.answer("в какой таблице записать данные: ", reply_markup=write_kb())

@router_commands.message(Command(commands=["create"]))
async def get_create(message: Message):
    await message.answer("создать: ", reply_markup=kb_start())

@router_commands.message(Command(commands=["delete"]))
async def get_delete(message: Message):
    await message.answer('удалить таблицу или лист в таблице?', reply_markup=deletes())

@router_commands.message(StateFilter(None), Command("cancel"))
@router_commands.message(default_state, F.text.lower() == "отменить")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )

@router_commands.message(Command("cancel"))
@router_commands.message(F.text.lower() == "отменить")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )

@router_commands.message(Command(commands=["message"]))
async def get_message(message: Message):
    await message.answer("Сообщение")
