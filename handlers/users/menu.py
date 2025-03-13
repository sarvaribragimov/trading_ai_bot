import asyncio
import json
import time

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from chatgpt import openai
from loader import dp
from handlers.users import functions as funcs
from aiogram.dispatcher import FSMContext
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
	print('message handler 1')
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
	print('signals type')
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


	elif message.text == user_sections[5]: #lang
		await message.answer(message.text, reply_markup=cities(config.langs.keys()))
		await User.lang.set()

@dp.message_handler(content_types=['text'], state=User.send_question, chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message, state: FSMContext):
	print('message handler 2')
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
	# start_time = time.process_time()
	q = message.text
	if lang != 'en':
		q = funcs.trans(q, 'en')
	await message.answer_chat_action(types.ChatActions.TYPING)
	parts = await generate(q)
	if parts:
		text = ' '.join(i['text'] for i in parts)
		if lang != 'en':
			text = funcs.trans(text, lang)
		# process_time = time.process_time() - start_time
		# text += f"\n{process_time}"
		await dp.bot.delete_message(chat_id=message.from_user.id, message_id=msg.message_id)
		try:
			await message.answer(funcs.to_markdown(text), parse_mode=types.ParseMode.MARKDOWN)
		except:
			await message.answer(funcs.to_markdown(text))


@dp.message_handler(content_types=['text'], state=User.send_ticker, chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message, state: FSMContext):
	print('message handler 3')
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
	ticker = message.text
	# await state.update_data(ticker=ticker, titles=config.answers_ques[lang])
	await message.answer(text='❇️Javobingiz tayyorlanmoqda iltimos kuting ...')
	ai_response = await openai(f'{ticker} kompaniyasini tahlil qilib ber hozir savdoga kirsam boladimi hafta oxirigacha qaysi narxga kotarilib berishi mumkin.')
	file_path = "ishalal.json"
	with open(file_path, "r", encoding="utf-8") as file:
		data = json.load(file)
		print(f'Ticker{ticker[1:]}=type{type(ticker)}')
		stock_info = next((stock for stock in data if stock["Ticker"] == str(ticker[1:])), None)
		print(stock_info)
		await message.answer(text=f'{stock_info["Compliance"]} {ai_response}')
	await message.answer(texts.choose(), reply_markup=menu_markup(lang))
	await User.menu.set()


@dp.message_handler(content_types=['text'], state=User.choose_question)
async def bot_start(message: types.Message, state: FSMContext):
	print('message handler 4')
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
	print('message handler 5')
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
	print('message =', message)
	try:
		trading_options = config.signals_type
		print('Available options:', trading_options)
		for status, text in trading_options.items():
			if message.text == text:
				print('status =', status)
				if status:
					update_result = await database.UsersTable().update_status(chat_id=message.from_user.id, status=status)
					print(update_result)
					if update_result:
						await message.answer(text=f'Siz {message.text} tanladingiz")')
					else:
						await message.answer(text='Status yangilanishida xatolik yuz berdi.')
				else:
					await message.answer(
						text='Hech qanday natija topilmadi. Iltimos, mavjud tugmalardan birini tanlang.',
						reply_markup=None
					)
	except Exception as e:
		await message.answer(text=f'Xatolik haqida @sarvar_developer ga murojat qiling update_signals_status error {e}')
