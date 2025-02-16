from utils.db_api import database
from loader import dp
from states.user import User
from datetime import datetime as dt
from data import config
from keyboards.inline.all import getTariffs
from aiogram import types
async def is_member_all_chats(_user_data):
    chat_id = _user_data['chat_id']
    lang = _user_data['lang']
    texts = config.Texts(lang)

    db = database.ChannelsTable()
    channels = await db.search(all=True)
    unfollowed = []
    for ch in channels:
        try:
            user = await dp.bot.get_chat_member(ch[0], chat_id)
            if user['status'] == "left":
                unfollowed.append(ch)
        except:
            pass
    if unfollowed:
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            *[
                types.InlineKeyboardButton(text=(await dp.bot.get_chat(ch[0]))['title'],
                url=(await dp.bot.create_chat_invite_link(chat_id=ch[0]))['invite_link'])
                for ch in unfollowed
            ]
        )
        m.add(types.InlineKeyboardButton(text=texts.subscibed(), callback_data='followed'))
        txt = texts.beforemustsubscribe()
        await dp.bot.send_message(chat_id=chat_id, text=txt, reply_markup=m)
        await User.confirm_joined.set()
        return False
    return True

async def is_granted(_user_data):
    db = database.UsersTable()
    chat_id = _user_data['chat_id']
    user = await db.search(chat_id)
    lang = _user_data['lang']
    texts = config.Texts(lang)
    date = user[2]
    today = dt.today()
    access = dt.strptime(date.split('.')[0], '%Y-%m-%d %H:%M:%S')
    if today <= access:
        return True
    await User.choose_tariff.set()
    txt = "\n".join([f"{tariff[0]} - {tariff[2]} so'm" for tariff in await database.TariffsTable().search(all=True)])
    await dp.bot.send_message(chat_id=chat_id, text=texts.choose_tariff_to_using().format(config.admin_username) + " " +  txt, reply_markup=await getTariffs())
    return False