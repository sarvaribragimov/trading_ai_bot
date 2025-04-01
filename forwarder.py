import imaplib
import email
from email.header import decode_header
import time
from data import config
from utils.db_api.database import DataBaseSql
from loader import bot
import asyncio
from drawer import Setup
from aiogram import types
from aiogram.types import InputMediaPhoto
from datetime import datetime
import pytz
import re




async def copy_media_group(chat_id, message):
    # Get the media group from the original message
    original_media_group = message

    # Create a copy of the media group
    copied_media_group = types.MediaGroup()

    # Iterate through the media in the original group and add them to the copy
    for media in original_media_group:
        if isinstance(media, InputMediaPhoto):
            # If it's a photo, add it to the copy
            copied_media_group.attach_photo(media.media)
        # You can add more conditions for other types of media (e.g., InputMediaVideo)

    # Send the copied media group to the same chat
    await bot.send_media_group(chat_id=chat_id, media=copied_media_group)
async def main(algorithm, date, tickers=None, ticker=None):
    await bot.send_message(chat_id=config.main_user, text=f"Ticker(s): {ticker or tickers}\nAlgorithm: {algorithm}\nDate: {date}")
    hour_minutes = date.split(',')[0]
    parsed_date = datetime.strptime(hour_minutes, "%H:%M")
    # interval = await Interval().search(
    #     ticker=" ".join(algorithm.strip().lower().replace('.', '').split())
    # )
    # print(interval)
    # if interval:
    #     start_date = datetime.strptime(interval[1], "%H:%M")
    #     end_date = datetime.strptime(interval[2], "%H:%M")
    #     if not (start_date <= parsed_date and parsed_date <= end_date):
    #         await bot.send_message(chat_id=config.main_user, text=f"O'tkazib yuborilgan: {algorithm}, {hour_minutes} da!")
    #         return
    if ticker:
        web = Setup(ticker=ticker)
        web.init()
        path = web.screenshot()
        web.close_browser()
        text = f"Aksiya tikeri: {ticker}\n" \
               f"Algoritm nomi: {algorithm}\n" \
               f"Kelgan vaqti: {date}"
        with open(path, 'rb') as photo:
            message = await bot.send_photo(chat_id=config.main_user, photo=photo, caption=text)
    else:
        # try:
        media_group = []
        print(tickers)
        for ticker in tickers:
            ticker = ticker.strip()
            web = Setup(ticker=ticker)
            web.init()
            path = web.screenshot()
            print(path)
            web.close_browser()
            media_group.append(
                types.InputMediaPhoto(media=open(path, 'rb')),
            )
        text = f"Aksiya tikerlari: {','.join(tickers)}\n" \
               f"Algoritm nomi: {algorithm}\n" \
               f"Kelgan vaqti: {date}"
        message = await bot.send_media_group(chat_id=config.main_user, media=media_group)
        await bot.edit_message_caption(chat_id=config.main_user, message_id=message[0].message_id, caption=text)

    users = await DataBaseSql().search_user(all=True)
    count = 0
    for u in users:
        try:
            if tickers is None:
                await bot.copy_message(chat_id=u[0], from_chat_id=config.main_user, message_id=message.message_id)
            else:
                photo_file_ids = [
                    types.InputMediaPhoto(media=media_message.photo[-1].file_id) for media_message in message
                ]
                message = await bot.send_media_group(chat_id=u[0], media=photo_file_ids)
                await bot.edit_message_caption(chat_id=u[0], message_id=message[0].message_id, caption=text)
            count += 1
        except:
             pass

# IMAP settings
imap_server = 'imap.gmail.com'
imap_port = 993
imap_username = config.email
imap_password = config.password

while True:
    # Connect to the IMAP server
    imap = imaplib.IMAP4_SSL(imap_server, imap_port)
    imap.login(imap_username, imap_password)

    imap.select('inbox')  # You can choose a different mailbox if needed
    # Search for unread emails
    status, email_ids = imap.search(None, f'(UNSEEN FROM "{config.sender_email}")')
    # Iterate through email IDs and retrieve email content
    for email_id in email_ids[0].split():
        EMAIL_ID = email_id
        status, email_data = imap.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1]

        # Parse the raw email content
        msg = email.message_from_bytes(raw_email)
        # Get email headers (subject, from, date)
        subject, _ = decode_header(msg["Subject"])[0]
        from_, _ = decode_header(msg.get("From"))[0]
        date, _ = decode_header(msg.get("Date"))[0]

        print(f"Subject: {subject}")
        print(f"From: {from_}")
        print(f"Date: {date}\n")
        try:
            date_string_cleaned = re.sub(r'\([^)]*\)', '', date).strip()
            # Convert the input date and time to a datetime object
            dt_object = datetime.strptime(date_string_cleaned, "%a, %d %b %Y %H:%M:%S %z")


            # Convert the datetime object to the target time zone (Uzbekistan Time)
            uzbek_timezone = pytz.timezone('Asia/Tashkent')
            converted_dt = dt_object.astimezone(uzbek_timezone)

            # Format the converted datetime object
            formatted_date = converted_dt.strftime("%H:%M, %d-%b, %Y")
        except:formatted_date = date
        print("\n__________________")


        message = str(subject).strip()
        if "Alert: New symbol:" in message:
            ticker, algorithm = message.replace("Alert: New symbol:", '').replace("was added to", '%%').split("%%")
            asyncio.run(main(algorithm, formatted_date, ticker=ticker))
        else:
            tickers, algorithm = message.replace("Alert: New symbols:", '').replace("were added to", '%%').replace("""were
         added to""", "%%").split("%%")
            tickers = tickers.split(',')
            asyncio.run(main(algorithm, formatted_date, tickers=tickers))
            continue


    time.sleep(10)


# Close the IMAP connection
imap.logout()
