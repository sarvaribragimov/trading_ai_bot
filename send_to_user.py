import asyncio
from beatifulsoup import get_column_inner_data
from bot import dp
from chatgpt import openai
from data.config import SUPER_ADMIN
from screnshot import Setup

async def send_to_user(ticker, algorithm,date):
    try:
        questions = await get_column_inner_data(ticker)
        print('1')
        print(len(questions))
        if not questions:  # Agar malumot bo'lmasa, xabar chiqarish
            return
        parts = await openai(questions)
        if parts:
            if isinstance(parts, dict):
                parts = str(parts)  # Uni stringga o‘girish
            web = Setup(ticker=ticker)
            web.init()
            path, price = web.screenshot()
            web.close_browser()
            text = f"<b>Aksiya tikeri:</b> {ticker}\n" \
                   f"<b>Narxi:</b> {price}\n" \
                   f"<b>Algoritm nomi:</b> {algorithm}\n" \
                   f"<b>Kelgan vaqti:</b> {date} \n {parts}"
            with open(path, 'rb') as photo:
                await dp.bot.send_photo(chat_id=SUPER_ADMIN, photo=photo, caption=text)
        else:
            await dp.bot.send_message(chat_id=SUPER_ADMIN, text='xabar yuborilmadi')
    except Exception as e:
        print('send_to_user error', e)
        await dp.bot.send_message(chat_id=SUPER_ADMIN, text=f'send_to_user error: {e}')


