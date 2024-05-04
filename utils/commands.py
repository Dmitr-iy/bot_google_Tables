from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start", description="Начать"
        ),
        BotCommand(
            command="help", description="инструкции"
        ),
        BotCommand(
            command="view", description="посмотреть"
        ),
        BotCommand(
            command="write", description="записать"
        ),
        BotCommand(
            command="create", description="создать"
        ),
        BotCommand(
            command="delete", description="удалить"
        ),
        BotCommand(
          command="cancel", description="Отменить"
        ),
        BotCommand(
            command="message", description="Сообщение"
        )
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
