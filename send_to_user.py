import asyncio
from beatifulsoup import get_column_inner_data
from bot import dp
from chatgpt import openai
from data.config import SUPER_ADMIN
from data.utils import getbarcharttableinfo
from loader import bot
from screnshot import Setup

async def send_to_user(ticker, algorithm,date):
    try:
        col, bar = await asyncio.gather(get_column_inner_data(ticker), getbarcharttableinfo(ticker))
        print(f"Type of col: {type(col)}")  # Bu qaysi tur ekanligini ko'rsatadi
        print(f"Type of bar: {type(bar)}")
        print('coll',col)
        print('bar',bar)
        if '401' in bar:
            print('4011')
            await bot.send_message(text=bar,chat_id=SUPER_ADMIN)
        else:
            questions = col + bar
            print('questions=',questions)
            if not questions:
                return
            parts = await openai(questions)
            if parts:
                if isinstance(parts, dict):
                    parts = str(parts)  # Uni stringga o‘girish
                web = Setup(ticker='NVDA')
                web.init()
                # path, price = web.screenshot()
                # web.close_browser()
                # text = f"<b>Aksiya tikeri:</b> {ticker}\n" \
                #        f"<b>Narxi:</b> {price}\n" \
                #        f"<b>Algoritm nomi:</b> {algorithm}\n" \
                #        f"<b>Kelgan vaqti:</b> {date}"
                # with open(path, 'rb') as photo:
                # await dp.bot.send_photo(chat_id=SUPER_ADMIN, photo=photo, caption=text)
                await bot.send_message(text=parts,chat_id=SUPER_ADMIN)
            else:
                await dp.bot.send_message(chat_id=SUPER_ADMIN, text='xabar yuborilmadi')
    except Exception as e:
        print('send_to_user error', e)
        await dp.bot.send_message(chat_id=SUPER_ADMIN, text=f'send_to_user error: {e}')


