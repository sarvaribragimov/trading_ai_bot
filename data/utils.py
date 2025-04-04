from utils.db_api import database
from datetime import datetime
import pytz
from bot import  dp

def investment_text(insider,invest):
    text = (f"{insider}  investment: {invest} ")
    return text


def alltext(ticker,comp_info,market_value,market_task,invest,insider):
    text = (f"${ticker} {market_value} {market_task}"
            f"kompaniya so'ngi yangiliklarini:{comp_info}"
            f"Instutsional transaction:{invest}\n"
            f"insider lar savdosi {insider}")
    return text


import requests


def options_expirations(ticker,cookie: str, token: str):
    url = "https://www.barchart.com/proxies/core-api/v1/options-expirations/get"
    headers = {
        "Cookie": cookie,
        "x-xsrf-token": token,
        "method":"GET",
        "authority": "www.barchart.com",
        "priority":"u=1, i",
        "scheme": "https",
        "accept-encoding":"gzip, deflate, br, zstd",
        "accept-language":"en-US,en;q=0.9,uz;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1129.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }
    params = {
        "fields": "expirationDate,putVolume,callVolume,totalVolume,putCallVolumeRatio,symbolCode",
        "symbol": ticker,
        "meta":"field.shortName,field.type,field.description",
        "page": 1,
        "limit": 1,
        "raw": 0,
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return f"token eskirdi: {response.status_code} details {response.text}"

def put_call_ratios_text(data):
    text = ""
    for index,item in enumerate(data):
        text += (f"{item['expirationDate']} sanasigacha ushbu kompaniyada {item['putVolume']} ta Put option, va {item['callVolume']}"
              f" ta call option bor ekan Put/call ratio {item['putCallVolumeRatio']} ekan ")

    return text


def long_put_volume(ticker,cookie: str, token: str):
    url = "https://www.barchart.com/proxies/core-api/v1/options/get"
    headers = {
        "Cookie": cookie,
        "x-xsrf-token": token,
        "method":"GET",
        "authority": "www.barchart.com",
        "priority":"u=1, i",
        "scheme": "https",
        "accept-encoding":"gzip, deflate, br, zstd",
        "accept-language":"en-US,en;q=0.9,uz;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1129.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }
    params = {
        "fields": "expirationDate,netDebit,strikePrice,volume",
        "baseSymbol": ticker,
        "orderBy": "volume",
        "orderDir": "desc",
        "expirationDate": "nearest",
        "eq(symbolType,put)": "",
        "page": 1,
        "limit": 4,
        "raw": 0
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return f"token eskirdi: {response.status_code} details {response.text}"

def long_put_volume_text(data):
    text = ""
    for index,item in enumerate(data):
        text += (f"{index+1}) {item['expirationDate']} sanasigacha {item['strikePrice']} USD ga narxi tushishiga {item['netDebit']}"
              f" dan {item['volume']} ta put option bor  ")

    return text


def long_call_volume(ticker: str,cookie: str, token: str):
    url = "https://www.barchart.com/proxies/core-api/v1/options/get"
    headers = {
        "Cookie": cookie,
        "x-xsrf-token": token,
        "method":"GET",
        "authority": "www.barchart.com",
        "priority":"u=1, i",
        "scheme": "https",
        "accept-encoding":"gzip, deflate, br, zstd",
        "accept-language":"en-US,en;q=0.9,uz;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1129.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }
    params = {
        "fields": "expirationDate,netDebit,strikePrice,volume",
        "baseSymbol": ticker,
        "orderBy": "volume",
        "orderDir": "desc",
        "expirationDate": "nearest",
        "eq(symbolType,call)": "",
        "page": 1,
        "limit": 5,
        "raw": 0
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return f"token eskirdi: {response.status_code} details {response.text}"

def long_call_volume_text(data):
    text = ""
    for index,item in enumerate(data):
        text += (f"{index+1}) {item['expirationDate']} sanasigacha {item['strikePrice']} USD ga narxi ko'tarilishiga {item['netDebit']}"
              f" dan {item['volume']} ta call option bor  ")

    return text


async def getbarcharttableinfo(ticker):
    try:
        db = database.BarchartTokenTable()
        data = await db.search_by_status(status='TOKEN')
        if data:
            cookie = data['cookie'] + data['cookie2'] + data['cookie3']
            result_text = ""
            longputvolume = long_put_volume(ticker, cookie, data['token'])
            if '401' not in longputvolume:
                result_text += long_put_volume_text(longputvolume)
            else:
                result_text += "\n⚠️ Long Put Volume: 401 Unauthorized\n"
            longcallvolume = long_call_volume(ticker, cookie, data['token'])
            if '401' not in longcallvolume:
                result_text += f"\n📈 Long Call Volume:\n{long_call_volume_text(longcallvolume)}\n"
            else:
                result_text += "\n⚠️ Long Call Volume: 401 Unauthorized\n"
            optionsexpirations = options_expirations(ticker, cookie, data['token'])
            if '401' not in optionsexpirations:
                result_text += f"\n📆 Options Expirations:\n{put_call_ratios_text(optionsexpirations)}\n"
            return result_text.strip()
    except Exception as e:
        await dp.bot.send_message(chat_id='523886206', text=f'getbarcharttableinfo error {e}')

def get_openai_question(lang='uz'):
    if lang == 'uz':
        text = ("sen bilan kompaniylarni kelgusida yurishi haqida prognozlar qilamiz, men malumot aytaman sen "
                "esa xulosa qiberishing kerak boladi,    fundamental holati, optionlar holati yangiliklari insayderlar "
                "va instutsional investorlar savdolariga asoslanib sotib olish kerakmi yoki sotish kerakmi, "
                "sotib olish kerak bolsa qaysi narxgacha yurib berishi mumkinligi haqida xulosa bergin. "
                "javoblar ozbek tilida bolsin. quyida malumotlar:")
    elif lang == 'en':
        text = ("We will make forecasts about the future performance of companies with you, I will give you information"
                " and you will have to draw conclusions, based on the fundamental situation,"
                " the news of the options situation, the trading of insiders and institutional investors,"
                " whether to buy or sell, and if you should buy, at what price it can go. Answers should be in English."
                "Below is the information:")
    else:
        text = ("Мы будем делать с вами прогнозы относительно будущих результатов деятельности компаний, "
                "я предоставлю информацию, а вам нужно будет сделать выводы, исходя из фундаментальной ситуации,"
                " новостей о ситуации на рынке опционов, торговли инсайдеров и институциональных инвесторов,"
                " покупать или продавать, и если да, то по какой цене это может произойти. Пусть ответы будут на "
                "русском языке. информация ниже:")
    return text



def get_tashkent_time():
    tashkent_tz = pytz.timezone("Asia/Tashkent")
    return datetime.now(tashkent_tz).time()  # Hozirgi Toshkent vaqti


