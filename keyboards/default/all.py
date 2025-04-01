from data import config
from aiogram import types

async def admin_menu():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.add(*[types.KeyboardButton(text=b)  for b in  config.admin_sections ] )
    return m