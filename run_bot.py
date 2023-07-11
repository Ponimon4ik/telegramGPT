import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis


from config import config
from bot.handlers import user_handlers
from bot.db import create_table_if_not_exists


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await create_table_if_not_exists()
    redis: Redis = Redis(
        host=config.redis.rd_host,
        password=config.redis.rd_password,
        port=config.redis.rd_port
    )
    bot: Bot = Bot(token=config.tg_bot.token)
    storage: RedisStorage = RedisStorage(redis=redis)
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_router(user_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
