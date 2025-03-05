import asyncio
import time

from beatifulsoup import get_column_inner_data
from bot import dp
from chatgpt import openai
from data.config import SUPER_ADMIN, ADMINS
from data.utils import getbarcharttableinfo
from loader import bot
from screnshot import Setup

async def send_to_user(ticker, algorithm,date):
    try:
        col = await get_column_inner_data(ticker)
        questions = col if isinstance(col, str) else str(col)
        if '401' in questions:
            print('401')
            await bot.send_message(text='token eskirdi 401',chat_id=SUPER_ADMIN)
        else:
            if not questions:
                return
            parts = await openai(questions)
            if parts:
                if isinstance(parts, dict):
                    parts = str(parts)  # Uni stringga o‘girish
                web = Setup(ticker='NVDA')
                web.init()
                path, price = web.screenshot()

                web.close_browser()
                text = f"<b>Aksiya tikeri:</b> {ticker}\n" \
                       f"<b>Narxi:</b> {price}\n" \
                       f"<b>Algoritm nomi:</b> {algorithm}\n" \
                       f"<b>Kelgan vaqti:</b> {date} {parts}"
                with open(path, 'rb') as photo:
                    for chat_id in ADMINS:
                        await dp.bot.send_photo(chat_id=chat_id, photo=photo, caption=text)
                        # await bot.send_message(text=parts,chat_id=SUPER_ADMIN)
            else:
                await dp.bot.send_message(chat_id=SUPER_ADMIN, text='xabar yuborilmadi')
    except Exception as e:
        print('send_to_user error', e)
        await dp.bot.send_message(chat_id=SUPER_ADMIN, text=f'send_to_user error: {e}')


