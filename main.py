import asyncio
from aiogram import Bot, Dispatcher
import logging

# from bot.handlers.handler_commands import router_commands
# from bot.handlers.handler_msg_save import router_save_msg
# from bot.handlers.handlers_save_object import router_save
# from bot.handlers.handlers_save_workers import router_save_workers
# from bot.utils.commands import set_commands
from data.config import config_settings
from handlers.create.handler_start import router_start_created
from handlers.create.new_table import router_new_table
from handlers.delete_data import router_delete
from handlers.start import router_commands
from handlers.view_data import router_view_data
from handlers.write.car import router_writer_car
from handlers.write.consumables import router_writer_consumables
from handlers.write.date_end import router_writer_date_end
from handlers.write.date_start import router_writer_date_start
from handlers.write.name_obj import router_write_name
# from handlers.write.object import router_write_object
from handlers.write.petrol_obj import router_writer_petrol
from handlers.write.repair_tools import router_writer_repair_tools
from handlers.write.salary import router_writer_salary
from handlers.write.write_data import router_write_data
from utils.commands import set_commands
from utils.middleware import sheet_id_middleware, ChatActionMiddleware


# from middlewares.dbmiddlewares import DbConnection
# from bot.handlers.start import router_start


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(config_settings.admin_id, "Бот запущен")

async def stop_bot(bot: Bot):
    await bot.send_message(config_settings.admin_id, "Бот остановлен")

# async def create_pool():
#     return await asyncpg.create_pool(
#         user=config_settings.db_user,
#         password=config_settings.db_password.get_secret_value(),
#         database=config_settings.db_name,
#         host=config_settings.db_host,
#         port=config_settings.db_port,
#     )

async def start():

    bot = Bot(token=config_settings.bot_token.get_secret_value(), parse_mode="HTML")
    # pool_connect = await create_pool()

    dp = Dispatcher()
    dp.update.middleware(sheet_id_middleware)
    dp.update.middleware(ChatActionMiddleware())
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        dp.include_routers(router_commands, router_view_data, router_write_data,
                           router_write_name, router_writer_date_start, router_writer_date_end,
                           router_writer_consumables, router_writer_repair_tools, router_writer_car,
                           router_writer_petrol, router_writer_salary, router_start_created,
                           router_new_table, router_delete)
        # dp.include_router(router_write_all)

        # dp.update.middleware(DbConnection(pool_connect))
        # dp.include_routers(router_commands, router_start, router_save, router_save_msg, router_save_workers)

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
