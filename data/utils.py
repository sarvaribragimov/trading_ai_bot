
def insider_text(trans,volume):
    text = ("Insayderlar savdosi: Ushbu malumotlarga asoslanib Insayderlar savdosi haqida fikr bildir, yaqinda sotib chiqib ketgan bolsa bu yomon, "
            "yaqinda sotib olgan ammo, insayder sotib olgan narxida 10% dan ko`p yurvorgan bolsa bu yomon, "
            f"yaqindagini insayderi sotib olgan bolsa $500,000 dan koproq summaga bu ijobiy, agar qancha summa katta bolsa shuncha yaxshi {trans}"
            f"Optionlar qiymati: hafta oxirigacha bolgan optionlar orasidan qaysi narxda eng kop Call option borligini aniqla sababi ,"
            f"eng kop call option bor narxgacha aksiya harakat qiladi  {volume}  (market Value qiymatini Shares held ga bo`lvorsak average price kelib chiqadi . "
            f"Quarterly changes in shares degan joyida qizil minus tursa sotvorgan degani, yashil plus tursa sotib olgan degani."
            f"ATR qiyamti 1 oylik ortacha yurish qiymati 10% ni tashkil qiladi, hozir esa aksiya 5% yurgan, buy yana 5%lik potensial borligini korsatadi")
    return text

def investment_text(insider,invest):
    text = (f"{insider}  investment: {invest} ")
    return text


def alltext(ticker,comp_info,market_value,market_task,insider,invest):
    text = (f"Quyidagi malumotlarni o`rganib chiq va “stock tiker”   kompaniyasi uchun ijobiy yoki salbiy xabar ekanligini aniqla"
            f"kompaniya malumotlari: {market_value} {market_task}"
            f"“Stock tiker”  kompaniyasining so'ngi yangiliklari:{comp_info}"
            f"Insayderlar savdosi:   {insider}"
            f"Instutsional transaction: {invest}"
            f" javobing 600 ta belgidan oshmasin probel qo'yma qisqa va lo'nda")
    return text


import requests


def options_expirations(cookie: str, token: str):
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
        "fields": "expirationDate,expirationType,daysToExpiration,putVolume,callVolume,totalVolume,putCallVolumeRatio,putOpenInterest,callOpenInterest,totalOpenInterest,putCallOpenInterestRatio,averageVolatility,symbolCode,symbolType,lastPrice,dailyLastPrice",
        "symbol": "TSLA",
        "page": 1,
        "limit": 100,
        "orderBy": "putCallVolumeRatio",
        "orderDir": "asc",
        "raw": 1,
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data: {response.status_code}", "details": response.text}