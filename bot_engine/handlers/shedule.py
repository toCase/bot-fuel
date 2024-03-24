from aiogram import Bot
from bot_engine.misc import fuel_connector

from bot_engine.config import load_config
config=load_config('.env')

async def sent_message_cron(bot:Bot):
    message = "Інформація по рахунку ОККО <br> {}".format(fuel_connector.get_info())
    await bot.send_message(config.tg_bot.chat, message)