from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.database import setup_tables, UsersTable
from data import config
from datetime import datetime as dt
async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)

    # set up database
    await setup_tables()
    # await UsersTable().delete(config.SUPER_ADMIN)
    await UsersTable().delete(1805233745)




if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
