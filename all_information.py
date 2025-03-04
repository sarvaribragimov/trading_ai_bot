from selenium.webdriver.common.devtools.v118.runtime import await_promise

from data.barchart import *
from data.insider_transaction import insider_ransaction
from data.investment import invest, get_invest
from data.utils import insider_text, investment_text
import requests
from bs4 import BeautifulSoup
import asyncio

from data.findvalue import tableinformation, extract_text_filter, companyinformation, findmarket
from data.utils import alltext

def get_column_inner_datasss(ticker):
    url = f"https://www.barchart.com/stocks/quotes/{ticker}/overview"
    url2 = f"https://www.barchart.com/stocks/quotes/{ticker}/news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        result = extract_text_filter(soup)
        results = findmarket(soup)
        market_value = result + results
        comp = companyinformation(soup)
        insider_ransaction(ticker)
        i = invest(ticker)
        d = alltext(ticker,comp,market_value)
        print(d)
    else:
        print(f"Xato: Sahifa yuklanmadi. Status kodi: {response.status_code}")
        return None
# ticker = "NVDA"
# data = get_column_inner_datasss(ticker)
# if data:
#     pass

def all_information(ticker):
    trans = transaction(ticker)
    # print(trans)
    volume = get_volume(ticker)
    percent = total_percent(ticker)
    print(percent)
    a = insider_text(trans,volume)
    # return volume

ticker = 'NVDA'
a = all_information(ticker)
print(a)

def investment(ticker):
    insider =  insider_ransaction(ticker)
    invest =  get_invest(ticker)
    d = investment_text(insider,invest)
    return d
# a = investment(ticker)
# print(a)