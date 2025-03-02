import imaplib
import email
import re
from email.utils import parsedate_to_datetime

import pytz

from data import config
from gemini import generate
from screnshot import Setup
from loader import dp
from data.config import *

imap_server = 'imap.gmail.com'
imap_port = 993
imap_username = 'lapasovsardorbek2000@gmail.com'
imap_password = 'xrberzvmmmovrnil'  # App Password

async def connect_to_imap():
    try:
        print("Connecting to IMAP server...")
        imap = imaplib.IMAP4_SSL(imap_server, imap_port)
        imap.login(imap_username, imap_password)
        print("Successfully connected and logged in!")
        imap.select("inbox")
        status, messages = imap.search(None, 'UNSEEN FROM "alerts@thinkorswim.com"')
        mail_ids = messages[0].split()
        if len(mail_ids) > 0:
            latest_mail_id = mail_ids[0]
            status, msg_data = imap.fetch(latest_mail_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Xabarni olish
                    msg = email.message_from_bytes(response_part[1])
                    date_header = msg["Date"]
                    date_obj = parsedate_to_datetime(date_header)

                    # Toshkent vaqtiga aylantirish
                    tashkent_tz = pytz.timezone("Asia/Tashkent")
                    date_tashkent = date_obj.astimezone(tashkent_tz)
                    formatted_date = date_tashkent.strftime("%H:%M, %d-%b, %Y")
                    print(f"Xabar vaqti (Toshkent): {formatted_date}")
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                # Xabarni hech qanday o'zgarishsiz o'qish
                                body = part.get_payload(decode=True).decode()
                                # print("\nEmail Content:\n", body)
                                # match = re.search(r"New symbol:\s*([A-Z]+)", body)
                                match = re.search(r"New symbol:\s*([A-Z]+)", body)
                                if match:
                                    print('ifd')
                                    ticker = match.group(1)
                                    algorithm = match.group(2)
                                    print(f"Ticker: {ticker}")
                                    web = Setup(ticker=ticker)
                                    web.init()
                                    path,price = web.screenshot()
                                    web.close_browser()
                                    text = f"Aksiya tikeri: {ticker}\n" \
                                           f"Narxi: {price}\n" \
                                           f"Algoritm nomi: {algorithm}\n" \
                                           f"Kelgan vaqti: {formatted_date}"
                                    with open(path, 'rb') as photo:
                                        message = await dp.bot.send_photo(chat_id=523886206, photo=photo, caption=text)
                                else:
                                    print("Ticker topilmadi.")
                                break

                    else:
                        raw_email = email_data[0][1]
                        msg = email.message_from_bytes(raw_email)
                        # print('else')
                        # body = msg.get_payload(decode=True).decode()
                        # match = re.search(r"New symbols:\s*([A-Z]+)", body)
                        # # match2 = re.search(r"were added to\s*([A-Z]+)", body)
                        # print(match)
                        # match2 = re.search(r"were added to\s*([A-Z]+)|was added to\s*([A-Z]+)", body)
                        # if match2:
                        #     ticker = match2.group(2)
                        #     print(f"Tiker: {ticker}")
                        # else:
                        #     print("Ticker topilmadi. Body matnini tekshiring!")
                        #
                        # tickers = match.group(1).split(", ")
                        # # algorithm = match2.group(1)
                        # # print('Algoritm',algorithm)
                        # print(match)
                        # for ticker in tickers:
                        #     print(f"Ticker: {ticker}")
                        #     parts = await generate(quessions(ticker))
                        #     print('parts',parts[0]['text'])
                        #     web = Setup(ticker=ticker)
                        #     web.init()
                        #     path,price = web.screenshot()
                        #     web.close_browser()
                        #     text = (f"<b>Aksiya tikeri:</b> {ticker}\n"
                        #             # f"<b>Algoritm nomi:</b> {algorithm}\n"
                        #             f"<b>Narxi:</b> {price} \n"
                        #             f"<b>Kelgan vaqti:</b> {formatted_date} \n"
                        #             f"{parts[0]['text']}")
                        #     with open(path, 'rb') as photo:
                        #         message = await dp.bot.send_photo(chat_id=523886206, photo=photo, caption=text)

        else:
            print("No messages found from the specified sender.")
        imap.logout()
    except Exception as e:
        print("Error:", e)


def quessions(ticker):
    text = (f"Quyidagi 5ta savol shablonini eslab qol, va aksiya tikeri jonatganimda  sen mana shu shablon asosida javob bergin. "
        f"Savollarga aniq va qisqa javob bergin, javoblardagi umumiy belgilar soni 500 ta belgidan  oshmasin. "
        f"1. “{ticker} ticker” kompaniya biznes faoliyati "
        f"2. Bu hafta uchun “{ticker} Tiker” aksiyasi uchun put /call ratio qiymatini va qancha put va qancha call option borligini aniqla "
        f"3. “{ticker} ticker” aksiyasi uchun bugungi holat boyicha aksiyaning qancha foiz qismi Short-Sale qilinganligini aniqla "
        f"4. “{ticker} ticker” aksiyaga oid oxirgi 3 kun Ichida qandaydir xabar chiqdimi, xabar sarlavhasini korsat va ijobiy yoki salbiy xabar ekanligni aniqlab qisqa javob ber "
        f"5. Yuqoridagi malumotlarga tayangan holda qisqa xulosangni ayt, ushbu kompaniya aksiyasini day trading uchun xarid qilsam boladimi yoki yoq?")
    return text


