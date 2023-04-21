import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from config import BOT_TOKEN
from bot.middlewares import CounterMiddleware
from bot.handlers import register_handlers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(CounterMiddleware())

register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
