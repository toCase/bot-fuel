import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot_engine.config import load_config
from bot_engine.handlers import handler, shedule

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

logger = logging.Logger

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    config = load_config(".env")

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher()

    scheduler = AsyncIOScheduler(timezone="Europe/Kiev")
    # scheduler.add_job(shedule.sent_message_cron, trigger='time', run_date=datetime.now() + timedelta(seconds=10), kwargs={'bot':bot})
    scheduler.add_job(shedule.sent_message_cron,
                      trigger='cron',
                      hour=8,
                      minute=30,
                      start_date=datetime.now(),
                      kwargs={'bot':bot})
    scheduler.add_job(shedule.sent_message_cron,
                      trigger='cron',
                      hour=17,
                      minute=00,
                      start_date=datetime.now(),
                      kwargs={'bot': bot})
    scheduler.start()
    # register_handlers(dp)

    dp.include_router(handler.router)
    # dp.include_router(handler_meet.router)
    # dp.include_router(handler_reg.router)
    # dp.include_router(handler_del.router)



    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        # await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':

    try:
        asyncio.run(main())

    except(KeyboardInterrupt, SystemExit):
        logger.error("!!!---Bot down---!!!")
