import time
import os
import tempfile
from data import config
from selenium.webdriver.common.by import By
from seleniumbase import Driver
from PIL import Image
from io import BytesIO
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

current_dir = os.getcwd()
files = os.listdir(current_dir)

images = "images"
main_folder = os.path.join(current_dir, images)
if not images in files:
    os.mkdir(main_folder)
print(main_folder)

class Setup:
    def __init__(self, ticker="AAPL"):
        self.ticker = ticker
        self.filepath = f"{main_folder}/{ticker}.png"
        self.driver = None  # Driver-ni faqat init da ishga tushiramiz

    def init(self):
        # Har bir sessiya uchun unik temporary direktoriya
        temp_user_data_dir = tempfile.mkdtemp()
        self.driver = Driver(
            headless=config.production,
            user_data_dir=temp_user_data_dir  # Unik direktoriya qo‘shish
        )
        self.driver.set_page_load_timeout(200)
        self.driver.set_window_size(1200, 800)

    def get_image_url(self):
        return self.filepath

    def check_offer_win(self):
        class_close_but = "tv-dialog__close"
        x_button = self.driver.find_elements(By.CLASS_NAME, class_close_but)
        if x_button:
            print("Class topildi")
            x_button[0].click()
        time.sleep(2)

    def screenshot(self):
        global prices
        ticker = self.ticker
        self.filepath = os.path.join(main_folder, f"{ticker}.png")
        self.driver.get('https://www.tradingview.com/chart/?symbol=' + ticker)
        time.sleep(2)
        self.check_offer_win()

        try:
            price_element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'container-qWcO4bp9')]")
                )
            )
            price = price_element.text.strip()
            lines = price.splitlines()
            if len(lines) == 4:
                main_price = lines[0].replace("price:", "").strip()  # Narx
                currency = lines[1].strip()  # Valyuta
                change_value = lines[2].strip()  # O'zgarish qiymati
                change_percent = lines[3].strip()  # O'zgarish foizi
                prices = f"Price: {main_price} {currency} | Change: {change_value} ({change_percent})"
            else:
                prices = "Narx ma'lumotlari to‘liq emas"
        except Exception as e:
            print(f"Narxni olishda xato: {e}")
            prices = "Narxni olishda xato yuz berdi"

        chart = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[5]")
        screenshot = chart.screenshot_as_png
        image = Image.open(BytesIO(screenshot))
        image.save(self.filepath)

        return self.filepath, prices

    def close_browser(self):
        try:
            if self.driver:
                self.driver.delete_all_cookies()
                self.driver.quit()
        except Exception as e:
            print(f"Driver-ni yopishda xato: {e}")
        finally:
            self.driver = None  # Driver-ni tozalash

# # Misol uchun foydalanish
# if __name__ == "__main__":
#     bot = Setup(ticker="AAPL")
#     bot.init()
#     filepath, price_info = bot.screenshot()
#     print(f"Skrinshot saqlandi: {filepath}")
#     print(f"Narx ma'lumotlari: {price_info}")
#     bot.close_browser()