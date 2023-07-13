from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from tabulate import tabulate

from bot.db import get_statistics
from config import config
from bot.filters import IsAdmin

router: Router = Router()

router.message.filter(IsAdmin(config.tg_bot.admin_ids))


@router.message(Command(commands=['stat']))
async def cmd_start(message: Message):
    statistics = await get_statistics()
    table = tabulate(statistics, headers="firstrow")
    await message.answer(table)
