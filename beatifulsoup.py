import asyncio
import json
import requests
from bs4 import BeautifulSoup
import httpx

from data.get_company_info import extract_text_filter, companyinformation, findmarket, insider_ransaction, get_invest
from data.utils import alltext, getbarcharttableinfo


# async def get_column_inner_data(ticker: str):
#     try:
#         url = f"https://www.barchart.com/stocks/quotes/{ticker}/overview"
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36"
#         }
#
#         async with httpx.AsyncClient() as client:
#             response = await client.get(url, headers=headers)
#
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#
#             # Barcha funksiyalar async bo‘lgani uchun to‘g‘ridan-to‘g‘ri await qilamiz
#             text_filter_task = extract_text_filter(soup)
#             market_task = findmarket(soup)
#             comp_info_task = companyinformation(soup)
#             insider_task = insider_ransaction(ticker)
#             invest_task = get_invest(ticker)
#
#             # Paralel ishlatish
#             text_filter_result, market_result, comp_info_result, insider_result, invest_result = await asyncio.gather(
#                 text_filter_task, market_task, comp_info_task, insider_task, invest_task
#             )
#
#             d = alltext(ticker, comp_info_result, text_filter_result, market_result, insider_result, invest_result)
#             return d
#         else:
#             return f"get_column_inner_data error: {response.status_code}"
#
#     except Exception as e:
#         return f"get_column_inner_data error: {e}"
#
async def get_column_inner_data(ticker:str):
    try:
        url = f"https://www.barchart.com/stocks/quotes/{ticker}/overview"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_filter_task = extract_text_filter(soup)
            market_task = findmarket(soup)
            comp_info = companyinformation(soup)
            insider = insider_ransaction(ticker)
            invest = get_invest(ticker)
            # Barcha funksiyalarni parallel ishlatamiz
            text_filter_result, market_result, comp_info_result,insider,invest = await asyncio.gather(
                text_filter_task, market_task, comp_info,insider,invest
            )
            d = alltext(ticker, comp_info_result, text_filter_result, market_result,insider,invest)
            # if isinstance(d, dict):
            #     d = json.dumps(d, ensure_ascii=False)  # Dictionary bo'lsa, stringga aylantiramiz
            # elif isinstance(d, list):
            #     d = "\n".join(map(str, d))
            # elif not isinstance(d, str):
            #     d = str(d)
            return str(d)
        else:
            print(f"get_column_inner_data error: {response.status_code}")
            return 'Malumot topilmadi'
    except Exception as e:
        return f"get_column_inner_data error: {e}"

# asyncio.run(get_column_inner_data('AAPL'))
