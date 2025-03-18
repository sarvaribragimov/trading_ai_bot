import asyncio
import json

from data.utils import get_tashkent_time

# from chatgpt import openai
# from beatifulsoup import get_column_inner_data
# from data.get_company_info import insider_ransaction, is_halal, get_stock_info
# from data.utils import options_expirations, long_put_volume, long_put_volume_text, long_call_volume, \
#     long_call_volume_text, put_call_ratios_text, getbarcharttableinfo, get_openai_question
# from utils.db_api import database


# def alltext(ticker,comp_info,market_value,market_task,insider,invest):
#     text = (f"Quyidagi malumotlarni o`rganib chiq va “stock tiker”   kompaniyasi uchun ijobiy yoki salbiy xabar ekanligini aniqla va javobing 800 ta belgidan oshmasin"
#             f"kompaniya malumotlari: {market_value} {market_task}\n\n"
#             f"“Stock tiker”  kompaniyasining so'ngi yangiliklari:{comp_info}   \n\n"
#             f"Insayderlar savdosi:   {insider}\n\n "
#             f"Instutsional transaction: {invest}")
#
#     return text


# async def getapi(ticker):
#     co = await get_column_inner_data(str(ticker))
    # barchart = await getbarcharttableinfo(str(ticker))
    # col = str(co) + str(barchart)
    # ai_response = await openai(col)
    # print(co)


# async def test(ticker):
    # te = await getapi(ticker)
    # t = insider_ransaction('AMD')
    # print(t)
    # barchart = await getbarcharttableinfo(ticker)
    # print(barchart)


# asyncio.run(getapi('AMD'))

# file_path = "ishalal.json"
# with open(file_path, "r", encoding="utf-8") as file:
#     data = json.load(file)
#     stock_info = next((stock for stock in data if stock["Ticker"] == 'AAPL'), None)
#     # if stock_info is None:
#     print(stock_info['Compliance'])

# t = insider_ransaction('AMD')
# print(t)

# t = get_stock_info('COIN')
# print(t)
#
# t = get_openai_question('ru')
# print(t)
# async def main(ticker):
#     barchart = await getbarcharttableinfo(ticker)
#     co = await get_column_inner_data(ticker)
#     questions = str(co) + str(barchart)
#     print(questions)
# asyncio.run(main('coin'))



