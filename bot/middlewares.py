from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.db import check_subscription, update_requests_count


class CounterMiddleware(BaseMiddleware):

    async def on_pre_process_message(self, message: Message, data: dict):
        user_id = message.from_user.id
        requests_count = await update_requests_count(user_id)
        subscription_status = await check_subscription(user_id)
        if requests_count is None:
            requests_count = 0
        if requests_count > 3 and not subscription_status:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(
                text="Оплатить подписку", callback_data="pay_subscription")
            )
            await message.reply(
                "Вы исчерпали лимит бесплатных запросов. "
                "Оформите подписку за 100 рублей.",
                reply_markup=markup
            )
            return False
