from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.database import DataBaseSql

async def on_startup(dispatcher):
#    await dp.bot.copy_message(chat_id=1805233745, from_chat_id= -1001596191086, message_id=674, caption="Tabriklaymiz, siz 'OPTIMUS ALGO' algoritmik signallar botiga rasman a'zo bo'ldingiz, ushbu video qo'llanma bilan tanishib chiqing")

    await DataBaseSql().create()
    await DataBaseSql().create_users()
    await DataBaseSql().delete(1805233745)
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
