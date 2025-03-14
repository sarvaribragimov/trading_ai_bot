# from selenium import webdriver
# from selenium.webdriver import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
#
#
# def transaction(ticker):
#     chrome_options = Options()
#     chrome_options.add_argument('--ignore-certificate-errors')
#     chrome_options.add_argument('--ignore-ssl-errors')
#     driver = webdriver.Chrome(options=chrome_options)
#     url = f"https://www.barchart.com/stocks/quotes/{ticker}/insider-trades"
#     driver.get(url)
#     wait = WebDriverWait(driver, 10)
#     def expand_shadow_element(element):
#         return driver.execute_script('return arguments[0].shadowRoot', element)
#     try:
#         grid_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "bc-data-grid")))
#         shadow_root = expand_shadow_element(grid_element)
#         reported_price_element = shadow_root.find_element(By.CSS_SELECTOR, "text-binding[binding='this.reportedPrice']")
#         usd_value_element = shadow_root.find_element(By.CSS_SELECTOR, "text-binding[binding='this.usdValue']")
#         transaction_type_element = shadow_root.find_element(By.CSS_SELECTOR,
#                                                             "text-binding[binding='this.transactionType']")
#         date_element = shadow_root.find_element(By.CSS_SELECTOR, "text-binding[binding='this.transactionDate']")
#         transaction_date = date_element.text.strip()
#         reported_price = reported_price_element.text.strip()
#         usd_value = usd_value_element.text.strip()
#         transaction_type = transaction_type_element.text.strip()
#         info = f"Transaction Type: {transaction_type},Transaction date:{transaction_date} Price: {reported_price}, Trans total: {usd_value}"
#         return info
#     except Exception as e:
#         text = (
#             f"❌ malumot topolmadm: o'zing https://www.barchart.com/stocks/quotes/NVDA/insider-trades "
#             f" haqida malumotni tahlil qil Insider Transactions{a} ")
#         return text
#     finally:
#         driver.quit()
#
#
#
#
#
#
#
# def transaction(ticker):
#     driver = webdriver.Chrome()
#     url = f"https://www.barchart.com/stocks/quotes/{ticker}/insider-trades"
#     driver.get(url)
#     wait = WebDriverWait(driver, 10)
#
#     def expand_shadow_element(element):
#         return driver.execute_script('return arguments[0].shadowRoot', element)
#
#     try:
#         grid_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "bc-data-grid")))
#         shadow_root = expand_shadow_element(grid_element)
#         reported_price_element = shadow_root.find_element(By.CSS_SELECTOR, "text-binding[binding='this.reportedPrice']")
#         usd_value_element = shadow_root.find_element(By.CSS_SELECTOR, "text-binding[binding='this.usdValue']")
#         transaction_type_element = shadow_root.find_element(By.CSS_SELECTOR,
#                                                             "text-binding[binding='this.transactionType']")
#         reported_price = reported_price_element.text.strip()
#         usd_value = usd_value_element.text.strip()
#         transaction_type = transaction_type_element.text.strip()
#         info = f"Transaction Type: {transaction_type} price: {reported_price} Trans total: {usd_value} "
#         print(info)
#         return info
#     except Exception as e:
#         print(f"❌ Xatolik yuz berdi: {e}")
#     finally:
#         driver.quit()
#
#
# def total_percent(ticker):
#     options = webdriver.ChromeOptions()
#     options.add_argument("--start-maximized")
#     driver = webdriver.Chrome(options=options)
#     url = f"https://www.barchart.com/stocks/quotes/{ticker}/seasonality-chart"
#     driver.get(url)
#     wait = WebDriverWait(driver, 10)
#     try:
#         table_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.bc-table-scrollable-inner")))
#         header_row = table_element.find_element(By.CSS_SELECTOR, "tr.header-border-bottom")
#         months = [th.text.strip() for th in header_row.find_elements(By.CSS_SELECTOR, "th") if th.text.strip()]
#         rows = table_element.find_elements(By.CSS_SELECTOR, "tr")
#         table_data = []
#         for row in rows:
#             cells = row.find_elements(By.CSS_SELECTOR, "td")
#             row_data = [cell.text.strip() for cell in cells]
#             if row_data:
#                 table_data.append(row_data)
#         print("\n📌 **Oylik nomlar:**")
#         print(["Year"] + months)
#         print("\n📊 **Jadval ma’lumotlari:**")
#         for row in table_data:
#             print(row)
#     except Exception as e:
#         print(f"❌ Xatolik yuz berdi: {e}")
#     finally:
#         driver.quit()
#
#
# def get_volume(ticker):
#     chrome_options = Options()
#     chrome_options.add_argument('--ignore-certificate-errors')  # SSL xatolarini e'tiborsiz qoldirish
#     chrome_options.add_argument('--ignore-ssl-errors')  # SSL xatolarini e'tiborsiz qoldirish
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.get(
#         f"https://www.barchart.com/stocks/quotes/{ticker}/long-options/long-call-options?expiration=2025-02-28-w&orderBy=volume&orderDir=desc")
#     wait = WebDriverWait(driver, 10)
#
#     def expand_shadow_element(element):
#         return driver.execute_script('return arguments[0].shadowRoot', element)
#
#
#     try:
#         close_ad_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close-ad")))
#         close_ad_button.click()
#         print("Reklama yopildi.")
#     except Exception as e:
#         print("Reklama topilmadi yoki yopib bo'lmadi:")
#
#     grid_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "bc-data-grid")))
#     shadow_root = expand_shadow_element(grid_element)
#     print(shadow_root)
#     actions = ActionChains(driver)
#     for _ in range(2):
#         actions.send_keys(Keys.PAGE_DOWN).perform()
#         time.sleep(1)
#     volume_cells = shadow_root.find_elements(By.CSS_SELECTOR, "div._cell._align_right.volume")
#     print(volume_cells)
#     volume_data = []
#     for index, cell in enumerate(volume_cells):
#         volume_text = cell.text.replace(',', '')
#         if volume_text.isdigit() and int(volume_text) > 3000:
#             volume_data.append((index, int(volume_text)))
#     volume_data.sort(key=lambda x: x[1], reverse=True)
#     top_10_rows = volume_data[:10]
#     print(top_10_rows)
#     for row in top_10_rows:
#         index, volume = row
#         info = f"Qator indeksi: {index}, Volume: {volume}"
#         print(info)
#         return info
#     driver.quit()
#
#
# import requests
# from bs4 import BeautifulSoup
#
#
# def get(ticker):
#     url = f"https://www.marketbeat.com/stocks/NASDAQ/{ticker}/institutional-ownership/"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36"
#     }
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         print("❌ Saytdan ma'lumot olishda xatolik yuz berdi.")
#         return None
#     soup = BeautifulSoup(response.text, "html.parser")
#     table = soup.find("table")
#     if not table:
#         print("❌ Jadval topilmadi.")
#         return None
#
#     thead = table.find("thead")
#     if not thead:
#         print("❌ Jadval ichida <thead> topilmadi.")
#         return None
#     original_headers = [th.get_text(strip=True) for th in thead.find_all("th")]
#
#     try:
#         market_value_index = original_headers.index("Market Value")
#         date_index = original_headers.index("Reporting Date")
#         company_index = original_headers.index("Major Shareholder Name")
#         shares_index = original_headers.index("Shares Held")
#         change_index = original_headers.index("Quarterly Change in Shares")
#     except ValueError:
#         print("❌ Kerakli ustun topilmadi.")
#         return None
#
#     # Jadval ichidagi ma'lumotlarni olish
#     tbody = table.find("tbody")
#     if not tbody:
#         print("❌ Jadval ichida <tbody> topilmadi.")
#         return None
#     rows = tbody.find_all("tr")
#
#     # Natijalarni saqlash
#     filtered_data = []
#
#     for row in rows:
#         cols = row.find_all("td")
#         cols = [col.get_text(strip=True) for col in cols]
#
#         if len(cols) == len(original_headers):  # Ustunlar soni to‘g‘ri bo‘lishi kerak
#             market_value_str = cols[market_value_index]
#
#             # "$1.38M" formatidagi qiymatni son ko‘rinishiga o‘tkazamiz
#             if market_value_str.startswith("$"):
#                 value = market_value_str[1:-1]  # "$" belgisi va oxirgi harfni olib tashlaymiz
#                 multiplier = market_value_str[-1]  # "M" yoki "B" ni olish
#                 try:
#                     numeric_value = float(value) * (1e6 if multiplier == "M" else 1e9 if multiplier == "B" else 1)
#
#                     # Agar qiymat 100M dan katta bo‘lsa, natijalarga qo‘shamiz
#                     if numeric_value > 100e6:
#                         filtered_data.append({
#                             "date": cols[date_index],
#                             "company": cols[company_index],
#                             "shares": cols[shares_index],
#                             "market_value": market_value_str,
#                             "change": cols[change_index]
#                         })
#                 except ValueError:
#                     continue  # Agar raqamga o‘tkazib bo‘lmasa, o‘tkazib yuboramiz
#     return filtered_data
# t = get("NVDA")
#
# if t:
#     for i, record in enumerate(t, start=1):
#         print(
#             f"{i}) {record['company']} kompaniyasi {record['date']} sanasida {record['shares']} aksiyaga egalik qiladi, jami {record['market_value']} summa kiritgan. Oxirgi chorakda aksiyalarini sonini {record['change']} ga ko‘paytirgan.")
# else:
#     print("⚠️ Ma'lumot yo'q.")

# def get_volume():
#     driver = webdriver.Chrome()
#     driver.get("https://www.barchart.com/stocks/quotes/NVDA/long-options/long-call-options?expiration=2025-02-28-w&orderBy=volume&orderDir=desc")
#     wait = WebDriverWait(driver, 10)
#     def expand_shadow_element(element):
#         return driver.execute_script('return arguments[0].shadowRoot', element)
#     grid_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "bc-data-grid")))
#     shadow_root = expand_shadow_element(grid_element)
#     actions = ActionChains(driver)
#     for _ in range(2):
#         actions.send_keys(Keys.PAGE_DOWN).perform()
#         time.sleep(1)
#     volume_cells = shadow_root.find_elements(By.CSS_SELECTOR, "div._cell._align_right.volume")
#     volume_data = []
#     for index, cell in enumerate(volume_cells):
#         volume_text = cell.text.replace(',', '')
#         if volume_text.isdigit() and int(volume_text) > 3000:
#             volume_data.append((index, int(volume_text)))
#     volume_data.sort(key=lambda x: x[1], reverse=True)
#     top_10_rows = volume_data[:10]
#     for row in top_10_rows:
#         index, volume = row
#         info = f"Qator indeksi: {index}, Volume: {volume}"
#         return info
#     driver.quit()
