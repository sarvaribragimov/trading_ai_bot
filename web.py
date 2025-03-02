import time
from data import config
from selenium.webdriver.common.by import By
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class Setup:
    def __init__(self, ticker="AAPL"):
        """
        ticker: Aksiyaning belgisi (masalan, AAPL, TSLA)
        """
        self.ticker = ticker

    def init(self):
        """
        Selenium WebDriver'ni boshlash.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36")

        self.driver = Driver(headless=False, options=chrome_options)
        self.driver.set_page_load_timeout(200)
        self.driver.set_window_size(1200, 800)

    def check_offer_win(self):
        """
        Sahifada reklama oynasi chiqsa, uni yopadi.
        """
        try:
            # Reklama oynasini yopish uchun turli usullar
            class_close_but = "tv-dialog__close"
            x_button = self.driver.find_elements(By.CLASS_NAME, class_close_but)
            if x_button:
                x_button[0].click()
            time.sleep(2)
        except Exception as e:
            print(f"Reklama oynasini yopishda xato: {e}")

    def get_column_inner_data(self):
        """
        column-inner clasidagi barcha HTML tarkibini olish va print qilish.
        """
        ticker = self.ticker
        self.driver.get(f'https://www.barchart.com/stocks/quotes/{ticker}/overview')
        time.sleep(5)  # Qo'shimcha vaqt kutish
        self.check_offer_win()

        try:
            # Elementni kutish va olish
            column_inner_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "column-inner"))
            )
            column_inner_html = column_inner_element.get_attribute("outerHTML")
            return column_inner_html
        except Exception as e:
            print(self.driver.page_source)  # Barcha HTMLni chop etish
            return None

    def close_browser(self):
        """
        Brauzer sessiyasini yopadi.
        """
        self.driver.delete_all_cookies()
        self.driver.quit()


# Foydalanish
if __name__ == "__main__":
    ticker = "AAPL"  # Ticker kodini kerakli aksiya bilan almashtiring
    setup = Setup(ticker)
    setup.init()
    try:
        column_inner_data = setup.get_column_inner_data()  # column-inner ma'lumotini olish
        if column_inner_data:
            print(f"column-inner HTML:\n{column_inner_data}")
        else:
            print("column-inner ma'lumotini olishda xato yuz berdi.")
    finally:
        setup.close_browser()
