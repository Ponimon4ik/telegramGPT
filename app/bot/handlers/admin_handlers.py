from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from tabulate import tabulate

from bot.db import get_statistics
from config import config
from bot.filters import IsAdmin
from bot.utils.gpt import no_quota_keys

router: Router = Router()

router.message.filter(IsAdmin(config.tg_bot.admin_ids))


@router.message(Command(commands=['stat']))
async def cmd_start(message: Message):
    statistics = await get_statistics()
    table = tabulate(statistics, headers="firstrow")
    await message.answer(table)


@router.message(Command(commands=['keys']))
async def cmd_keys(message: Message):
    await message.answer(tabulate(no_quota_keys))
