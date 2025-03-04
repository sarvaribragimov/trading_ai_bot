import asyncio

from beatifulsoup import get_column_inner_data
from data.utils import options_expirations, long_put_volume, long_put_volume_text, long_call_volume, \
    long_call_volume_text, put_call_ratios_text, getbarcharttableinfo
from utils.db_api import database


def alltext(ticker,comp_info,market_value,market_task,insider,invest):
    text = (f"Quyidagi malumotlarni o`rganib chiq va “stock tiker”   kompaniyasi uchun ijobiy yoki salbiy xabar ekanligini aniqla va javobing 800 ta belgidan oshmasin"
            f"kompaniya malumotlari: {market_value} {market_task}\n\n"
            f"“Stock tiker”  kompaniyasining so'ngi yangiliklari:{comp_info}   \n\n"
            f"Insayderlar savdosi:   {insider}\n\n "
            f"Instutsional transaction: {invest}")

    return text


async def getapi(ticker):
    # await qilinishi kerak bo'lgan funksiya chaqirilishi
    # barchart = await getbarcharttableinfo(ticker)
    # q = await get_column_inner_data(ticker)

    # async funksiyalarni parallel ravishda ishlatish
    col = await asyncio.gather(get_column_inner_data(ticker))
    # col = await get_column_inner_data(ticker)
    # Natijalarni qo'shish
    print(col)
    print(type(col))  #
    # print(barchart+q)
    # db = database.BarchartTokenTable()
    # data =  await db.search_by_status(status='TOKEN')
    # cookie = data['cookie']+data['cookie2']+data['cookie3']
    # data=long_put_volume(ticker,cookie, data['token'])
    # data=long_call_volume(ticker,cookie, data['token'])
    # data=options_expirations('NVDA',cookie, data['token'])
    # if '401' not in data:
    #     text = put_call_ratios_text(data)
    #     print(text)
    # else:
    #     print(data)

asyncio.run(getapi('NVDA'))

