from aiogram import types

from drawer import Setup
from utils.db_api.database import DataBaseSql
from aiogram.dispatcher import FSMContext
from states.user import User
from data import config
from loader import dp,bot

from keyboards.default.all import admin_menu
from .functions import list_tokens, generate_token

@dp.message_handler(chat_id=config.ADMINS, chat_type=types.ChatType.PRIVATE, state=User.admin, content_types=['text'])
async def func(message: types.Message, state: FSMContext):
    id = message.from_user.id
    _user_data = await state.get_data()
    q = message.text
    if q == config.admin_sections[0]:
        await message.answer(await list_tokens())
    elif q == config.admin_sections[1]:
        await message.answer("Yaratmoqchi bo'lgan tokenlaringiz miqdorini kiring👇", reply_markup=types.ReplyKeyboardRemove())
        await User.enter_count.set()
    elif q == config.admin_sections[2]: # remove user
        await message.answer("Foydalanuvchi ID sini kiriting👇",
                             reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton(text=config.orqaga)))
        await User.remove_user.set()
    elif q == config.admin_sections[3]:
        await message.answer("test kuting👇",
                             reply_markup=None)
        await User.test.set()


@dp.message_handler(chat_id=config.ADMINS, chat_type=types.ChatType.PRIVATE, state=User.test, content_types=['text'])
async def testfunc(message: types.Message, state: FSMContext):
    print('1')
    count = message.text
    media_group = []
    web = Setup(ticker='AMD')
    web.init()
    path = web.screenshot()
    print(path)
    print('2')
    web.close_browser()
    media_group.append(
        types.InputMediaPhoto(media=open(path, 'rb')),
    )
    text = f"Aksiya tikerlari: AMD"
    message = await bot.send_media_group(chat_id=config.main_user, media=media_group)
    await bot.edit_message_caption(chat_id=config.main_user, message_id=message[0].message_id, caption=text)
    await User.admin.set()

@dp.message_handler(chat_id=config.ADMINS, chat_type=types.ChatType.PRIVATE, state=User.enter_count, content_types=['text'])
async def func(message: types.Message, state: FSMContext):
    print('3dv')
    count = message.text
    if not count.isdigit():
        await message.answer("Son kiriting!\nMisol uchun <i>20</i>")
        return
    count = int(count)
    for i in range(count):
        token = await generate_token()
        await DataBaseSql().addtoken(token=token)
    await message.answer(await list_tokens(), reply_markup=await admin_menu())
    await User.admin.set()

@dp.message_handler(chat_id=config.ADMINS, chat_type=types.ChatType.PRIVATE, state=User.remove_user, content_types=['text'])
async def func(message: types.Message, state: FSMContext):
    print('asdf')
    user_id = message.text.strip()
    if user_id == config.orqaga:
        await message.answer("Admin panel", reply_markup=await admin_menu())
        await User.admin.set()
        return
    db = DataBaseSql()
    user = await db.search_user(chat_id=user_id)
    if not user:
        await message.answer("Foydalanuvchi topilmadi!")
        return
    await db.delete_user(user_id)
    await message.answer("Muvaffaqiyatli o'chirildi✅", reply_markup=await admin_menu())
    await User.admin.set()



