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
    if config.sender_email in str(from_):
        message = str(subject).strip()
        # print('email',message,date)
        if "Alert: New symbol:" in message:
            ticker, all_algorithm = message.replace("Alert: New symbol:", "").replace("was added to", "%%").split("%%")
            match = re.search(r"(?:was added to|were added to)\s+(\S+)", message)
            date_match = re.search(r"Date:\s+(.+)", message)
            date = date_match.group(1) if date_match else datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
            print('send_to_user.........')
            await send_to_user(ticker=str(ticker), algorithm=str(match.group(1)), date=date)
        else:
            tickers, algorithm = message.replace("Alert: New symbols:", "").replace("were added to", "%%").split("%%")
            tickers = [t.strip() for t in tickers.split(",")]
            match = re.search(r"(?:was added to|were added to)\s+(\S+)", message)
            date_match = re.search(r"Date:\s+(.+)", message)
            date = date_match.group(1) if date_match else datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
            if tickers:
                for ticker in tickers:
                    await send_to_user(ticker=str(ticker),algorithm=str(match.group(1)),date=str(date))


async def send_mail():
    """Har 5 soniyada pochtani tekshirib, yangi xabarlarni yuboradi"""
    while True:
        try:
            imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
            imap.login(IMAP_USERNAME, IMAP_PASSWORD)
            imap.select("inbox")
            status, email_ids = imap.search(None, 'UNSEEN FROM "alerts@thinkorswim.com"')
            for email_id in email_ids[0].split():
                status, email_data = imap.fetch(email_id, "(RFC822)")
                raw_email = email_data[0][1]
                msg = email.message_from_bytes(raw_email)
                await process_email(msg)
            await asyncio.sleep(2)
            imap.close()
            imap.logout()
        except Exception as e:
            print(f"IMAP xatosi: {e}")
        await asyncio.sleep(5)
