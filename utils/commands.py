from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start", description="Начать"
        ),
        BotCommand(
            command="read", description="Помощь"
        ),
        BotCommand(
          command="cancel", description="Отменить"
        ),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
