from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

# Chrome brauzer uchun sozlamalar
chrome_options = Options()
chrome_options.add_argument("--headless")  # Brauzerni ko'rsatmaslik uchun

# Chrome driver ishga tushiriladi
service = Service("chromedriver")  # `chromedriver` yo'lini ko'rsating
driver = webdriver.Chrome(service=service, options=chrome_options)

# Saytga kirish
url = "https://www.barchart.com"
driver.get(url)

# 🟢 `localStorage` ma'lumotlarini olish
local_storage_data = driver.execute_script("return JSON.stringify(localStorage);")
local_storage = json.loads(local_storage_data)
print("🔹 Local Storage:", local_storage)

# 🔵 `sessionStorage` ma'lumotlarini olish
session_storage_data = driver.execute_script("return JSON.stringify(sessionStorage);")
session_storage = json.loads(session_storage_data)
print("🔹 Session Storage:", session_storage)

# 🟡 Cookies ma’lumotlarini olish
cookies = driver.get_cookies()
print("🔹 Cookies:", cookies)

# Brauzerni yopish
driver.quit()
