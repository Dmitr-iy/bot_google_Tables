import asyncio
from aiogram import Bot, Dispatcher
import logging

from aiohttp import BasicAuth
from aiogram.client.session.aiohttp import AiohttpSession

from data.config import config_settings
from handlers.messag import router_message
from handlers.new_table import router_new_table
from handlers.delete_data import router_delete
from handlers.start import router_commands
from handlers.view_data import router_view_data
from handlers.write_data import router_write_data
from utils.commands import set_commands
from utils.middleware import sheet_id_middleware, ChatActionMiddleware


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(config_settings.admin_id, "Бот запущен")

async def stop_bot(bot: Bot):
    await bot.send_message(config_settings.admin_id, "Бот остановлен")

async def start():
    auth = BasicAuth(login="gvncnbbf", password="k0u8o62jgu6z")
    session = AiohttpSession(proxy=("http://45.94.47.66:8110", auth))

    bot = Bot(token=config_settings.bot_token.get_secret_value(), session=session)

    dp = Dispatcher()
    dp.update.middleware(sheet_id_middleware)
    dp.update.middleware(ChatActionMiddleware())
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        dp.include_routers(router_commands, router_view_data, router_write_data, router_new_table, router_delete,
                           router_message)

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"An error occurred during bot polling: {e}")
        await bot.send_message(config_settings.admin_id, f"An error occurred during bot polling: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
                        )
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        loop.close()
