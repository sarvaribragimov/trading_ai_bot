from environs import Env

env = Env()
env.read_env()
production =True
pro = env.bool('PRODUCTION',default=True)
BOT_TOKEN = env.str("BOT_TOKEN") if pro else env.str("BOT_TOKEN")
SUPER_ADMIN = env.int("SUPER_ADMIN")
ADMINS = env.list("ADMINS") + [SUPER_ADMIN]
GOOGLE_API_KEY = env.str('GOOGLE_API_KEY')
MISTRAL_API_KEY = env.str('MISTRAL_API_KEY')
LESSONS_CHAT_ID=-1002573513671
sender_email = "alerts@thinkorswim.com"
CHATGPT_API_KEY=env.str('CHATGPT_API_KEY')

imap_server = 'imap.gmail.com'
imap_port = 993
imap_username = 'lapasovsardorbek2000@gmail.com'
imap_password = 'iafikcrfprpclwuo'
free_days = 15
usage_limit_daily = 2000
admin_username = "@Sardor_Lapasov"
reffered_users = 5
refferals = {
	5: 0.5,
	10: 1,
	30: 3
}

main_lang = 'uz'
langs = {
    "🇺🇿O'zbekcha": 'uz',
	"🇬🇧English": 'en',
    "🇷🇺Русский": 'ru',
}

signals_type = {
    'DAY':"💹 Day Trading",
	'SWING':"📈 Swing Trading",
    'INVESTING':"💰 Investing",
	"ALL":"🔄 All"
}


class Texts:
	def __init__(self, lang):
		self.lang = lang or main_lang
	def promoteadminbot(self):
		return {
			'uz': "Kanalni qo'shishdan avval botni unga admin qilib tayinlang!",
			'en': "Promote your bot an admin of channel before adding a channels list!",
			'ru': "Прежде чем добавлять канал, сделайте своего бота администратором!"

		}[self.lang]
	def appendchannel(self):
		return {
			'uz': "{} qo'shildi",
			'en': "{} added",
			'ru': "{} добавлен"

		}[self.lang]
	def deletechannel(self):
		return {
			'uz': "{} kanal o'chirildi",
			'en': "{} channel deleted",
			'ru': "{} канал удален"

		}[self.lang]
	def enterchannel_id(self):
		return {
			'uz': "Kanal id sini yuboring: ",
			'en': "Send channel id:",
			'ru': "Отправить идентификатор канала:"

		}[self.lang]
	def beforemustsubscribe(self):
		return {
			'uz': "❌Avval quyidagi kannallarga ubuna bo'ling!👇",
			'en': "❌Subscribe to the following channels first!👇",
			'ru': "❌Сначала подпишитесь на следующие каналы!👇"

		}[self.lang]
	def subscibed(self):
		return {
			'uz': "🛎Obuna bo'ldim",
			'en': "🛎I subscribed",
			'ru': "🛎Я подписался"

		}[self.lang]
	def didntfoundticker(self):
		return {
			'uz': '❌Aksiya topilmadi',
			'en': "❌The stock not found",
			'ru': "❌Акция не найдена"

		}[self.lang]
	def ticker_complience(self):
		return {
			'uz': '🌙Aksiya halolligini tekshirish',
			'en': "🌙Check the compliance of the stock",
			'ru': "🌙Проверьте честность продвижения"

		}[self.lang]


	def completly_started(self):
		return {
			'uz': '✨Siz botdan {} gacha bepul foydalanish huquqiga ega bo`ldingiz',
			'en': "✨You have been granted the right to use the bot for free up to {}",
			'ru': "✨Вам предоставлено право бесплатного использования бота до {}"

		}[self.lang]
	def usage_limited_text(self):
		return {
			'uz': f"🥺Siz kunlik {usage_limit_daily} ta limitlangan so'rovni amalga oshirdingiz",
			'en': f"🥺You have made {usage_limit_daily} limit request",
			'ru': f"🥺Вы отправили запрос на ограничение в размере {usage_limit_daily}."

		}[self.lang]

	def main(self):
		return {
			'uz': '🔝Bosh sahifa',
			'en': "🔝Main page",
			'ru': "🔙Главная страница"

		}[self.lang]
	def orqaga(self):
		return {
			'uz': '🔙Orqaga',
			'en': "🔙Back",
			'ru': "🔙Назад"

		}[self.lang]
	def phone_number(self):
		text = {
		'uz': 'Telefon raqamingizni ulashish uchun: "📲Raqamni yuborish" tugmasini bosing',
		'en': 'To share your phone number: Click the "📲Send" button',
		'ru': "Чтобы поделиться своим номером телефона: нажмите кнопку 📲Отправить"
		}
		return text[self.lang]

	def phone_number_button(self):
		text = {
		'uz': "📱Yuborish",
		'en': "📱Send",
		'ru': "📱 Отправить"
		}
		return text[self.lang]

	def choose(self):
		text = {
		'uz': 'Tanlang👇',
		'ru': "Выбирайте👇",
		'en': "Choose👇"
		}
		return text[self.lang]
	def user_sections(self):
		text = {
			'uz': [
				"📈Signal turlari",
				"📝O'z savolingizni yo'llang",
				"🔍Aksiya tikerini kiriting",
				"📚 Darslar",
				"🇺🇿Til sozlamalari"
			],
			'en': [
				"📈Signal types",
				"📝Send your question",
				"🔍Enter stock ticker",
				"📚 Уроки",
				"🇺🇿Language Settings"
			],
			'ru': [
				"📈Типы сигналов",
				"📝Отправьте свой вопрос",
				"🔍Введите биржевой тикер",
				"📚 Lessons",
				"🇺🇿Настройки языка"
			]
		}
		return text[self.lang]
	def refferal_successful_text(self):
		text = {
			'uz': "Siz <b>{}</b> ni botga taklif qildingiz💫",
			'en': "You invited <b>{}</b> to the bot💫",
			'ru': "Вы пригласили <b>{}</b> в бот💫",
		}
		return text[self.lang]
	def changed_access_time_via_refferal(self):
		text = {
			'uz': "Siz taklif qilgan foydalanuvchilar soni {} ga yetdi.\nVa siz {} gacha botdan foydalanish huquqiga ega bo'ldingiz.",
			'en': "The number of users you have invited has reached {}.\nAnd you have access to the bot up to {}.",
			'ru': "Число приглашенных вами пользователей достигло {}.\nИ у вас есть доступ к боту до {}.",
		}
		return text[self.lang]
	def send_question(self):
		text = {
			'uz': "Bu bo`limda siz o`zingizni qiziqtirgan xohlagan savolingizga suniy intelekt orqali javob olasiz. \nSavolingizni yo`llang!",
			'en': "In this section, you will receive an answer to any question you are interested in through artificial intelligence. \nSend your question!",
			'ru': "В этом разделе вы получите ответ на любой интересующий вас вопрос посредством искусственного интеллекта.Отправьте свой вопрос!"
		}
		return text[self.lang]

	def signals_type(self):
		text = {
			'uz': f"📊 O‘z savdo uslubingizga mos signalni tanlang:\n\n " 
				  f"💹 **<b>Day Trading</b>**\n  — Qisqa muddatli kunlik savdolar.\n  — Faqat bugungi kun uchun amal qiladi.\n" 
				  f" — Har bir savdodan 📈 <b>0.7%</b> daromad ko‘zlanadi.\n\n"
				  f"📈 **<b>Swing Trading</>**\n  — 2-10 kunlik qisqa muddatli savdolar.\n "
				  f"— Har bir savdodan 📈 <b>4%</b> daromad ko‘zlanadi.\n\n"
				  f"💰 **<b>Investing</b>** \n — 2 haftadan 3 oyga qadar uzoq muddatli savdolar.\n"
				  f"— Har bir savdodan 📈 <b>10%</b> daromad ko‘zlanadi.\n\n"
				  f"🔄 **<b>All</b>**\n  — Barcha signallarni olish.",
			'en': "Choose Signals Based on Your Trading Style!",
			'ru': "Выбирайте сигналы в соответствии с вашим стилем торговли!"
		}
		return text[self.lang]

	def send_ticker(self):
		return {
			'uz': 'Quyida siz aksiya tikerini $ belgisi bilan kiriting! Masalan: $AAPL yoki $aapl ko`rinishida.👇',
			'en': "Below you enter the stock ticker with the $ sign! For example: $AAPL or $aapl.👇",
			'ru': "Ниже вы вводите тикер акции со знаком $! Например: $AAPL или $aapl.👇"

		}[self.lang]
	def waiting_generate(self):
		return {
			'uz': '♻️ 1 daqiqa Kuting javob tayyorlanmoqda...',
			'en': "♻️Please wait for a minute...",
			'ru': "♻️Пожалуйста, дождитесь ответа..."

		}[self.lang]
	def choose_one(self):
		return {
			'uz': "Savollardan birini tanlang👇",
			'en': "Choose one of the questions👇",
			'ru': "Выберите один из вопросов👇"
		}[self.lang]
	def premium_sections(self):
		return {
			'uz': ['🟢Obuna bolish', '📲Referal tizimi'],
			'en': ['🟢Subscribe', '📲Referral System'],
			"ru": ['🟢Подписаться', '📲Реферальная система']
		}[self.lang]
	def your_refferal_link(self):
		return {
			'uz': "Sizning referralingiz orqali botga qo'shilgan har bir foydalanuvchi uchun botdan 1 hafta bepul foydalanishni qo'lga kiritasiz!\n🙋‍♂️Taklif qilingan foydalanuvchilar soni {} ta\n✨Sizning refferal havolangiz👇",
			'en': 'For each user who joins the bot through your referral, you will get 1 week of free use of the bot!\n🙋‍♂️Number of invited users {} \n✨Your referral link👇',
			"ru": 'За каждого пользователя, присоединившегося к боту по вашему рефералу, вы получаете 1 неделю бесплатного использования бота!\n🙋‍♂️Количество приглашенных пользователей {} \n✨Ваша реферальная ссылка👇'
		}[self.lang]

	def refferal_link(self):
		return {
			'uz': 'Botga o\'ting va tradingda AI yordamchiga ega bo\'ling\n👉🏻 https://t.me/{}',
			'en': 'Go to Bot and get an AI assistant in trading\n👉🏻 https://t.me/{}',
			"ru": 'Перейдите в Bot и получите ИИ-помощника в торговле\n👉🏻 https://t.me/{}'
		}[self.lang]
	def choose_tariff(self):
		return {
			'uz': 'Quyidagi tariflardan birini tanlang',
			'en': 'Choose one of the rates below',
			"ru": 'Выберите один из тарифов ниже'
		}[self.lang]
	def choose_tariff_to_using(self):
		return {
			'uz': '💸Botdan foydalanishda davom etish uchun tariflar bilan tanishing👇\nYoki {} tomonidan berilgan bir martalik <b><i>token</i></b>ni yuboring',
			'en': '💸Read the rates to continue using the bot👇\nOr send a one-time <b><i>token</i></b> issued by {}',
			"ru": '💸Прочитайте тарифы, чтобы продолжить использование бота👇\nИли отправьте одноразовый <b><i>токен</i></b>, выпущенный {}'
		}[self.lang]
	def tariff_info(self):
		return {
			'uz': '<b>{}</b>  obuna narxi <b>{}</b> so\'m\nMaxsus token olish uchun '+ admin_username +' ga yozing',
			'en': '<b>{}</b>  subscription price <b>{}</b> sum\nTo get a special token, write to ' + admin_username,
			"ru": '<b>{}</b>  стоимость подписки <b>{}</b> sum\nЧтобы получить специальный токен, напишите ' + admin_username
		}[self.lang]
	def enter_token_text(self):
		return {
			'uz': '👨🏻‍💻Admin bergan tokenni kiritish',
			'en': '👨🏻‍💻Enter the token given by the admin',
			'ru': '👨🏻‍💻Введите токен, предоставленный администратором',
		}[self.lang]
	def ignore_token_text(self):
		return {
			'uz': """Afsuski, ushbu TOKEN raqam bizning  bazamizda mavjud emas yoki siz allaqachon ishlatilgan TOKEN raqamni kiritmoqdasiz.""",
			'en': 'Unfortunately, this TOKEN number is not available in our database, or you are entering a TOKEN number that has already been used.',
			'ru': 'К сожалению, этот номер ТОКЕНА недоступен в нашей базе данных, или вы вводите номер ТОКЕНА, который уже использовался.',
		}[self.lang]
	def admin_sections(self):
		return {
			'uz':  [
				"💰Tariflar boshqaruvi",
				"📲Foydalanuvchilarga xabar yuborish",
				"📊Statistika",
				"📃Mavjud tokenlar",
				"♻️Yangi generatsiya qilish",
				"🗑Foydalanuvchini o'chirish",
				"👨🏻‍💻Kanallar boshqaruvi",
				"Darslarni yuklash",
				"Signal turlari",
				"Barchart token kiritish",
				"🕐Stock signal oralig'ini belgilash",
				"🕑🕒Barcha intervallar",
			],
			'en': [
				"💰Rate Management",


				"📲Send messages to users",
				"📊Statistics",

				"📃Available Tokens",
				"♻️Making a new generation",
				"🗑Delete User",
				"👨🏻‍💻Channel Management",
				"Darslar",
				"Signal turlari",
				"Barchart token kiritish",
				"🕐Stock signal oralig'ini belgilash",
				"🕑🕒Barcha intervallar",
			],
			'ru': [
				"💰Управление тарифами",
				

				"📲Отправлять сообщения пользователям",
				"📊Статистика",
				
				"📃Доступные токены",
				"♻️Создаем новое поколение",
				"🗑Удалить пользователя",
				"👨🏻‍💻Управление каналом",
				"Darslar",
				"Signal turlari",
				"Barchart token kiritish",
				"🕐Stock signal oralig'ini belgilash",
				"🕑🕒Barcha intervallar",
			]
		}[self.lang]
	def send_post_to_rek(self):
		return {
			'uz': "Kontentni yuboring",
			'en': "Send content",
			'ru': "Отправить контент",
		}[self.lang]
	def count_users(self):
		return {
			'uz': "📊Foydalanuvchilar soni: {}",
			'en': "📊Number of users: {}",
			'ru': "📊Количество пользователей: {}",
		}[self.lang]
	def send_user_id(self):
		return {
			'uz': "Foydalanuvchi ID sini kiriting👇",
			'en': "Enter User ID👇",
			'ru': "Введите идентификатор пользователя👇",
		}[self.lang]
	def enter_tokens_count(self):
		return {
			'uz': "Yaratmoqchi bo'lgan tokenlaringiz miqdorini kiring",
			'en': "Enter the amount of tokens you want to generate",
			'ru': "Введите количество токенов, которое вы хотите сгенерировать",
		}[self.lang]
	def enter_true_count(self):
		return {
			'uz': "Son kiriting!\nMisol uchun <i>20</i>",
			'en': "Enter a number!\nFor example <i>20</i>",
			'ru': "Введите число!\nНапример, <i>20</i>",
		}[self.lang]
	def admin_panel_text(self):
		return {
			'uz': "Admin panel",
			'en': "Admin panel",
			'ru': "Панель администратора",
		}[self.lang]
	def not_founded_user_text(self):
		return {
			'uz': "Foydalanuvchi topilmadi!",
			'en': "User not found!",
			'ru': "Пользователь не найден!",
		}[self.lang]
	def user_deleted_successfully(self):
		return {
			'uz': "Muvaffaqiyatli o'chirildi✅",
			'en': "Deleted successfully✅",
			'ru': "Удален успешно✅",
		}[self.lang]
	def sent_users_count(self):
		return {
			'uz': "{} ta foydalanuvchilarga yuborildi:)",
			'en': "Sent to {} users:)",
			'ru': "Отправлено {} пользователям:)",
		}[self.lang]
	def enter_tariff_name(self):
		return {
			'uz': "Tarifga nom bering misol uchun \n<i>6 oylik</i>",
			'en': "Name the tariff, for example \n<i>6 months</i>",
			'ru': "Назовите тариф, например \n<i>6 месяцев</i>",
		}[self.lang]
	def tariff_name_price(self):
		return {
			'uz': "Tarif nomi: <b>{} ({} kun)</b>\nNarxi: <b>{} so'm</b>",
			'en': "Tariff name: <b>{} ({} day)</b> \nPrice: <b>{} sum</b>",
			'ru': "Название тарифа: <b>{} ({} день)</b>\nЦена: <b>{} сум</b>",
		}[self.lang]
	def enter_days_count(self):
		return {
			'uz': "Kun miqdorini kiriting misol uchun 6 oy uchun <i>180</i> kun👇",
			'en': "Enter the number of days, for example <i>180</i> days for 6 months👇",
			'ru': "Введите количество дней, например <i>180</i> дней для 6 месяцев👇",
		}[self.lang]
	def enter_only_numbers(self):
		return {
			'uz': "Kun miqodori faqat raqamlardan iborat bo'lishi kerak\nIltimos <i>180  360</i> kabi sonlardan foydalaning!",
			'en': "The amount of days must be numbers only\nPlease use numbers like <i>180 360</i>!",
			'ru': "Количество дней должно быть только числами.\nПожалуйста, используйте цифры, например <i>180 360</i>!",
		}[self.lang]
	def enter_tariff_price(self):
		return {
			'uz': "Oxirgi bosqich: Tarif narxini kiriting misol uchun \n<i>1200</i>\nSo'm so'zi shart emas 👇",
			'en': "Last step: Enter the price of the tariff, for example \n<i>1200</i>\nSoum is not necessary 👇",
			'ru': "Последний шаг: Введите стоимость тарифа, например \n<i>1200</i>\nСум не обязательно 👇",
		}[self.lang]
	def appended_tariff_text(self):
		return {
			'uz': '<i>"{}"</i> tarifi muvaffaqiyatli qo\'shildi',
			'en': '<i>"{}"</i> tariff added successfully',
			'ru': 'Тариф <i>"{}"</i> успешно добавлен',
		}[self.lang]
	def enter_token_by_admin(self):
		return {
			'uz': 'Tokenni kiriting👇',
			'en': 'Enter the token👇',
			'ru': 'Введите токен👇',
		}[self.lang]

	def changed_access_time(self):
		return {
			'uz': "✅Bot uchun ruxsat {}.{}.{} gacha uzaytirildi",
			'en': '✅Bot permission extended to {}.{}.{}',
			'ru': '✅Разрешение бота расширено до {}.{}.{}',
		}[self.lang]

questions = "kompaniyasini tahlil qilib ber hozir savdoga kirsam boladimi hafta oxirigacha qaysi narxga kotarilib berishi mumkin."
answers='s'
def answer_que(lang):
	answer_que_uz = {}
	for a, b in zip(questions, answers):answer_que_uz[b] = a
	return answer_que_uz
answers_ques = {
	'uz': answer_que('uz'),
	'en': answer_que('en'),
	'ru': answer_que('ru')
}

orqaga = "🔙 Orqaga"
searched = """
Apple Inc AAPL:NASDAQ- Open0.00- Day High0.00- Day Low0.00- Prev Close185.04- 52 Week High199.62- 52 Week High Date12/14/23- 52 Week Low143.90- 52 Week Low Date03/02/23Key Stats- Market Cap2.861T- Shares Out15.46B- 10 Day Average Volume57.33M- Dividend0.96- Dividend Yield0.52%- Beta1.31- YTD % Change-3.89KEY STATS- Open0.00- Day High0.00- Day Low0.00- Prev Close185.04- 52 Week High199.62- 52 Week High Date12/14/23- 52 Week Low143.90- 52 Week Low Date03/02/23- Market Cap2.861T- Shares Out15.46B- 10 Day Average Volume57.33M- Dividend0.96- Dividend Yield0.52%- Beta1.31- YTD % Change-3.89RATIOS/PROFITABILITY- EPS (TTM)6.43- P/E (TTM)28.79- Fwd P/E (NTM)28.54- EBITDA (TTM)130.109B- ROE (TTM)154.27%- Revenue (TTM)385.706B- Gross Margin (TTM)45.03%- Net Margin (TTM)26.16%- Debt To Equity (MRQ)145.80%EVENTS- Earnings Date05/02/2024(est)- Ex Div Date02/09/2024- Div Amount0.24- Split Date-- Split Factor-

 |Previous Close|187.15|Open|185.77|Bid|0.00 x 900|Ask|185.45 x 900|Day's Range|183.51 - 186.21|52 Week Range|143.90 - 199.62|Volume|Avg. Volume|53,167,470|Market Cap|2.857T|Beta (5Y Monthly)|1.31|PE Ratio (TTM)|28.82|EPS (TTM)|6.42|Earnings Date|May 02, 2024 - May 06, 2024|Forward Dividend & Yield|0.96 (0.52%)|Ex-Dividend Date|Feb 09, 2024|1y Target Est|201.08Apple (AAPL) recently launched its AR/VR headset Vision Pro. Spatial Dynamics Co-CEO Cathy Hackl joins Yahoo Finance Live to discuss Vision Pro’s potential, describing it as the technology's “early days.” Hackl called the Vision Pro “a really advanced piece of consumer technology” that combines computing and visuals into the physical world, unlike full virtual reality. However, with a $3,500 price tag, she says it doesn’t offer “$3,500 worth of value... just yet.” Adoption will "take time," Hackl notes, as app content catches up to the capabilities. She sees it as "a progression," but the lack of consumer awareness of spatial technology makes the costs hard to justify for most. For more expert insight and the latest market action, click here to watch this full episode of Yahoo Finance Live. Editor's note: This article was written by Angel Smith Click here to watch the full interview on the Yahoo Finance YouTube page or you can watch this full episode of Yahoo Finance Live here.If you don't know what to buy next, poach a pick or two from the world's best-known stock picker.(Bloomberg) -- Apple Inc.’s longest-serving senior industrial designer is leaving the company, marking the near-complete turnover of a team once led by Jony Ive.Most Read from BloombergMusk Says Putin Can’t Lose in Ukraine, Opposes Senate BillStanChart Weighs Break Up of Corporate, Investment BankPutin Seeks Revenge on a World Order He Once Wanted to JoinLyft Corrects Earnings Margin Gain to 50 Basis Points From 500Retail Traders Are Losing Billions in India’s Booming Options MarketBart Andre, w

 2024 Proxy MaterialsView the Proxy StatementView the Form 10-K2024 Annual Meeting of ShareholdersApple will host the 2024 Annual Meeting of Shareholders on February 28, 2024 at 9:00 am P.T. in a virtual format. You can access the meeting by visiting www.virtualshareholdermeeting.com/AAPL2024 on the day of the meeting. The bank, broker, or other organization that holds your Apple shares will be issuing proxy materials to you that will include a unique control number. You’ll need that unique control number to access the meeting, and vote during the meeting. The record date for the meeting is January 2, 2024. Additional details about the meeting and the matters to be voted on are available in our proxy statement.

 - Ukrainian military says it sank a Russian landing ship in the Black Sea- Barron's Meta’s Zuckerberg Blasts Apple Headset, OpenAI Founder Leaves, and Other Tech News Today- Defense Minister Subianto leads in early count of Indonesia’s presidential race- Amazon, British American Tobacco fined in Italy over smoking-device ads- Barron's Tesla Stock Is Down 26% in 2024. This Number Explains Why.- Heineken shares slump as customers balk at brewer’s hiked prices- Barron's Bitcoin Tears Higher, Bucking Inflation Data Pressure on the S&P 500- Interest rates have bottomed due to surging government spending, Gundlach says- ‘I felt humiliated’: Is it emasculating to allow a woman to pick up the dinner check?- Barron's Jeff Bezos Sold Another $2 Billion of Amazon Stock. Why It May Be Good Timing.to be replacedApple Inc.$185.64|Close|Chg|Chg %|$185.04|-2.11|-1.13%Partner CenterYour Watchlists|SymbolCompany|PriceChg/Chg %|Recently Viewed TickersOverviewAAPL OverviewKey Data- Open $185.77- Day Range 183.51 - 186.21- 52 Week Range 143.90 - 199.62- Market Cap $2.89T- Shares Outstanding 15.44B- Public Float 15.43B- Beta 1.20- Rev. per Employee $2.396M- P/E Ratio 28.79- EPS $6.43- Yield 0.52%- Dividend $0.24- Ex-Dividend Date Feb 9, 2024- Short Interest 99.24M 01/31/24- % of Float Shorted 0.64%- Average Volume 53.4MPerformance|5 Day||1 Month||3 Month||YTD||1 Year|Analyst RatingsRecent NewsThe Best Warren Buffett Stocks to Buy With $3,000 Right NowThese 3 Companies Are Shattering Quarterly RecordsThe Next Disney? 3 Entertainment Stocks That Investors Shouldn’t Ignore.Royce Investment Partners' Annual Letter: The Dog That Didn't BarkRoyce Investment Partners' Annual Letter: The Dog That Didn't BarkApple Inc.Apple, Inc. engages in the design, manufacture, and sale of smartphones, personal computers, tablets, wearables and accessories, and other varieties of related services. It operates through the following geographical segments: Americas, Europe, Greater China, Japan, and Rest of Asia Pacific. The Americas segment includes North and South America. The Europe segment consists of European countries, as well as India, the Middle East, and Africa. The Greater China segment comprises China, Hong Kong, and Taiwan. The Rest of Asia Pacific segment includes Australia and Asian countries. Its products and services include iPhone, Mac, iPad, AirPods, Apple TV, Apple Watch, Beats products, AppleCare, iCloud, digital content stores, streaming, and licensing services. The company was founded by Steven Paul Jobs, Ronald Gerald Wayne, and Stephen G. Wozniak in April 1976 and is headquartered in Cupertino, CA.Competitors|Name|Chg %|Market Cap|Microsoft Corp.|$3.09T|Alphabet Inc. Cl C|$1.84T|Alphabet Inc. Cl A|$1.84T|Amazon.com Inc.|$1.79T|Meta Platforms Inc.|$1.2T|Samsung Electronics Co. Ltd.|₩493.38T|Samsung Electronics Co. Ltd. Pfd. Series 1|₩493.38T|Sony Group Corp.|¥17.66T|Dell Technologies Inc. Cl C|$61.18B|HP Inc.|$28.43B

 PRESS RELEASE June 5, 2023Introducing watchOS 10, a milestone update for Apple WatchDelivering redesigned apps, a new Smart Stack, additional watch faces, new cycling and hiking features, and tools to support mental healthCUPERTINO, CALIFORNIA Apple today previewed watchOS 10, bringing Apple Watch users a fresh approach to quickly view information with redesigned apps, a new Smart Stack to show relevant widgets right when they’re needed, and delightful new watch faces. New metrics, Workout Views, and Bluetooth connectivity for power meters, speed sensors, and cadence sensors arrive for cyclists, while new Compass Waypoints and Maps capabilities further help hikers. The Mindfulness app offers additional tools to support mental health. watchOS 10 is available as a developer beta today, and will be available as a free software update this fall.“watchOS is the world’s most advanced wearable operating system, and it has redefined how people all over the world think of what a watch can do,” said Kevin Lynch, Apple’s vice president of Technology. “watchOS 10 is a major milestone and an energizing new approach for Apple Watch, introducing a fresh new design for quickly viewing information, delightful new watch faces, new features for cyclists and hikers, and important tools for health.”New Design Language and NavigationWith watchOS 10, redesigned apps provide more information at a glance, and there are new ways to navigate and quickly access content.“With watchOS 10, we’ve redesigned the interface, allowing users to experience Apple Watch like never before,” said Alan Dye, Apple’s vice president of Human Interface Design. “The update gives users the information that matters most to them at a glance, simplified navigation, and a new visual language that takes full advantage of the Apple Watch display. We’re also introducing the Smart Stack, offering quick access to proactive and relevant information, right from the watch face.”Apple Watch apps, including Weather, Stocks, Home, Maps, Messages, World Clock, and others, now utilize more of the Apple Watch display for more glanceable information. The Activity app on Apple Watch and the Fitness app on iPhone make tracking daily movement even easier with more details, improvements to sharing, a redesigned trophy case, and Apple Fitness+ trainer tips.A new Smart Stack contains widgets that display timely information that adapts to the user’s context and can be revealed with a simple turn of the Digital Crown from any watch face. For example, at the beginning of the day, Weather will show the forecast, or, when traveling, the Smart Stack will show boarding passes from Wallet. Calendar and Reminders will reshuffle to the top to display upcoming meetings or tasks, and apps that are running, such as Podcasts, will also move up so they are readily available. Smart Stack also enables users to enjoy a beautiful watch face, like Portraits, while still offering a way to quickly access information they care about.Developers can also use the new design language to update their apps. For example, Streaks now utilizes the entire display to easily show progress and access tasks, the NBA app makes keeping up with a favorite team even more compelling with team colors and new game details, and with Waterllama’s redesign, users can quickly glance at their hydration from the last seven days with just a turn of the Digital Crown.Control Center is now accessible using the side button, making it easy to quickly open it at any time, over any app. A double-click of the Digital Crown reverts back to any apps used recently.New Watch FaceswatchOS 10 introduces two new artistic and joyful watch faces: Palette and Snoopy. The Palette face depicts time in a wide variety of colors using three distinct overlapping layers, and as the time changes, the colors on the display also shift.Additionally, the beloved comic strip Peanuts comes to life on Apple Watch with a new watch face featuring Snoopy and Woodstock. The characters interact and play with the watch hands, react to the weather conditions in the area, or even get active when the user does a workout.CyclingApple Watch is a great device for cyclists, with features including automatic Workout reminders, calorimetry for e-biking, and Fall Detection. watchOS 10 takes this popular activity even further with advanced new metrics, views, and experiences.When a cycling workout is started from Apple Watch in watchOS 10, it will automatically show up as a Live Activity on iPhone and, when tapped, will utilize the full screen. Workout Views, such as Heart Rate Zones, Elevation, Race Route, Custom Workouts, and a new Cycling Speed view, have been optimized for the display size of iPhone, which can be mounted to a bike for convenient, easy viewing during a ride.Apple Watch can now automatically connect to Bluetooth-enabled cycling accessories, such as power meters, speed sensors, and cadence sensors. This enables brand-new metrics, including cycling power (watts) and cadence (RPM), and additional Workout Views, including Power Zones. Bluetooth connection is supported for Indoor and Outdoor cycling workouts, as well as GymKit.New algorithms combining sensor data from Apple Watch and connected power meters can estimate Functional Threshold Power (FTP), the highest level of cycling intensity that a rider could theoretically maintain for an hour. Using FTP, Apple Watch calculates personalized Power Zones, used to easily see the current zone and track how long is spent in each, which is an effective and popular way of improving performance.HikingThe Compass app on Apple Watch is a helpful tool for exploring the great outdoors. With watchOS 10, Compass automatically generates two new waypoints: A Last Cellular Connection Waypoint will estimate the last place with cellular reception, which may be useful for checking messages or making a call. In case of emergencies, a Last Emergency Call Waypoint will estimate where on the route their device had the last connection to any available carrier’s network so that an emergency call can be made.When preparing routes, a new Elevation view uses altimeter data, offering a three-dimensional view of saved waypoints. And starting in the U.S., Apple Maps displays a new topographic map featuring contour lines, hill shading, elevation details, and points of interest. Users can also search for nearby trails and trailheads, with place cards that include detailed information, like trail length, type, and difficulty.Mental HealthMental health is as important as physical health, and research shows that reflecting on state of mind can help build emotional awareness and resilience. With the Mindfulness app in watchOS 10, users can discreetly and conveniently log their momentary emotions and daily moods. Users can turn the Digital Crown to scroll through engaging, multidimensional shapes to choose how they are feeling, select what is having the biggest impact on them, and describe their feelings.In the Health app in iOS 17 and iPadOS 17, users can see valuable insights to identify what might be contributing to their state of mind — whether it’s associations or lifestyle factors, like sleep or exercise. Additionally, depression and anxiety assessments often used in clinics are now easily accessible in the Health app and can help users determine their risk level, connect to resources available in their region, and create a PDF to share with their doctor.Vision HealthMyopia, or nearsightedness, is the leading cause of vision impairment globally. To reduce the risk of myopia, the International Myopia Institute recommends children spend at least 80-120 minutes a day outdoors. With watchOS 10, Apple Watch introduces the ability to measure time spent in daylight using the ambient light sensor. Users can view this information in the Health app on iPhone or iPad.Time spent in daylight can provide additional benefits to physical and mental health for all ages. And children who do not have their own iPhone can use Family Setup to pair their Apple Watch to their parent’s iPhone, giving parents visibility into the amount of time their kids are spending in daylight with Health Sharing.Viewing something like a device or a book too closely has also been documented as a myopia risk factor. The new Screen Distance feature uses the same TrueDepth camera that powers Face ID in iPad and iPhone to encourage users to move their device farther away after holding it closer than 12 inches for an extended period of time.When a device is locked with a passcode, Touch ID, or Face ID, all Health app data, including mental health and vision health data, is encrypted.1Additional watchOS 10 updates include:- NameDrop allows users to easily share contact information by bringing Apple Watch close to someone else’s iPhone. Apple Watch users can also use NameDrop by tapping the Share button in My Card in the Contacts app, or by tapping the My Card watch face complication, and then bringing Apple Watch face to face with someone else’s Apple Watch.2- Offline maps on iPhone provide access to turn-by-turn navigation, estimated time of arrival, places in Maps, and more while away from Wi-Fi or cellular services. These features can also be used on a paired Apple Watch that is in range of its companion iPhone.- Users can now initiate playback of a FaceTime video message and view it directly on Apple Watch. Additionally, Group FaceTime audio is now supported on Apple Watch.- The Medications app can send follow-up reminders if a medication hasn’t been logged 30 minutes after the scheduled time.- Apple Fitness+ introduces Custom Plans, a new way to receive a custom workout or meditation schedule based on day, duration, workout type, and more; Stacks, which allows users to select multiple workouts and meditations to do seamlessly back to back; and Audio Focus, which gives users the ability to prioritize the volume of the music or the trainers’ voices.EnterpriseApple Watch offers enterprise customers features to enhance productivity and safety in the office or in the field, such as hands-free communication and responding to notifications on the go, or Fall Detection on a job site. watchOS 10 introduces support for Mobile Device Management (MDM), enabling enterprise customers to remotely and centrally install apps and configure accounts on a fleet of devices, with features such as passcode enforcement, and configuring Wi-Fi and VPN settings. With this update, Apple Watch can further help improve employee wellness, productivity and health, and safety monitoring.APIs for Workout App DeveloperswatchOS 10 includes new APIs for workout app developers that will allow them to create compelling new experiences. The powerful motion sensors on both Apple Watch Series 8 and Apple Watch Ultra can detect rapid changes in velocity and acceleration, such as when swinging a golf club or a tennis racket. Now, developers will have access to this high-frequency motion data, so apps like SwingVision can analyze serve pronation, which is the twisting motion of the forearm, wrist, and hand, and Golfshot can detect small wrist movements to refine a golf swing.Popular coaching platforms such as TrainingPeaks can use a new API to create a Custom Workout that can be imported directly into the Workout app. App developers using HealthKit for workouts will be able to provide validated calories for golf workouts, as the variation between using a golf cart or walking on the green is now identified. Developers can also access speed, cadence, and power metrics for cycling, plus mirror workouts from Apple Watch to iPhone.AvailabilityThe developer beta of watchOS 10 is available to Apple Developer Program members at developer.apple.com starting today. A public beta will be available to watchOS users next month at beta.apple.com. watchOS 10 will be available this fall as a free software update for Apple Watch Series 4 or later paired with iPhone Xs or later, running iOS 17. Some features may not be available in all regions or all languages, or on all devices. Features are subject to change. For more information, visit apple.com/watchos/watchos-preview.Share articleMedia-Text of this article-Images in this article- This applies to all health information other than the user’s Medical ID.- NameDrop will be available on Apple Watch with a software update later this year.Press ContactsApple Media Helpline


"""