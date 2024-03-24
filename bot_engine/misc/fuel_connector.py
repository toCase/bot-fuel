import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from bot_engine.config import load_config

config=load_config('.env')

def get_info():
    info :str = ""
    # options = Options()
    # options.add_argument("--headless")
    # chrome_driver_path = "/usr/lib/chromium-browser/chromedriver"
    #
    # chrome = webdriver.Chrome(service=chrome_driver_path, options=options)
    chrome = webdriver.Chrome()
    chrome.get('https://www.okko.ua/fuel-for-business')
    time.sleep(10)
    original_window = chrome.current_window_handle

    try:
        chrome.find_element(By.PARTIAL_LINK_TEXT, 'ВХІД В КАБІНЕТ').click()
        time.sleep(7)
        print("OPEN LOGIN")

        try:
            for window_handle in chrome.window_handles:
                if window_handle != original_window:
                    chrome.switch_to.window(window_handle)
                    break

            print("title:", chrome.title)
            chrome.find_element(By.ID, 'mat-input-0').send_keys(config.fuel_acc.f_login)
            chrome.find_element(By.ID, 'mat-input-1').send_keys(config.fuel_acc.f_pass)
            time.sleep(5)

            original_window = chrome.current_window_handle
            buttons = chrome.find_elements(By.TAG_NAME, 'button')

            for button in buttons:
                if button.text == 'Увійти':
                    button.click()

            time.sleep(7)
            print("LOGIN OK")

            try:
                if original_window == chrome.current_window_handle:
                    print("WINDOW OK")
                    element = chrome.find_element(By.TAG_NAME, 'ob-favorite-contracts')
                    table = element.find_element(By.TAG_NAME, 'mat-table')
                    rows = table.find_elements(By.TAG_NAME, 'mat-row')
                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, 'mat-cell')
                        for cell in cells:
                            info = info + "  --  " + cell.text
                else:
                    info = "ERROR: WINDOW CHANGE AGAIN"
            except:
                info = "ERROR: APP"
        except:
            info = "ERROR: LOGIN PAGE"
    except:
        info = "ERROR: OPEN OKKO WEB"

    chrome.quit()
    return info