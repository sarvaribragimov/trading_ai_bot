import asyncio
import time

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
        # print('ticker', ticker,'type',type(ticker))
        co = await get_column_inner_data(str(ticker))
        barchart = await getbarcharttableinfo(str(ticker))
        col = str(co) + str(barchart)
        questions = col if isinstance(col, str) else str(col)
        if '401' in questions:
            print('401')
            await bot.send_message(text='token eskirdi 401',chat_id=SUPER_ADMIN)
        else:
            if not questions:
                return
            ai_response = await openai(questions)
            if ai_response:
                # db = database.UsersTable()
                # users = await db.search(all=True)
                # for user in users:
                #     await bot.send_message(text=f'{ticker}{date}{ai_response}', chat_id=user[0])

                if isinstance(ai_response, dict):
                    ai_response = str(ai_response)  # Uni stringga o‘girish
                web = Setup(ticker='NVDA')
                web.init()
                path, price = web.screenshot()

                web.close_browser()
                text = f"<b>Aksiya tikeri:</b> {ticker}\n" \
                       f"<b>Narxi:</b> {price}\n" \
                       f"<b>Algoritm nomi:</b> {algorithm}\n" \
                       f"<b>Kelgan vaqti:</b> {date} {ai_response}"
                with open(path, 'rb') as photo:
                    db = database.UsersTable()
                    users = await db.search(all=True)
                    for user in users:
                        # await bot.send_message(text=text, chat_id=user[0])
                        await dp.bot.send_photo(chat_id=user[0], photo=photo, caption=text)
                        # await bot.send_message(text=ai_response,chat_id=SUPER_ADMIN)
            else:
                await dp.bot.send_message(chat_id=SUPER_ADMIN, text='xabar yuborilmadi')
    except Exception as e:
        print('send_to_user error', e)
        await dp.bot.send_message(chat_id=SUPER_ADMIN, text=f'send_to_user error: {e}')


