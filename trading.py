# import time
# import os
# from selenium.webdriver.common.by import By
# from seleniumbase import Driver
# from PIL import Image
# from io import BytesIO
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
#
# def get_stock_data(ticker, url, headless=True):
#     """
#     Berilgan `ticker` va `url` bo'yicha aksiyalar narxini olish va skrinshot qilish.
#
#     Params:
#     - ticker (str): Aksiya belgisi (masalan, "AAPL").
#     - url (str): Trading sahifasi URL.
#     - headless (bool): Brauzer oynasiz rejimda ishga tushishi.
#
#     Returns:
#     - (str, str): Skrinshot fayl yo'li va aksiyalar narxi.
#     """
#
#     # Fayl joylashuvi
#     current_dir = os.getcwd()
#     images_dir = os.path.join(current_dir, "images")
#     os.makedirs(images_dir, exist_ok=True)
#     filepath = os.path.join(images_dir, f"{ticker}.png")
#
#     # Selenium driver
#     driver = Driver(headless=headless)
#     driver.set_page_load_timeout(200)
#     driver.set_window_size(1200, 800)
#
#     try:
#         # Sahifani ochish
#         driver.get(url)
#         time.sleep(2)
#
#         # Pop-up yoki taklif oynasi yopilsa
#         close_button_class = "tv-dialog__close"
#         x_button = driver.find_elements(By.CLASS_NAME, close_button_class)
#         if x_button:
#             x_button[0].click()
#         time.sleep(2)
#
#         # Narxni olish
#         try:
#             price_element = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'container-qWcO4bp9')]"))
#             )
#             price = price_element.text.strip()
#             lines = price.splitlines()
#
#             if len(lines) == 4:
#                 main_price = lines[0].replace("price:", "").strip()
#                 currency = lines[1].strip()
#                 change_value = lines[2].strip()
#                 change_percent = lines[3].strip()
#                 prices = f"Price: {main_price} {currency} | Change: {change_value} ({change_percent})"
#             else:
#                 prices = price
#         except Exception:
#             prices = "Narx topilmadi"
#
#         # Grafikdan skrinshot olish
#         chart = driver.find_element(By.XPATH, "/html/body/div[2]/div[5]")
#         screenshot = chart.screenshot_as_png
#         image = Image.open(BytesIO(screenshot))
#         image.save(filepath)
#
#         return filepath, prices
#
#     finally:
#         driver.quit()
# #
#
# # Foydalanish:
# ticker = "AAPL"
# url = f"https://www.tradingview.com/chart/?symbol={ticker}"
# screenshot_path, stock_price = get_stock_data(ticker, url)
# print(f"Skrinshot saqlandi: {screenshot_path}")
# print(f"Aksiya narxi: {stock_price}")
