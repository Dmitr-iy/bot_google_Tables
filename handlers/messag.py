import os
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from utils.callbackdata import Admin
from utils.managers import save_message, clear_messages, delete_messages, get_user_name
from utils.state_class import StateMessage, StatSupport, StateAdmin

router_message = Router()

@router_message.message(StateMessage.message_text)
async def get_message(message, state: FSMContext):
    try:
        message_text = message.text
        print("", message_text)
        await state.update_data(message_text=message_text)
        user_id = str(message.from_user.id)
        allowed_chat_ids = os.environ.get('allowed_chat_ids', '').split(',')
        if user_id in allowed_chat_ids:
            recipient_id = allowed_chat_ids[1] if user_id == allowed_chat_ids[0] else allowed_chat_ids[0]
            print("recipient_id", recipient_id)
            await message.bot.send_message(recipient_id, f"Сообщение от {message.from_user.full_name}:\n"
                                                         f" {message_text}")
            await message.reply("сообщение отправлено!")
            await state.clear()
        else:
            await message.answer("Ваш ID не найден в списке пользователей.")
            await state.clear()
    except Exception as e:
        print(e)

@router_message.message(StatSupport.message_text)
async def saved_message(message, state: FSMContext):
    try:
        user_id = str(message.from_user.id)
        user_name = message.from_user.first_name
        text = message.text
        saved = save_message(user_id, user_name, text)
        if saved:
            await message.reply("Ваше сообщение сохранено и будет передано администратору.")
            await state.clear()
        else:
            await message.reply("Произошла ошибка при сохранении сообщения. Попробуйте ещё раз.")
            await state.clear()
    except Exception as e:
        print(e)

# admin

@router_message.callback_query(Admin.filter())
async def handle_clear_messages(call: CallbackQuery, callback_data: Admin, state: FSMContext):
    clear_files = callback_data.admin
    print('clear_files', clear_files)
    user_id = str(call.from_user.id)
    print('user_id', user_id)
    allowed_chat_ids = os.environ.get('allowed_chat_ids', '').split(',')
    if user_id in allowed_chat_ids:
        if clear_files == 'clear':
            result = clear_messages()
            print('result', result)
            if result:
                await call.message.answer("Все сообщения были удалены.")
            else:
                await call.message.answer("Произошла ошибка при удалении сообщений.")
        else:
            recipient_name = await get_user_name(message=call, user_id=user_id, allowed_chat_ids=allowed_chat_ids)
            print('recipient_name', recipient_name)
            await call.message.answer(f"Выбери пользователя чьи сообщения удалить: {recipient_name}\n"
                                      f"{call.from_user.full_name}")
            await state.set_state(StateAdmin.message_text)
    else:
        await call.message.answer("У вас нет прав для удаления сообщений.")

@router_message.message(StateAdmin.message_text)
async def get_message(message, state: FSMContext):
    user_select = message.text
    print('user_select', user_select)
    user_id = str(message.from_user.id)
    allowed_chat_ids = os.environ.get('allowed_chat_ids', '').split(',')

    if user_id in allowed_chat_ids:
        command_args = user_select
        print('command_args', command_args)
        if command_args:
            result = delete_messages(user_id=command_args)
            print('result', result)
            if result:
                await message.answer(f"Сообщения от пользователя с ID {command_args} были удалены.")
            else:
                await message.answer("Произошла ошибка при удалении сообщений.")
        else:
            await message.answer("Пожалуйста, укажите ID пользователя, чьи сообщения вы хотите удалить.")
    else:
        await message.answer("У вас нет прав для удаления сообщений.")

    await state.clear()
