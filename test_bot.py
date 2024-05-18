import pytest
from aiogram import Bot, Dispatcher, types
from unittest.mock import AsyncMock

# Замените 'YOUR_BOT_TOKEN' на ваш токен бота
BOT_TOKEN = 'YOUR_BOT_TOKEN'

@pytest.fixture
def bot():
    return Bot(token=BOT_TOKEN)

@pytest.fixture
def dp(bot):
    return Dispatcher(bot)

@pytest.fixture
def mock_message():
    return AsyncMock(types.Message)

async def start_command(message: types.Message):
    await message.answer("Hello! This is a test bot.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])

@pytest.mark.asyncio
async def test_start_command(bot, dp, mock_message):
    register_handlers(dp)

    mock_message.text = '/start'
    mock_message.answer = AsyncMock()

    await dp.process_update(mock_message)

    mock_message.answer.assert_called_with("Hello! This is a test bot.")
