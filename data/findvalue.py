import json
import re

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




