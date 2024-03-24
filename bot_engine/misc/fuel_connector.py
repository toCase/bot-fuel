import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from bot_engine.config import load_config

config=load_config('.env')

def get_info():
    info :str = "INFO MESSAGE"
    options = Options()
    # options.page_load_strategy = 'normal'
    options.add_argument("--headless=new")
    options.add_argument("--incognito")
    options.add_argument("--nogpu")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,1280")
    options.add_argument("--no-sandbox")
    # Запуск браузера в режиме без графического интерфейса
    options.add_argument("--enable-javascript")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument("--disable-gpu")  # Отключение GPU


    service = webdriver.ChromeService(executable_path='/usr/bin/chromedriver')
    chrome = webdriver.Chrome(service=service, options=options)

    # chrome = webdriver.Chrome()
    chrome.get('https://www.okko.ua/fuel-for-business')
    time.sleep(15)
    original_window = chrome.current_window_handle
    print(chrome.page_source)

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
