import imaplib
import email
import asyncio
import re
import pytz
import time
from datetime import datetime
from email.header import decode_header
from data import config
from send_to_user import send_to_user

# IMAP sozlamalari
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
IMAP_USERNAME = config.imap_username
IMAP_PASSWORD = config.imap_password


async def process_email(msg):
    """Emailni o'qib, Telegramga yuborish"""
    subject, _ = decode_header(msg["Subject"])[0]
    from_, _ = decode_header(msg.get("From"))[0]
    date, _ = decode_header(msg.get("Date"))[0]

    print(f"New email: {subject} | From: {from_} | Date: {date}")

    # Sana formatini to'g'irlash
    try:
        date_string_cleaned = re.sub(r'\([^)]*\)', '', date).strip()
        dt_object = datetime.strptime(date_string_cleaned, "%a, %d %b %Y %H:%M:%S %z")
        uzbek_timezone = pytz.timezone('Asia/Tashkent')
        formatted_date = dt_object.astimezone(uzbek_timezone).strftime("%H:%M, %d-%b, %Y")
    except:
        formatted_date = date

    if config.sender_email in str(from_):
        message = str(subject).strip()
        if "Alert: New symbol:" in message:
            ticker, all_algorithm = message.replace("Alert: New symbol:", "").replace("was added to", "%%").split("%%")
            match = re.search(r"(?:was added to|were added to)\s+(\S+)", message)
            date_match = re.search(r"Date:\s+(.+)", message)
            date = date_match.group(1) if date_match else datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
            print('send_to_user.........')
            await send_to_user(ticker=str(ticker), algorithm=str(match.group(1)), date=date)
            time.sleep(2)

            # await main(algorithm, formatted_date, ticker=ticker.strip())
        else:
            tickers, algorithm = message.replace("Alert: New symbols:", "").replace("were added to", "%%").split("%%")
            tickers = [t.strip() for t in tickers.split(",")]
            match = re.search(r"(?:was added to|were added to)\s+(\S+)", message)
            date_match = re.search(r"Date:\s+(.+)", message)
            date = date_match.group(1) if date_match else datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
            if tickers:
                print('for all ti=========')
                for ticker in tickers:
                    print('send_to_user.........')
                    await send_to_user(ticker=str(ticker),algorithm=str(match.group(1)),date=str(date))
                    print('tickers: ', ticker, 'all algorithm', algorithm, 'algorithm', match.group(1), '||date:',
                          date)


# async def send_to_user(ticker,algorithm, date):
#     print(f"Sending email to {ticker} with algorithm {algorithm} on date {date}")

async def send_mail():
    """Har 5 soniyada pochtani tekshirib, yangi xabarlarni yuboradi"""
    while True:
        try:
            print('start')
            imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
            imap.login(IMAP_USERNAME, IMAP_PASSWORD)
            imap.select("inbox")

            # O'qilmagan xabarlarni tekshiramiz
            status, email_ids = imap.search(None, 'UNSEEN FROM "alerts@thinkorswim.com"')
            for email_id in email_ids[0].split():
                status, email_data = imap.fetch(email_id, "(RFC822)")
                raw_email = email_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Emailni qayta ishlash
                await process_email(msg)

            imap.close()
            imap.logout()
        except Exception as e:
            print(f"IMAP xatosi: {e}")
        print('sleeeeeeeep')
        await asyncio.sleep(5)
