import asyncio
import json
import time

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from beatifulsoup import get_column_inner_data
from chatgpt import openai
from data.get_company_info import insider_ransaction, get_stock_info
from data.utils import getbarcharttableinfo, get_openai_question
from loader import dp
from handlers.users import functions as funcs
from aiogram.dispatcher import FSMContext

from screnshot import Setup
from states.user import User
from data import config
from utils.db_api import database
from datetime import datetime as dt
from keyboards.default.all import menu_markup, informations_key, cities, lessons_btn
from gemini import generate
from keyboards.inline.all import getTariffs
from .userpermissons import is_granted, is_member_all_chats





@dp.message_handler(content_types=['text'], state=User.menu, chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message, state: FSMContext):
	chat_id = message.from_user.id
	_user_data = await state.get_data()
	lang = _user_data['lang']
	texts = config.Texts(lang)
	today = dt.today()
	extrausers = database.ExtraTable()
	if not await extrausers.search(chat_id=chat_id):
		await extrausers.adduser(chat_id=chat_id, name=message.from_user.full_name, last_usage=today.strftime("%Y-%m-%d"), usage_count=0)
	if not await is_member_all_chats(_user_data) or not await is_granted(_user_data):
		return
	user_sections = texts.user_sections()
	if message.text == user_sections[0]:# signals type
		await message.answer(texts.signals_type(), reply_markup=cities(config.signals_type.values()))
		await User.type.set()
	if message.text == user_sections[1]:# send_question
		await message.answer(texts.send_question(), reply_markup=cities([texts.orqaga()]))
		await User.send_question.set()
	elif message.text == user_sections[2]: #send_ticker
		await message.answer(texts.send_ticker(), reply_markup=cities([texts.orqaga()]))
		await User.send_ticker.set()
	elif message.text == user_sections[3]: #lessons
		db = database.LessonsTable()
		lessons = await db.get_lessons()
		await User.lessons_btn.set()
		await message.answer(message.text, reply_markup=lessons_btn(lessons))
	elif message.text == user_sections[4]: #lang
		await message.answer(message.text, reply_markup=cities(config.langs.keys()))
		await User.lang.set()

@dp.message_handler(content_types=['text'], state=User.send_question, chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message, state: FSMContext):
	_user_data = await state.get_data()
	lang = _user_data['lang']
	texts = config.Texts(lang)
	chat_id = message.from_user.id
	if await funcs.is_limited(_user_data):return
	if message.text == texts.orqaga():
		await message.answer(texts.choose(), reply_markup=menu_markup(lang))
		await User.menu.set()
		return
	msg = await message.answer(texts.waiting_generate())
	q = message.text
	if lang != 'en':
		q = funcs.trans(q, 'en')
	await message.answer_chat_action(types.ChatActions.TYPING)
	parts = await openai(q)
	if parts:
		text = parts
		if lang != 'en':
			text = funcs.trans(text, lang)
		await dp.bot.delete_message(chat_id=message.from_user.id, message_id=msg.message_id)
		try:
			await message.answer(funcs.to_markdown(text), parse_mode=types.ParseMode.MARKDOWN)
		except:
			await message.answer(funcs.to_markdown(text))


@dp.message_handler(content_types=['text'], state=User.send_ticker, chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message, state: FSMContext):
	_user_data = await state.get_data()
	lang = _user_data['lang']
	texts = config.Texts(lang)
	if message.text == texts.orqaga():
		await message.answer(texts.choose(), reply_markup=menu_markup(lang))
		await User.menu.set()
		return
	if not "$" in message.text:
		await message.answer("❌" + texts.send_ticker())
		return
	ticker = str(message.text[1:])
	await message.answer(text='❇️Javobingiz tayyorlanmoqda iltimos kuting ...')
	res = await database.BarchartExpired().get_max_token()

	if res:
		if res['status'] == 'ACTIVE':
			barchart = await getbarcharttableinfo(ticker)
			if '401' in barchart:

				await dp.bot.send_message(chat_id='523886206',text="token expired")
				await dp.bot.send_message(chat_id='6866199714',text="token expired")
				await database.BarchartExpired().add_token(status='INACTIVE')
				await message.answer(texts.choose(), reply_markup=menu_markup(lang))
				await User.menu.set()
			else:
				co = await get_column_inner_data(ticker)
				q = get_openai_question(lang)
				questions = str(q) + str(co) + str(barchart)
				ai_response = await openai(questions)
				web = Setup(ticker=str(ticker))
				web.init()
				path, price = web.screenshot()
				web.close_browser()
				text = f"<b>Aksiya tikeri:</b> {ticker}\n<b>Islamicly:</b> {get_stock_info(ticker)}\n" \
					   f"<b>Narxi:</b> {price[6:]}\n"
				with open(path, 'rb') as photo:
					if len(text) + len(ai_response) > 1000:
						await dp.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text)
						await dp.bot.send_message(chat_id=message.chat.id, text=f"<b>Taxlil</b> {ticker}\n {ai_response}")
					else:
						await dp.bot.send_message(chat_id=message.chat.id, photo=photo,text=f"{text} {ai_response}")
				await message.answer(texts.choose(), reply_markup=menu_markup(lang))
				await User.menu.set()
		else:
			await message.answer(text="iltimos keyinroq urinib ko'ring")
			await User.menu.set()

	else:
		await message.answer(text="iltimos keyinroq urinib ko'ring")
		await User.menu.set()

@dp.message_handler(content_types=['text'], state=User.choose_question)
async def bot_start(message: types.Message, state: FSMContext):

	_user_data = await state.get_data()
	lang = _user_data['lang']
	texts = config.Texts(lang)
	if await funcs.is_limited(_user_data): return
	ticker = _user_data['ticker'].replace('$', '').upper()
	titles = _user_data['titles']
	if message.text == texts.ticker_complience():
		txt = funcs.getData(ticker=ticker)
		if txt == 0:
			await message.answer(texts.didntfoundticker())
			return
		m = cities([texts.ticker_complience()] + list(titles.keys()) + [texts.main()])
		await message.answer(funcs.to_markdown(txt), reply_markup=m, reply=True)
		return
	elif message.text == texts.main():
		await message.answer(texts.choose(), reply_markup=menu_markup(lang))
		await User.menu.set()
		return

	answer = message.text
	if not answer in titles.keys():
		return
	question = titles[answer]
	del titles[answer]
	await state.update_data(titles=titles)
	q = question.format(ticker)
	msg = await message.answer(texts.waiting_generate())
	await message.answer_chat_action(types.ChatActions.TYPING)
	parts = await generate(q)
	if parts:
		text = ' '.join(i['text'] for i in parts)
		if lang != 'en':
			text = funcs.trans(text, lang)
		await dp.bot.delete_message(chat_id=message.from_user.id, message_id=msg.message_id)
		m = cities([texts.ticker_complience()] + list(titles.keys()) + [texts.main()])
		try:
			await message.answer(funcs.to_markdown(text), parse_mode=types.ParseMode.MARKDOWN, reply_markup=m, reply=True)
		except:
			await message.answer(funcs.to_markdown(text), reply_markup=m, reply=True)



@dp.message_handler(content_types=['text'], state=User.premium, chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message, state: FSMContext):

	id = message.from_user.id
	_user_data = await state.get_data()
	lang = _user_data['lang']
	texts = config.Texts(lang)
	premium_sections = texts.premium_sections()
	if message.text == texts.main():
		await message.answer(texts.choose(), reply_markup=menu_markup(lang))
		await User.menu.set()
		return
	elif message.text == premium_sections[0]:#subscribe
		await message.answer(text=texts.choose_tariff(), reply_markup=await getTariffs())
		await User.choose_tariff.set()
	elif message.text == premium_sections[1]:
		count = (await database.UsersTable().search(reffer_by=id))[0]
		await message.answer(texts.your_refferal_link().format(count))
		await message.answer(texts.refferal_link().format(f"{(await dp.bot.get_me())['username']}?start={id}"), disable_web_page_preview=True)


@dp.message_handler(content_types=['text'], state=User.type, chat_type=types.ChatType.PRIVATE)
async def update_signals_status(message: types.Message, state: FSMContext):
	try:
		trading_options = config.signals_type
		_user_data = await state.get_data()
		lang = _user_data['lang']
		texts = config.Texts(lang)
		for status, text in trading_options.items():
			if message.text == text:
				if status:
					update_result = await database.UsersTable().update_status(chat_id=message.from_user.id, status=status)
					if update_result:
						await message.answer(text=f'Siz {message.text} tanladingiz")')
						await message.answer(texts.choose(), reply_markup=menu_markup(lang))
						await User.menu.set()
					else:
						await message.answer(text='Status yangilanishida xatolik yuz berdi.')
				else:
					await message.answer(
						text='Hech qanday natija topilmadi. Iltimos, mavjud tugmalardan birini tanlang.',
						reply_markup=None
					)
	except Exception as e:
		await message.answer(text=f'Xatolik haqida @sarvar_developer ga murojat qiling update_signals_status error {e}')
