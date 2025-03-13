
from aiogram import executor
from dotenv import dotenv_values
from gemini import generate

config = dotenv_values('.env')

# Bot token can be obtained via https://t.me/BotFather
TOKEN = config.get('BOT_TOKEN')
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.message import ParseMode


bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

def hbold(text):
	return f"<b>{text}</b>"
def to_markdown(text):
	return text.replace('*$', '>')


@dp.message_handler(commands=['start'])
async def command_start_handler(message: types.Message) -> None:

	await message.answer(f"Salom, {hbold(message.from_user.full_name)}!\nSavolingizni berishingiz mumkin", parse_mode='html')
	await message.answer("🚀")
@dp.message_handler(content_types=['text'])
async def func(message: types.Message):
	q = message.text + " in english"
	msg = await message.answer("Kuting✍️...")
	parts = generate(q)
	await dp.bot.delete_message(chat_id=message.from_user.id, message_id=msg.message_id)
	# response = await model.generate_content_async(q)
	if parts:
		print(parts)
		text = ' '.join(i['text'] for i in parts)
		try:
			await message.answer(to_markdown(text), parse_mode=types.ParseMode.MARKDOWN)
		except:
			await message.answer(to_markdown(text))



@dp.message_handler()
async def echo_handler(message: types.Message) -> None:
	try:
		await message.send_copy(chat_id=message.chat.id)
	except TypeError:
		await message.answer("Nice try!")



if __name__ == "__main__":
	print("Running")
	executor.start_polling(dp)

