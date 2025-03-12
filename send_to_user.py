import asyncio
import time

from aiogram.types import InputMediaPhoto
from aiogram import types
from utils.db_api import database
from beatifulsoup import get_column_inner_data
from bot import dp
from chatgpt import openai
from data.config import SUPER_ADMIN, ADMINS
from data.utils import getbarcharttableinfo
from loader import bot
from screnshot import Setup

async def send_to_user(ticker, algorithm,date):
    try:
        ticker = ticker.strip()
        questions=(f'{ticker}  kompaniyasini tahlil qilib ber hozir savdoga kirsam boladimi hafta oxirigacha qaysi '
                   f'narxga kotarilib berishi mumkin. javobing 1000 ta belgidan oshmasin')
        print(questions)
        ai_response = await openai(questions)
        if ai_response:
            if isinstance(ai_response, dict):
                ai_response = str(ai_response)
            web = Setup(ticker=str(ticker))
            web.init()
            path, price = web.screenshot()
            web.close_browser()
            text = f"<b>Aksiya tikeri:</b> {ticker}\n" \
                   f"<b>Narxi:</b> {price}\n" \
                   f"<b>Algoritm nomi:</b> {algorithm}\n" \
                   f"<b>Kelgan vaqti:</b> {date} {ai_response}"

            with open(path, 'rb') as photo:
                message = await bot.send_photo(chat_id='523886206', photo=photo, caption=text[:1000])
                db = database.UsersTable()
                users = await db.search(all=True)
                count = 0
                photo_file_id = message.photo[-1].file_id  # Yuborilgan rasmning file_id sini saqlab qolamiz

            # Endi barcha foydalanuvchilarga rasmni file_id orqali yuborish
            for user in users:
                try:
                    if photo_file_id:
                        sent_message = await bot.send_photo(chat_id=user[0], photo=photo_file_id,
                                                            caption=text[:1000])
                    count += 1
                except Exception as e:
                    print(f"Xatolik {user[0]} foydalanuvchiga xabar yuborishda: {e}")

            print(f"{count} ta foydalanuvchiga xabar yuborildi!")

        else:
            await dp.bot.send_message(chat_id=SUPER_ADMIN, text='xabar yuborilmadi')
    except Exception as e:
        print('send_to_user error', e)
        await dp.bot.send_message(chat_id=SUPER_ADMIN, text=f'send_to_user error: {e}')


