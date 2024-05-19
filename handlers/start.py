from aiogram import Router, F
from aiogram.filters import Command, StateFilter
import os
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.inline_kb.kb_new_file import kb_start
from keyboards.inline_kb.select_kb import select_kb, deletes
from keyboards.inline_kb.write_kb import write_kb, kb_admin
from utils.managers import get_messages, get_user_name
from utils.state_class import StateMessage, StatSupport

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
    user_id = str(message.from_user.id)
    allowed_chat_ids = os.environ.get('allowed_chat_ids', '').split(',')
    if user_id in allowed_chat_ids:
        recipient_name = await get_user_name(message, user_id, allowed_chat_ids)
        await message.answer(f"Описание функционала бота.\n\nКоманда *_'Старт'_* - запуск бота."
                             f"\nКоманда *_'посмотреть'_* - посмотреть данные в таблице.\n"
                             f"Команда *_'записать'_* - записать данные.\nКоманда *_'создать'_* - создать новую "
                             f"таблицу или новый лист в таблице.\nКоманда *_'удалить'_* - удалить таблицу или "
                             f"лист в таблице.\nКоманда *_'отменить'_* - отмена текущего процесса. "
                             f"В процессе создания или просмотра данных можно отменить процесс и начать "
                             f"сначала или выбрать другую команду.\nКоманда *_'Сообщение'_* - "
                             f"можно отправить сообщение *{recipient_name}*. Сообщения отправляются и приходят в этот "
                             f"бот, только в том чате, в котором находится пользователь.\n"
                             f"команда *_'support'_* - отправить сообщение в службу поддержки(сюда можно писать "
                             f"об ошибках бота, рекомендации по улучшению функционала бота и т.д.)",
                             parse_mode="Markdown")

# Запуск диспетчера
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
async def get_message(message: Message, state: FSMContext):
    await message.answer(f"введи Сообщение")
    await state.set_state(StateMessage.message_text)

@router_commands.message(Command(commands=["support"]))
async def get_support(message: Message, state: FSMContext):
    await message.answer(f"введи Сообщение для support")
    await state.set_state(StatSupport.message_text)

@router_commands.message(Command(commands=["admin"]))
async def admin_messages(message: Message):
    user_id = str(message.from_user.id)
    admin_id = os.environ.get('admin_id', '').split(',')
    if user_id in admin_id:
        messages = get_messages()
        response = "\n\n".join([f"{msg[1]} ({msg[0]}): {msg[2]} - {msg[3]}" for msg in messages])
        await message.answer(f"Сохраненные сообщения:\n\n{response}", reply_markup=kb_admin())
    else:
        await message.reply("У вас нет прав для просмотра этих сообщений.")
