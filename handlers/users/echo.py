from aiogram import types
from loader import dp


# Echo bot
@dp.message_handler(state='*')
async def bot_echo(message: types.Message):
    await message.answer("Nimadir xato /start ni bosib botni yangilang:(")
