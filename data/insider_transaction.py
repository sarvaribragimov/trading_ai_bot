import requests
from bs4 import BeautifulSoup

from datetime import datetime, timedelta

def insider_ransaction(ticker):
    url = "http://openinsider.com/search?q=AMD"
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