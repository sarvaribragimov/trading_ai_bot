import json
import re

import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

from datetime import datetime, timedelta

async def extract_text_filter(soup):
    ng_init = soup.find('div', class_='page-title')['data-ng-init']
    json_data = ng_init.split('init(')[1].rstrip(')')
    data = json.loads(json_data)
    lastPriceExt = data.get('lastPriceExt')
    percentChangeExt = data.get('percentChangeExt')
    lastPrice = data.get('lastPrice')
    percent_change = data.get('percentChange')
    session_date = data.get('sessionDateDisplayLong')
    text = f"joriy narxi: {lastPrice} ({percent_change}) pre-market: {lastPriceExt} ({percentChangeExt}) {session_date} "

    return text

async def findmarket(soup): #barchart.com fundamentals analize text
    market_cap = soup.find("span", text="Market Capitalization, $K")
    sales = soup.find("span", text="Annual Sales, $")
    income = soup.find("span", text="Annual Income, $")
    if market_cap:
        value = market_cap.find_next_sibling("span", class_="right").text.strip()
        value2 = sales.find_next_sibling("span", class_="right").text.strip()
        value3 = income.find_next_sibling("span", class_="right").text.strip()
        info = f"Bozor qiymati $K :{value},Daromadi $:{value2},Sof foydasi $:{value3}"
        return info
    else:
        return "Qiymat topilmadi!"


async def totalpercent(soup): #barchart.com total percent table info
    print('1')
    tds = soup.find_all("td")
    texts = [td.get_text() for td in tds]
    percentages = []
    for text in texts:
        percentages.extend(re.findall(r'[-+]?\d+\.\d+%', text))
    print(percentages)

async def companyinformation(soup): #barchart.com company information
    titles = [a.text.strip() for a in soup.find_all('a', class_='story-link')]
    meta_info = [meta.text.strip() for meta in soup.find_all('span', class_='story-meta')]
    excerpts = [p.text.strip() for p in soup.find_all('p', class_='story-excerpt')]
    info = ""
    for i in range(len(titles)):
        if i < 3:
            info += f"{i+1} {titles[i]}\n"
            info += f"{meta_info[i]}\n"
            info += f"{excerpts[i]}\n"
    return info


def tableinformation(soup): #barchart.com company monthly report information
    print('11111111111')
    rows = soup.find_all("div", class_="_grid_groups")
    print(rows)
    for row in rows:
        print(row.text.strip())




async def insider_ransaction(ticker):
    try:
        ticker = str(ticker)
        url = f"http://openinsider.com/search?q={ticker}"
        today = datetime.today()
        one_month_ago = (today - timedelta(days=30)).strftime('%Y-%m-%d')
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="tinytable")
        if table:
            rows = table.find_all("tr")[1:]  # Sarlavhani tashlab ketamiz
            info = ""
            for idx,row in enumerate(rows):
                cols = row.find_all("td")
                if cols:
                    date_cell = cols[1]  # trade date
                    insider_name = cols[4].text.strip()
                    trade_type = cols[6].text.strip()
                    price = cols[7].text.strip()
                    total_price = cols[11].text.strip()
                    date_time_str = date_cell.text.strip()
                    parsed_date = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
                    trade_date = parsed_date.strftime("%Y-%m-%d")
                    if one_month_ago <= trade_date:
                        text = f"{idx+1}. {trade_date} sanasida {ticker} aksiyasini {insider_name} insayderi {price} dan jami {total_price}lik aksiyani {trade_type} qildi."
                        info += text + "\n"
                else:
                    return  "malumot topilmadi"
            return info.strip()
        else:
            return "Jadval topilmadi."
    except Exception as e:
        print(e)


async def invest(ticker):
    url = f"https://www.marketbeat.com/stocks/NASDAQ/{ticker}/institutional-ownership/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "❌ Saytdan ma'lumot olishda xatolik yuz berdi."
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if not table:
        return "❌ Jadval topilmadi."
    thead = table.find("thead")
    if not thead:
        return "❌ Jadval ichida <thead> topilmadi."
    original_headers = [th.get_text(strip=True) for th in thead.find_all("th")]
    try:
        market_value_index = original_headers.index("Market Value")
        date_index = original_headers.index("Reporting Date")
        company_index = original_headers.index("Major Shareholder Name")
        shares_index = original_headers.index("Shares Held")
        change_index = original_headers.index("Quarterly Change in Shares")
    except ValueError:
        return "❌ Kerakli ustun topilmadi."

    tbody = table.find("tbody")
    if not tbody:
        return "❌ Jadval ichida <tbody> topilmadi."
    rows = tbody.find_all("tr")
    # Natijalarni saqlash
    filtered_data = []
    for row in rows:
        cols = row.find_all("td")
        cols = [col.get_text(strip=True) for col in cols]
        if len(cols) == len(original_headers):  # Ustunlar soni to‘g‘ri bo‘lishi kerak
            market_value_str = cols[market_value_index]
            # "$1.38M" formatidagi qiymatni son ko‘rinishiga o‘tkazamiz
            if market_value_str.startswith("$"):
                value = market_value_str[1:-1]  # "$" belgisi va oxirgi harfni olib tashlaymiz
                multiplier = market_value_str[-1]  # "M" yoki "B" ni olish
                try:
                    numeric_value = float(value) * (1e6 if multiplier == "M" else 1e9 if multiplier == "B" else 1)
                    # Agar qiymat 100M dan katta bo‘lsa, natijalarga qo‘shamiz
                    if numeric_value > 100e6:
                        filtered_data.append({
                            "date": cols[date_index],
                            "company": cols[company_index],
                            "shares": cols[shares_index],
                            "market_value": market_value_str,
                            "change": cols[change_index]
                        })
                except ValueError:
                    continue  # Agar raqamga o‘tkazib bo‘lmasa, o‘tkazib yuboramiz
    return filtered_data
async def get_invest(ticker):
    t = await invest(ticker)
    if t:
        info=""
        for i, record in enumerate(t, start=1):
            text = (f"{i}) {record['company']} kompaniyasi {record['date']} sanasida {record['shares']} aksiyaga egalik qiladi,"
                    f"jami {record['market_value']} summa kiritgan. Oxirgi chorakda aksiyalarini sonini {record['change']} ga ko‘paytirgan.")
            info += text + "\n"
        return info
    else:
        return "⚠️ Ma'lumot yo'q."

import json

def is_halal(ticker):
    file_path = "ishalal.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        if data:
            stock_info = next((stock for stock in data if stock.get("Ticker") == ticker), None)
            return stock_info.get("Compliance", "") if stock_info else ""
    return ""

