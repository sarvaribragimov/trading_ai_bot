from aiogram import types
from data import config
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from utils.db_api.database import DataBaseSql
from states.user import User
from aiogram.dispatcher import FSMContext
from keyboards.default.all import admin_menu


@dp.message_handler(commands="admin", chat_id=config.ADMINS,chat_type=types.ChatType.PRIVATE, state='*')
async def func(message: types.Message, state: FSMContext):
    id = message.from_user.id
    _user_data = await state.get_data()
    await message.answer("Admin panel", reply_markup=await admin_menu())
    await User.admin.set()

@dp.message_handler(CommandStart(), state='*', chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message):
    id = message.from_user.id
    db = DataBaseSql()
    user = await db.search_user(chat_id=id)
    if not user:
        await message.answer(config.start_text.format(message.from_user.full_name))
        await User.enter_code.set()
        return
    await message.answer(f"Xush kelibsiz, <b>{message.from_user.full_name}!</b>")
@dp.message_handler(content_types=['text'], state=User.enter_code, chat_type=types.ChatType.PRIVATE)
async def func(message: types.Message):
    id = message.from_user.id
    token = message.text
    db = DataBaseSql()
    if not await db.search(token=token):
        await message.answer(config.ignore_text)
        return
    await db.delete(token)

    await DataBaseSql().adduser(chat_id=id, name=message.from_user.full_name, access="unlimited")
    await dp.bot.copy_message(chat_id=id, from_chat_id= -1001596191086, message_id=779)
    # await message.answer("Tabriklaymiz, siz 'OPTIMUS ALGO' algoritmik signallar botiga rasman a'zo bo'ldingiz, ushbu video qo'llanma bilan tanishib chiqing")

    txt = f'✅ <code>{token}</code> orqali <b><a href="tg://user?id={id}">{message.from_user.full_name}</a> ({id})</b> botga qo\'shildi'
    for a in config.ADMINS:
        await dp.bot.send_message(chat_id=a, text=txt)


