import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from config import BOT_TOKEN
from bot.middlewares import CounterMiddleware
from bot.handlers import register_handlers
from bot.db import create_table_if_not_exists


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(CounterMiddleware())

register_handlers(dp)


async def main():
    await create_table_if_not_exists()
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
