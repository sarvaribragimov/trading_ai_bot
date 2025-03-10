from utils.db_api import database


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
    text = (f"kompaniya malumotlari: {market_value} {market_task}"
            f"Quyidagi yangiliklarni o`rganib chiq va ular orasidan  kompaniya uchun  ijobiy✅ yoki salbiy🚫"
            f" asos ekanligini xulosa chiqar. Javobni quyidagi korinishda taqdim qil: 2.	Yangiliklari🚫"
            f"•	Taiwan Semiconductor, Apple, Nvidia va AMD’ning kengayish rejalari — ✅ Ijobiy"
            f"•	AQSh fond bozori Trampning tariflari sababli tushib ketdi — 🚫 Salbiy"
            f"•	AQShning Kanada, Meksika va Xitoyga tariflari kuchga kirishi — 🚫 Salbiy"
            f" so'ngi yangiliklar :{comp_info}"
            f"Insayderlar savdosi:   {insider}"
            f"Intutsional transaction ichidan aksiyalar sonini  ijobiy  va salbiyga kopaytirgan kompaniyalar  umumiy summasini har biri uchun alohida aniqla va  eng katta  summa ijobiyga yoki salbiyga kopayganligini aniqla. N/A bolganlarni hiisobdan chiqar. Ushbu savdolar umumiy qiymatidan kelib chiqib  ijobiy✅ yoki salbiy🚫 asos ekanligini xulosa chiqar."
            f" Javobni quyidagi korinishda taqdim qil:3.	Instutsinal investorlar savdosi✅ Savdoga kirgan: $693.10M Sovdodan chiqqan: $296.52M Eng katta o‘zgarish: "
            f"Ijobiy tarafda — Employees Retirement System of Texas $536.62M . Instutsional transaction:{invest}"
            f" javobing 600 ta belgidan oshmasin probel qo'yma qisqa va lo'nda\n ")
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
            cookie = data['cookie'] + data['cookie2']
            result_text = ""
            longputvolume = long_put_volume(ticker, cookie, data['token'])
            if '401' not in longputvolume:
                result_text += (f"\n Quyidagi option malumotlariga asoslanib  optionlar soni va narxini xisoblab eng kop summa kiritilgan  2ta put va 2ta call option uchun strike narxlarini aniqla va  yaxshi holatda aynan qaysi narxgacha kotarilishi mumkin yoki yomon  holatda aynan qaysi narxgacha tushib ketishi mumkin.  Put/call  nisbatini va sonini yaxlitlab solishtir va 0.5dan kichik qiymati biz uchun yaxshi ekanligini hisobga ol.  ijobiy✅  yoki salbiy🚫 asos ekanligini xulosa chiqar va "
                                f"Javobni quyidagi korinishda taqdim qil: 📉 Long Put Volume: 5.	Option xulosa: 🚫 narx yomon holatda 03/07gacha $115gacha tushib ketishi Yaxshi holatda $120ga ko`tarilib berishi mumkin "
                                f"Put narx tushishiga: •	$115.00 strike: $445 × 123,217 = $54,931,565 🛑 ENG KATTA PUT •	$120.00 strike: $765 × 63,336 = $48,455,040 Call narx ko‘tarilishiga:"
                                f"•	$120.00 strike: $163 × 148,242 = $24,156,446 🟢 ENG KATTA CALL •	$125.00 strike: $69 × 121,363 = $8,373,047 "
                                f"Put/Call ratio: 1M put/1,4M call, 0.74 (0.5 dan katta) \n{long_put_volume_text(longputvolume)}\n")
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
            return result_text.strip()  # Qaytariladigan natijani tozalash
    except Exception as e:
        print('barchart table info error',e)