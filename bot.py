import os
import asyncio
import logging

from dotenv import load_dotenv

from aiogram import Dispatcher, Router, Bot
from aiogram.client.default import DefaultBotProperties

from handlers import client


load_dotenv()
router = Router()

async def main():
    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(bot=bot)

    dp.include_routers(
        client.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:

        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")