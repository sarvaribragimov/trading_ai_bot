import asyncio

from beatifulsoup import get_column_inner_data
from data.get_company_info import get_stock_info
from data.utils import getbarcharttableinfo, get_openai_question
from utils.db_api import database
from bot import dp
from chatgpt import openai
from data.config import SUPER_ADMIN, ADMINS
from loader import bot
from screnshot import Setup

async def send_to_user(ticker, algorithm,date,day):
    try:
        res = await database.BarchartExpired().get_max_token()
        if res:
            co = await get_column_inner_data(ticker)
            q = get_openai_question()
            if res['status'] == 'ACTIVE':
                ticker = ticker.strip()
                print('||',ticker,'||s')
                barchart = await getbarcharttableinfo(ticker)
                if '401' in barchart:
                    await bot.send_message(chat_id='523886206', text=f"Token eskirdi")
                    await bot.send_message(chat_id='6866199714', text=f"Token eskirdi")
                    await database.BarchartExpired().add_token(status='INACTIVE')
                else:
                    questions = str(q) + str(co) + str(barchart)
                    ai_response = await openai(questions)
                    if '401' in ai_response:
                        await bot.send_message(chat_id='523886206', text=f"Chatgpt Token muddati tugadi")
                        await bot.send_message(chat_id='6866199714', text=f"Chatgpt Token muddati tudadi")
                        await database.BarchartExpired().add_token(status='INACTIVE')
                    else:
                        if ai_response:
                            if isinstance(ai_response, dict):
                                ai_response = str(ai_response)
                            try:
                                web = Setup(ticker=str(ticker))
                                web.init()
                                path, price = web.screenshot()
                                web.close_browser()
                            except Exception as e:
                                await bot.send_message(chat_id=SUPER_ADMIN, text=f'screnshot error: {e}')
                            text = f"<b>Aksiya tikeri:</b> {ticker}\n" \
                                   f"<b>Islamicly:</b> {get_stock_info(ticker)}\n" \
                                   f"<b>Narxi:</b> {price}\n" \
                                   f"<b>Algoritm nomi:</b> {day}\n" \
                                   f"<b>Kelgan vaqti:</b> {date}"
                            with open(path, 'rb') as photo:
                                message = await bot.send_photo(chat_id='523886206', photo=photo, caption=text)
                                await bot.send_message(chat_id='523886206', text=f"{ticker} uchun taxlil\n {ai_response}")
                                db = database.UsersTable()
                                users = await db.search(all=True)
                                count = 0
                                photo_file_id = message.photo[-1].file_id
                                try:
                                    if users:
                                        for user in users:
                                            try:
                                                if photo_file_id:
                                                    if len(text) + len(ai_response)>1000:
                                                        await bot.send_photo(chat_id=user[0], photo=photo_file_id,caption=text)
                                                        await bot.send_message(chat_id=user[0], text=f"{ticker} uchun taxlil\n {ai_response}")
                                                    else:
                                                        await bot.send_photo(chat_id=user[0], photo=photo_file_id,caption=f"{text} \n {ai_response}")
                                                    await asyncio.sleep(0.1)
                                                count += 1
                                            except Exception as e:
                                                await dp.bot.send_message(chat_id=SUPER_ADMIN,text=f"Xatolik {user[0]} foydalanuvchiga xabar yuborishda: {e}")
                                        await dp.bot.send_message(chat_id=SUPER_ADMIN,text=f"{count} ta foydalanuvchiga xabar yuborildi!")
                                except Exception as e:
                                    await dp.bot.send_message(chat_id=SUPER_ADMIN,text=f"users error {e}")
                        else:
                            await dp.bot.send_message(chat_id=SUPER_ADMIN, text='xabar yuborilmadi')
            else:
                questions = str(q) + str(co)
                ai_response = await openai(questions)
                t = await send_user_el(ai_response=ai_response, ticker=ticker,day=day,date=date)
        else:
            await database.BarchartExpired().add_token(status='INACTIVE')
            await dp.bot.send_message(chat_id=SUPER_ADMIN, text='inactive saqlandi')
    except Exception as e:
        await dp.bot.send_message(chat_id='523886206', text=f'send_to_user error: {e}')



async def send_to_user_one(ticker, algorithm,date):
    try:
        ticker = ticker.strip()
        questions=(f'{ticker}  kompaniyasini tahlil qilib ber hozir savdoga kirsam boladimi hafta oxirigacha qaysi '
                   f'narxga kotarilib berishi mumkin. javobing 1000 ta belgidan oshmasin')

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
                await bot.send_photo(chat_id='523886206', photo=photo, caption=text[:1000])
        else:
            await dp.bot.send_message(chat_id=SUPER_ADMIN, text='xabar yuborilmadi')
    except Exception as e:
        await dp.bot.send_message(chat_id=SUPER_ADMIN, text=f'send_to_user error: {e}')

async def send_user_el(ai_response,ticker,day,date):
    if ai_response:
        if isinstance(ai_response, dict):
            ai_response = str(ai_response)
        web = Setup(ticker=str(ticker))
        web.init()
        path, price = web.screenshot()
        web.close_browser()
        text = f"<b>Aksiya tikeri:</b> {ticker}\n" \
               f"<b>Islamicly:</b> {get_stock_info(ticker)}\n" \
               f"<b>Narxi:</b> {price}\n" \
               f"<b>Algoritm nomi:</b> {day}\n" \
               f"<b>Kelgan vaqti:</b> {date}"
        with open(path, 'rb') as photo:
            message = await bot.send_photo(chat_id='523886206', photo=photo, caption=text)
            await bot.send_message(chat_id='523886206', text=f"{ticker} uchun taxlil\n {ai_response}")
            db = database.UsersTable()
            users = await db.search(all=True)
            count = 0
            photo_file_id = message.photo[-1].file_id
            try:
                if users:
                    for user in users:
                        try:
                            if photo_file_id:
                                if len(text) + len(ai_response) > 1000:
                                    await bot.send_photo(chat_id=user[0], photo=photo_file_id, caption=text)
                                    await bot.send_message(chat_id=user[0],
                                                           text=f"{ticker} uchun taxlil\n {ai_response}")
                                else:
                                    await bot.send_photo(chat_id=user[0], photo=photo_file_id,
                                                         caption=f"{text} \n {ai_response}")
                                await asyncio.sleep(0.1)
                            count += 1
                        except Exception as e:
                            await dp.bot.send_message(chat_id=SUPER_ADMIN,
                                                      text=f"Xatolik {user[0]} foydalanuvchiga xabar yuborishda: {e}")
                    await dp.bot.send_message(chat_id=SUPER_ADMIN, text=f"{count} ta foydalanuvchiga xabar yuborildi!")
            except Exception as e:
                await dp.bot.send_message(chat_id=SUPER_ADMIN, text=f"users error {e}")
    else:
        await dp.bot.send_message(chat_id=SUPER_ADMIN, text='xabar yuborilmadi')