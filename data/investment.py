import requests
from bs4 import BeautifulSoup


def invest(ticker):
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
def get_invest(ticker):
    t =  invest(ticker)
    if t:
        info=""
        for i, record in enumerate(t, start=1):
            text = (f"{i}) {record['company']} kompaniyasi {record['date']} sanasida {record['shares']} aksiyaga egalik qiladi,"
                    f"jami {record['market_value']} summa kiritgan. Oxirgi chorakda aksiyalarini sonini {record['change']} ga ko‘paytirgan.")
            info += text + "\n"
        return info
    else:
        return "⚠️ Ma'lumot yo'q."