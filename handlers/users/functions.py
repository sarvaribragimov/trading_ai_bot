import asyncio
import os
import time

from loader import database as tickers_database, names, tickers, data_ishalal, bot

from data import config
from aiogram import types
from utils.db_api import database
import re
import string
from random import choices
import json
from deep_translator import GoogleTranslator, detection
from keyboards.default.all import menu_markup

from utils.db_api.database import UsersTable, TokensTable
from string import ascii_letters
from random import choices
from datetime import datetime as dt
from states.user import User
import pandas as pd


def renderData(data):
    txt = ""
    keys = data.keys()
    if "Ticker" in keys:
        txt += f'<b>Ticker:</b> ${data["Ticker"]}\n'
    if "Company" in keys:
        name = data['Company'].split('-')[-1]
        txt += f'<b>Company:</b> {name}\n'
    if "Sector" in keys:
        txt += f'<b>Sector:</b> {data["Sector"]}\n'
    if "Industry" in keys:
        txt += f'<b>Industry:</b> {data["Industry"]}\n'
    if "Sub-Industry" in keys:
        txt += f'<b>Sub-Industry:</b> {data["Sub-Industry"]}\n'
    if "Result" in keys:
        txt += f'<b>Result Muslim Exchange:</b> {data["Result"]} '
    if "Stars" in keys:
            txt += f' {data["Stars"] * "🎖"}\n'
    if "AAOIFI" in keys:
            txt += f'   <b>AAOIFI:</b> {"✅" if data["AAOIFI"] == "PASS" else "❌"}{data["AAOIFI"]}\n'
    if "S&P" in keys:
        txt += f'   <b>S&P:</b> {"✅" if data["S&P"] == "PASS" else "❌"}{data["S&P"]}\n'
    if "DJIM" in keys:
        txt += f'   <b>DJIM:</b> {"✅" if data["DJIM"] == "PASS" else "❌"}{data["DJIM"]}\n'
    if "FTSE" in keys:
        txt += f'   <b>FTSE:</b> {"✅" if data["FTSE"] == "PASS" else "❌"}{data["FTSE"]}\n'
    if "MSCI" in keys:
        txt += f'   <b>MSCI:</b> {"✅" if data["MSCI"] == "PASS" else "❌"}{data["MSCI"]}\n'

    if data["Ticker"] in data_ishalal.keys():
        compliance = data_ishalal[data["Ticker"]]
        txt += f'<b>Result Islamicly:</b> {"✅" if compliance.strip() == "Halal" else "❌"}{compliance}\n'
    return txt
def getData(ticker=None, name=None):
    if ticker and ticker in tickers:
        indexOfData = tickers.index(ticker)

        data = tickers_database[indexOfData]

        return renderData(data)

    if name and name in names:
        indexOfData = names.index(name)
        data = tickers_database[indexOfData]
        return renderData(data)
    return 0

async def db_to_excel(id, caption):
    users = await database.UsersTable().search(all=True)
    chat_ids = []
    names = []
    languages = []
    access_dates = []
    reffers = []
    last_usages = []

    for u in users:
        chat_id = u[0]
        name = None
        lang = u[1]
        access = u[2]
        reffer_by = u[3]
        last_usage = None
        user = await database.ExtraTable().search(chat_id=chat_id)
        if user:
            name = user[1]
            last_usage = user[2]
        chat_ids.append(chat_id)
        names.append(name)
        languages.append(lang)
        access_dates.append(access)
        reffers.append(reffer_by)
        last_usages.append(last_usage)
    data = {
        'chat_id': chat_ids,
        'Full Name': names,
        'Language': languages,
        'Access Date': access_dates,
        'Reffer By': reffers,
        'Last Usage': last_usages
    }
    df = pd.DataFrame(data)
    output = f"{dt.now().second}.xlsx"
    df.to_excel(output)
    await bot.send_chat_action(id, types.ChatActions.UPLOAD_DOCUMENT)
    await bot.send_document(chat_id=id,document=open(output, 'rb'), caption=caption)
    await asyncio.sleep(10)
    os.remove(output)






async def is_limited(_user_data):
    chat_id = _user_data['chat_id']
    lang = _user_data['lang']
    texts = config.Texts(lang)
    extrausers = database.ExtraTable()
    extra_user = await extrausers.search(chat_id=chat_id)
    today = dt.today().strftime("%Y-%m-%d")
    last_usage = dt.strptime(extra_user[2], "%Y-%m-%d").strftime("%Y-%m-%d")
    usage_count = int(extra_user[3])
    if today == last_usage and usage_count >= config.usage_limit_daily:
        await bot.send_message(chat_id, texts.usage_limited_text(), reply_markup=menu_markup(lang))
        await User.menu.set()
        return True
    if today != last_usage:
        await database.ExtraTable().adduser(chat_id=chat_id, last_usage=today)
        await database.ExtraTable().adduser(chat_id=chat_id, usage_count=0)
    if usage_count < config.usage_limit_daily:
        await database.ExtraTable().adduser(chat_id=chat_id, usage_count=usage_count + 1)
    return False

async def generate_token():
    letters = ascii_letters + "1234567890"
    token = "".join(choices(letters, k=9))
    while await TokensTable().search(token=token):
        token = "".join(choices(letters, k=9))
    return token

async def list_tokens(days):
    db = TokensTable()
    tokens = await db.search(days=days)
    txt = f"<b>Umumiy tokenlar soni: {len(tokens)} ta</b>\n"
    count = 1
    for token in tokens:
        txt += f"{count}. <code>{token[0]}</code> \n"
        count += 1
    return txt
def to_markdown(text):
  text = text.replace("**", '@@').replace('*', "@@").replace("@@", "**")
  return text



async def password_render():
    letters = string.ascii_letters + string.digits + string.punctuation
    return "".join(choices(letters, k=8))
async def checkMember(user_id, lang):
    texts = config.Texts(lang)
    db = database.UsersTable()
    channels = await db.search(all=True)
    markup = types.InlineKeyboardMarkup(row_width=1)
    number = 1
    for ch in channels:
        ch = ch[0]
        try:
            chat = await bot.get_chat(ch)
            d = await bot.get_chat_member(ch, user_id)
        except:
            db = database.UsersTable()
            await db.delete(ch)
            continue
        if d['status'] == "left":
            txt = await texts.channel_number()
            markup.add(
                types.InlineKeyboardButton(text=txt.format(number), url=f"{chat['invite_link']}")
            )
            number += 1
    if markup['inline_keyboard']:
        markup.add(types.InlineKeyboardButton(text=await texts.confirm_joined(), callback_data='confirm_joined'))
    return markup
async def check_number(number):
    number = str(number)
    if len(number) != 13:
          return False
    validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"
    return re.match(validate_phone_number_pattern, number)
async def is_same_locations(_user_data):
    return _user_data['lat'] == _user_data['lat1'] and _user_data['long'] == _user_data['long1']


# def detect(text):
#     try:
#         return translator.detect(text)
#     except Exception as e:
#         print(e)
#         return detect(text)

def trans(text, dest='en'):
    try:
        # src = detect(text)
        # print(src, type(src))
        # if src != dest:
        return GoogleTranslator(target=dest).translate(text)
        # return translator.translate(text, lang_tgt=dest).text
        # return text
    except Exception as e:
        print(e)
        return trans(text, dest)


