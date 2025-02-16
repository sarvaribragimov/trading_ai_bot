from aiogram import types
from utils.db_api.database import TariffsTable

async def getTariffs():
    db = TariffsTable()
    tariffs = await db.search(all=True)
    m = types.InlineKeyboardMarkup(row_width=1)
    for tariff in tariffs:
        m.add(types.InlineKeyboardButton(text=tariff[0], callback_data=tariff[1]))
    return m
async def tariffs_key():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.add(*[types.KeyboardButton(text= t[0]) for t in  await TariffsTable().search(all=True)])
    return m



def signals_b(signals_type):
    print('signals_type', signals_type)  # Debug maqsadida chop etiladi
    m = types.InlineKeyboardMarkup(row_width=2)  # Inline tugmalar uchun markup
    for key, value in signals_type.items():
        print(key)
        m.add(types.InlineKeyboardButton(text=value, callback_data=key))  # Tugma yaratish
    return m


def signals_list_b(data):
    print('data:', data)
    m = types.InlineKeyboardMarkup(row_width=2)  # Inline tugmalar uchun markup
    for row in data:
        button_text = f"{row['signal_name']} ({row['status']})"  # Tugma matni
        callback_data = f"signal_{row['id']}"  # Tugmaga mos callback_data
        print('row==',row['id'])
        m.add(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
    return m

