import asyncio
from pyppeteer import launch
from bot_engine.config import load_config

config=load_config('.env')

async def get_info():
    info: str = "ЖДТ-СЕРВІС"
    browserObj = await launch({"executablePath": '/usr/bin/chromium-browser', "headless": True})
    url = await browserObj.newPage()
    await url.goto("https://ssp-online.okko.ua/login")
    await url.waitFor(10000)

    print("OPEN PAGE")

    await url.type('#mat-input-0', config.fuel_acc.f_login)
    await url.type('#mat-input-1', config.fuel_acc.f_pass)
    await url.waitFor(1000)

    buts = await url.querySelectorAll('ob-card-body button')
    await buts[1].click()

    await url.waitFor(4000)

    cells = await url.querySelectorAll('ob-favorite-contracts mat-cell')
    for cell in cells:
        _str = (await cell.getProperty('textContent')).toString()
        info = info + " -- " + _str.replace('JSHandle:', '')

    await url.waitFor(4000)
    await browserObj.close()
    return info


# response = asyncio.get_event_loop().run_until_complete(main())
# print(response)
