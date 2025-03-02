import asyncio

from data.utils import options_expirations
from utils.db_api import database


def alltext(ticker,comp_info,market_value,market_task,insider,invest):
    text = (f"Quyidagi malumotlarni o`rganib chiq va “stock tiker”   kompaniyasi uchun ijobiy yoki salbiy xabar ekanligini aniqla va javobing 800 ta belgidan oshmasin"
            f"kompaniya malumotlari: {market_value} {market_task}\n\n"
            f"“Stock tiker”  kompaniyasining so'ngi yangiliklari:{comp_info}   \n\n"
            f"Insayderlar savdosi:   {insider}\n\n "
            f"Instutsional transaction: {invest}")

    return text


cookie='compass_uid=45eea333-4940-4613-97ed-4c666a3ed2e5; _gcl_au=1.1.190775763.1740041165; _gid=GA1.2.1290139120.1740041166; OptanonAlertBoxClosed=2025-02-20T08:46:33.342Z; gcid_first=86002729-156b-4d00-84dd-5c13ebb4f68f; _cc_id=419d99c5c71bca16eb8d3483b6c94c04; alo_uid=a96a9179-72bc-41f6-a44a-19a628b901ce; _unifiedId_cst=zix7LPQsHA%3D%3D; sharedId=ca93ef15-466b-49fa-b830-dac4a5190b93; _pbjs_userid_consent_data=3524755945110770; _ga_4HQ9CY2XKK=GS1.1.1740225000.1.1.1740226637.60.0.0; _unifiedId=%7B%22TDID%22%3A%22280462b5-a248-43d7-9145-74a4ae5bbaf6%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222025-01-24T09%3A44%3A08%22%7D; cto_bundle=-gMFi19lb2tCQzI3NWR0dllHYVk1eGtWckVnMzJnb1NnS1d3d0NlYjJOSTR0OU5CRDM4OGFUd25iWEFBT2lYTE9xOE9WMktxQ2Fyc3FzYXN3eERTTXp0WWtjR3hzTzhQWUhWRTBTVUM3bHlxZURrTVNnazJYRG5URUtxamVZR3hyYWZYUSUyQlFtRUUlMkZ5aGtodUd3YWlZZjAzTmtEciUyRkVONzhDM043TmhmN1VSR081b2lWeTlkJTJCVE15ZHpocU1xYlpSa3ljVDA5JTJGSTJkakFidWZpbiUyRmdOTk1lZlBGSDdmaGtEVFRGdXZjMW1QQkVoTGRkdzBmQjRudkZ1NG1nQ2NqMTJmdld6bmNzQmhWM1J5bjZIT3VVTGhSUlpWUSUzRCUzRA; cto_bundle=-gMFi19lb2tCQzI3NWR0dllHYVk1eGtWckVnMzJnb1NnS1d3d0NlYjJOSTR0OU5CRDM4OGFUd25iWEFBT2lYTE9xOE9WMktxQ2Fyc3FzYXN3eERTTXp0WWtjR3hzTzhQWUhWRTBTVUM3bHlxZURrTVNnazJYRG5URUtxamVZR3hyYWZYUSUyQlFtRUUlMkZ5aGtodUd3YWlZZjAzTmtEciUyRkVONzhDM043TmhmN1VSR081b2lWeTlkJTJCVE15ZHpocU1xYlpSa3ljVDA5JTJGSTJkakFidWZpbiUyRmdOTk1lZlBGSDdmaGtEVFRGdXZjMW1QQkVoTGRkdzBmQjRudkZ1NG1nQ2NqMTJmdld6bmNzQmhWM1J5bjZIT3VVTGhSUlpWUSUzRCUzRA; sharedId_last=Tue%2C%2025%20Feb%202025%2014%3A29%3A42%20GMT; __gads=ID=c67cabde7c862226:T=1740059000:RT=1740495032:S=ALNI_Ma2o7-m36EtaGyxmuFYZyZ0ybnTaA; __gpi=UID=0000103a8ee604b7:T=1740059000:RT=1740495032:S=ALNI_Mb8ve1ctCWM_-nvYL5Up6zPb0bhpg; __eoi=ID=4703144ae5b69997:T=1740059000:RT=1740495032:S=AA-AfjaH-jXWww8m1Gv_e0qoMeMv; cto_bundle=EIEnGF9lb2tCQzI3NWR0dllHYVk1eGtWckVsTTJvVWtFbFRrSnlTbUZyNVczN3d0c1J5MXM1WkJzM1cza1p4QlloOHRuY2wyOSUyRnFKOWx4UkxYakZiZThFa3F5enFDM2tGZkg4eWhUbUd6M2ZBMXRuS0loQ1AyRUdnNjY2ekJFd2NRVVc4dncwT3JsZlQ5WGtzOG85a0VaM0JzVHg3QlI4WiUyRnhid0R5RzF2c1AycTAlMkIxZ2dIT1VhRmJBTyUyQkJKclFwJTJCdkN5T0RWTGRtTDJvS1pJRjYlMkZOJTJGcmR0MXNGaE9YQW0zRDh0UzRFSGZvUlJtJTJGZno2RGY3aHZMN2p4OURkbzglMkYwRU1MRmQ2cjZGdVV3VVZ3cWRVdTlDQkdKdyUzRCUzRA; panoramaId_expiry=1741253026501; panoramaId=59450acc56918b485d76cf262a4016d539387916d28317836c7f322c480a510e; panoramaIdType=panoIndiv; _awl=2.1740648468.5-50fe523739e3d12e788bfbb4d2d31905-6763652d6575726f70652d7765737431-0; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IklkMGZrY2pQTGJKeWNXUzVaNlZad3c9PSIsInZhbHVlIjoidHY0cDBlVldhaHhOZS9WUjUxQURUKzRLQnF5Yld5OFM1c1dEN2JzUFNqN2ZiL2JPcUxyTUpLekgzM2JQR3o2dUlrZFlyS1oydGhRS2JjWHNEdHlWUjBXSDR1VWZTZzlJZXdvRVlESUxjWnhaMWx1NEg3TVJWWkNwU2l3UndoY2pDeWtFWm44L0QzZmNmYzNlSzlCNEFaNStneUg4anlQQ2U2Q0FmOWFuUXlDM1FyN1I4Y0Z2c0w5V1JFOElxdFFVUXlWQnlQVERvTDZIaU9keGdKZTRVT3ovR1VwTzRzT0ZkV0Nqb1N2NVpuWT0iLCJtYWMiOiIwYTY4YjljOTRkOGM5Zjk1ZGExOWM3NDVkOTk0YWJjZTRiNDFmMzQxNjI1NTI4OGIxOWJiY2NhY2M1NjBkZDQ5IiwidGFnIjoiIn0%3D; market=eyJpdiI6IlVrWTZOSE9NQnpsemlscUlZbEhRUVE9PSIsInZhbHVlIjoiaDV0MGRPZUVpR0RrR0IzcjhwTjE5VitMQm4vWUJyc21udVFRdG15MlM3bW5nVUlqVjVWangzRVhKeS8zOG91biIsIm1hYyI6ImE1ZGE1M2M4NTExZjc0MDI2M2E3YzE2NDc3NTgxNmI2MDhkMTc2Y2M2MWIwZmI4MWI2OWZjZjVlOGQ2YTZiMTgiLCJ0YWciOiIifQ%3D%3D; webinarClosed=234; ic_tagmanager=UAT; ___nrbi=%7B%22firstVisit%22%3A1740041164%2C%22userId%22%3A%2245eea333-4940-4613-97ed-4c666a3ed2e5%22%2C%22userVars%22%3A%5B%5D%2C%22futurePreviousVisit%22%3A1740837251%2C%22timesVisited%22%3A70%7D; _gat_UA-2009749-51=1; _ga=GA1.2.1773291130.1740041166; laravel_token=eyJpdiI6IlBXZDZGRktsZlRhYzMydmZDdVVPblE9PSIsInZhbHVlIjoicEtjcDk2OFZUN3NNQVdnQjVWY2lONjd0RjRjcGJMNHlYM2x2c25wRUt4NU9iVy9HZHc1cEh4THR3Tk5CVFR0dmJpYWlvdkZWNFIwOVhnTDJ2aWpONmpmZ0Q3ajNTQmZTV0xwUGhydjZ4WU5XUHc1c3g5bVIrRXFrZzVMRTlBbng4cmJodWFmRGdHUG1taE5DcFFZZ2RIcW1OQnErRDZjaUcxamd6cGNrQzIyYitqM1BRS2hZSTZlODEyVnQxNEV5WGozNXlCNUdUd2VzcGwvVU5lRmx1UDZMQzNWbVFKTklHVlBuVkNSNGFuZjloMzJUb2VWaXVqRC9IRFBOSjg3RlYzdFBpTStLd2swRXNqVmE3TkFJMktGbkFaV1VyZWFzVDNYZ2xaMFJsemF4S21yUnJJUGUvdm1EZnk3YUpRSGoiLCJtYWMiOiI0ODE1MWUwNTY3Yjc1YmU1NmEwM2NiZjFkZjFhMThjYTdhMDE5MDI2YTYzNWEzNmJiYmEwY2RjZGM0ODUwZjRhIiwidGFnIjoiIn0%3D; XSRF-TOKEN=eyJpdiI6Im85TFJab1QxVzltNG9zb043QzEwOVE9PSIsInZhbHVlIjoiRHVmUUI1TEZHeThtYitIN3gzM0JzV1l6a2ViWkhndUx4c2hzSG1hZlVvU013LzBhbTdnSm1SQkhiL1ZJM2lCKzFNam1ZWk5RV3dKb0Q2c29SUDllV1ZaQmlPUkVQZEFWai9sM3BRUGhISzRmR3BnNTc3N201TnFVY3RqY01rMzAiLCJtYWMiOiI0YjA4OWQ5NzcxYzA4ZTZiOTc1MDg2ZTE1YTI1OTMyOTJiNmU2NjAyYzRlYWIwYTkxNzBlMzYzMWYyNjI3MjJhIiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6Ijc1NXBsTEcreE1jSHdML0dkRS9aeFE9PSIsInZhbHVlIjoiOVRtREtPUXVUUVAraVlRZG1JT0cvZ2R4U3JJM1MzdDdMQWpwNnR0Z0lpMlBmazB2LzY2dlJiNWZNY2NpS2JjZ0NnKzdJYWpIeWYzdUpoRjcrTThabzBkeGR0bkZkekVqT3JmUE4vQVpqZ0RqZkE1akNSaDJTNDVtdDlheHovcE8iLCJtYWMiOiJkMzA5OWY2ZTFjMTg2ZWEwNGI3YjUxYWU1ZTdkMThjM2U0YjI2MmJjOTNhNWViNGYyNDkwZjYyNjZmNjc3MDU4IiwidGFnIjoiIn0%3D; _ga_PE0FK9V6VN=GS1.1.1740817672.17.1.1740837419.12.0.0; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Mar+01+2025+18%3A56%3A59+GMT%2B0500+(Uzbekistan+Standard+Time)&version=202501.2.0&browserGpcFlag=0&isIABGlobal=false&consentId=e854d8d6-90ac-4660-b084-62a144f89f5c&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0004%3A1%2CC0003%3A1%2CC0002%3A1&hosts=H309%3A1%2CH2%3A1%2CH353%3A1%2CH330%3A1%2CH4%3A1%2CH7%3A1%2CH9%3A1%2CH12%3A1%2CH331%3A1%2CH13%3A1%2CH14%3A1%2CH15%3A1%2CH17%3A1%2CH235%3A1%2CH19%3A1%2CH236%3A1%2CH237%3A1%2CH238%3A1%2CH26%3A1%2CH321%3A1%2CH239%3A1%2CH240%3A1%2CH27%3A1%2CH29%3A1%2CH30%3A1%2CH31%3A1%2CH32%3A1%2CH366%3A1%2CH35%3A1%2CH36%3A1%2CH242%3A1%2CH367%3A1%2CH243%3A1%2CH38%3A1%2CH244%3A1%2CH245%3A1%2CH246%3A1%2CH39%3A1%2CH40%3A1%2CH247%3A1%2CH41%3A1%2CH248%3A1%2CH43%3A1%2CH356%3A1%2CH312%3A1%2CH45%3A1%2CH46%3A1%2CH334%3A1%2CH47%3A1%2CH53%3A1%2CH54%3A1%2CH368%3A1%2CH57%3A1%2CH249%3A1%2CH250%3A1%2CH369%3A1%2CH60%3A1%2CH251%3A1%2CH61%3A1%2CH62%3A1%2CH63%3A1%2CH66%3A1%2CH253%3A1%2CH254%3A1%2CH69%3A1%2CH71%3A1%2CH72%3A1%2CH255%3A1%2CH357%3A1%2CH256%3A1%2CH370%3A1%2CH257%3A1%2CH231%3A1%2CH76%3A1%2CH81%3A1%2CH82%3A1%2CH258%3A1%2CH337%3A1%2CH259%3A1%2CH86%3A1%2CH338%3A1%2CH88%3A1%2CH261%3A1%2CH89%3A1%2CH262%3A1%2CH93%3A1%2CH94%3A1%2CH95%3A1%2CH340%3A1%2CH96%3A1%2CH265%3A1%2CH98%3A1%2CH266%3A1%2CH267%3A1%2CH101%3A1%2CH268%3A1%2CH269%3A1%2CH102%3A1%2CH326%3A1%2CH103%3A1%2CH106%3A1%2CH108%3A1%2CH109%3A1%2CH111%3A1%2CH270%3A1%2CH112%3A1%2CH271%3A1%2CH114%3A1%2CH116%3A1%2CH118%3A1%2CH358%3A1%2CH342%3A1%2CH121%3A1%2CH122%3A1%2CH274%3A1%2CH275%3A1%2CH125%3A1%2CH371%3A1%2CH126%3A1%2CH276%3A1%2CH359%3A1%2CH360%3A1%2CH129%3A1%2CH314%3A1%2CH130%3A1%2CH131%3A1%2CH278%3A1%2CH344%3A1%2CH279%3A1%2CH132%3A1%2CH135%3A1%2CH137%3A1%2CH280%3A1%2CH282%3A1%2CH361%3A1%2CH139%3A1%2CH140%3A1%2CH283%3A1%2CH142%3A1%2CH284%3A1%2CH143%3A1%2CH144%3A1%2CH146%3A1%2CH147%3A1%2CH285%3A1%2CH151%3A1%2CH372%3A1%2CH286%3A1%2CH153%3A1%2CH317%3A1%2CH157%3A1%2CH288%3A1%2CH233%3A1%2CH167%3A1%2CH168%3A1%2CH347%3A1%2CH289%3A1%2CH170%3A1%2CH171%3A1%2CH172%3A1%2CH364%3A1%2CH173%3A1%2CH174%3A1%2CH177%3A1%2CH291%3A1%2CH180%3A1%2CH292%3A1%2CH348%3A1%2CH228%3A1%2CH182%3A1%2CH183%3A1%2CH184%3A1%2CH293%3A1%2CH186%3A1%2CH187%3A1%2CH365%3A1%2CH294%3A1%2CH188%3A1%2CH295%3A1%2CH296%3A1%2CH349%3A1%2CH194%3A1%2CH297%3A1%2CH195%3A1%2CH298%3A1%2CH198%3A1%2CH199%3A1%2CH299%3A1%2CH350%3A1%2CH300%3A1%2CH202%3A1%2CH301%3A1%2CH205%3A1%2CH206%3A1%2CH302%3A1%2CH303%3A1%2CH304%3A1%2CH209%3A1%2CH210%3A1%2CH211%3A1%2CH212%3A1%2CH305%3A1%2CH214%3A1%2CH306%3A1%2CH373%3A1%2CH216%3A1%2CH307%3A1%2CH217%3A1%2CH308%3A1%2CH218%3A1%2CH352%3A1%2CH320%3A1%2CH241%3A1%2CH272%3A1&genVendors=&intType=3&geolocation=UZ%3BTK&AwaitingReconsent=false; ___nrbic=%7B%22previousVisit%22%3A1740833997%2C%22currentVisitStarted%22%3A1740837251%2C%22sessionId%22%3A%22f7991971-4d44-4a4e-9867-b290c46733bb%22%2C%22sessionVars%22%3A%5B%5D%2C%22visitedInThisSession%22%3Atrue%2C%22pagesViewed%22%3A4%2C%22landingPage%22%3A%22https%3A//www.barchart.com/stocks/quotes/NVDA/overview%22%2C%22referrer%22%3A%22%22%2C%22lpti%22%3Anull%7D'
token ="eyJpdiI6Im85TFJab1QxVzltNG9zb043QzEwOVE9PSIsInZhbHVlIjoiRHVmUUI1TEZHeThtYitIN3gzM0JzV1l6a2ViWkhndUx4c2hzSG1hZlVvU013LzBhbTdnSm1SQkhiL1ZJM2lCKzFNam1ZWk5RV3dKb0Q2c29SUDllV1ZaQmlPUkVQZEFWai9sM3BRUGhISzRmR3BnNTc3N201TnFVY3RqY01rMzAiLCJtYWMiOiI0YjA4OWQ5NzcxYzA4ZTZiOTc1MDg2ZTE1YTI1OTMyOTJiNmU2NjAyYzRlYWIwYTkxNzBlMzYzMWYyNjI3MjJhIiwidGFnIjoiIn0="

async def getapi():
    db = database.BarchartTokenTable()
    data =  await db.search_by_status(status='ACTIVE')
    print(data['status'])
    s=options_expirations(data['cookie'], data['token'])
    print(s)

# asyncio.run(getapi())



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Browser uchun options
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": os.getcwd(),  # Joriy papkaga yuklab olish
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Chrome WebDriver ishga tushirish
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Saytni ochish
url = "https://www.barchart.com/stocks/quotes/AMD/long-options/long-call-options?orderBy=volume&orderDir=desc&expiration=2025-03-07-w"
driver.get(url)
time.sleep(5)  # Sahifaning yuklanishini kutish

# Download tugmasini topish
try:
    download_button = driver.find_element(By.CLASS_NAME, "bc-glyph-download")
    ActionChains(driver).move_to_element(download_button).click().perform()
    print("Downloading...")
    time.sleep(10)  # Fayl yuklanishini kutish
except Exception as e:
    print("Download tugmasi topilmadi:", e)

# Brauzerni yopish
driver.quit()
