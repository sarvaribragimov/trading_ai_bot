from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def get_volume():
    driver = webdriver.Chrome()
    driver.get("https://www.barchart.com/stocks/quotes/NVDA/long-options/long-call-options?expiration=2025-02-28-w&orderBy=volume&orderDir=desc")
    wait = WebDriverWait(driver, 10)
    def expand_shadow_element(element):
        return driver.execute_script('return arguments[0].shadowRoot', element)
    grid_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "bc-data-grid")))
    shadow_root = expand_shadow_element(grid_element)
    actions = ActionChains(driver)
    for _ in range(2):
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)
    volume_cells = shadow_root.find_elements(By.CSS_SELECTOR, "div._cell._align_right.volume")
    volume_data = []
    for index, cell in enumerate(volume_cells):
        volume_text = cell.text.replace(',', '')
        if volume_text.isdigit() and int(volume_text) > 3000:
            volume_data.append((index, int(volume_text)))
    volume_data.sort(key=lambda x: x[1], reverse=True)
    top_10_rows = volume_data[:10]
    for row in top_10_rows:
        index, volume = row
        info = f"Qator indeksi: {index}, Volume: {volume}"
        return info
    driver.quit()
