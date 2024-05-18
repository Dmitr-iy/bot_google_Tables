# import pytest
# from aiogram import Bot, Dispatcher, types
# from unittest.mock import AsyncMock
#
# # Замените 'YOUR_BOT_TOKEN' на ваш токен бота
# BOT_TOKEN = 'YOUR_BOT_TOKEN'
#
# @pytest.fixture
# def bot():
#     return Bot(token=BOT_TOKEN)
#
# @pytest.fixture
# def dp(bot):
#     return Dispatcher(bot)
#
# @pytest.fixture
# def mock_message():
#     return AsyncMock(types.Message)
#
# async def start_command(message: types.Message):
#     await message.answer("Hello! This is a test bot.")
#
# def register_handlers(dp: Dispatcher):
#     dp.register_message_handler(start_command, commands=["start"])
#
# @pytest.mark.asyncio
# async def test_start_command(bot, dp, mock_message):
#     register_handlers(dp)
#
#     mock_message.text = '/start'
#     mock_message.answer = AsyncMock()
#
#     await dp.process_update(mock_message)
#
#     mock_message.answer.assert_called_with("Hello! This is a test bot.")

import pytest
from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from unittest.mock import AsyncMock
import os


@pytest.fixture
def mock_bot():
    return AsyncMock(Bot)


@pytest.fixture
def mock_message(mock_bot):
    message = AsyncMock(types.Message)
    message.bot = mock_bot
    message.chat.id = 123456  # Пример chat_id
    message.text = "Test message"
    return message


@pytest.fixture
def mock_state():
    state = AsyncMock(FSMContext)
    return state


@pytest.mark.asyncio
async def test_get_message(mock_message, mock_state):
    os.environ['USER_ID'] = '654321'
    os.environ['ADMIN_ID'] = '123456'

    await get_message(mock_message, mock_state)

    mock_state.update_data.assert_called_with(message_text="Test message")
    mock_message.bot.send_message.assert_called_with('123456', "Test message")
