import asyncio
from aiogram import executor
# from forwarder import connect_to_imap
from loader import dp
import middlewares, filters, handlers
from send_mail import send_mail
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
    asyncio.create_task(send_mail())



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)


