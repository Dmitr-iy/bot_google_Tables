import os
from aiogram import Router
from aiogram.fsm.context import FSMContext
from utils.state_class import StateMessage


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
