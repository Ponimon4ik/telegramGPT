from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import LabeledPrice

from bot.db import (check_subscription, create_user,
                    process_successful_payment)
from bot.keyboards import get_payment_keyboard
from bot.states import SubscriptionStates
from bot.utils import gpt_request


async def on_start(message: types.Message):
    user_id = message.from_user.id
    await create_user(user_id)
    await message.reply(
        "Привет! Я бот, использующий ChatGPT 3.5. "
        "У вас есть 3 бесплатных запроса, "
        "после чего вам нужно будет оплатить подписку."
    )


async def on_message(message: types.Message):
    user_id = message.from_user.id
    subscription_status = await check_subscription(user_id)
    if subscription_status:
        response = await gpt_request(message.text)
        await message.reply(response)
    else:
        payment_keyboard = get_payment_keyboard(user_id)
        await message.reply(
            "Пожалуйста, оплатите подписку "
            "для продолжения использования бота.",
            reply_markup=payment_keyboard

        )


async def on_callback_query(
        callback_query: types.CallbackQuery, state: FSMContext,):
    user_id = callback_query.from_user.id
    if callback_query.data.startswith("pay_tinkoff"):
        await SubscriptionStates.waiting_for_payment.set()
        payment_keyboard = get_payment_keyboard(user_id)
        await callback_query.bot.send_invoice(
            chat_id=user_id,
            title="Подписка на бот",
            description="Оплата подписки на 30 дней",
            provider_token="your_tinkoff_payment_provider_token",
            currency="RUB",
            prices=[LabeledPrice(label="Подписка", amount=10000)],
            reply_markup=payment_keyboard,
            payload=f"subscription:{user_id}",
        )
        await callback_query.answer()
    elif callback_query.data.startswith("pay_cber"):
        await SubscriptionStates.waiting_for_payment.set()
        payment_keyboard = get_payment_keyboard(user_id)
        await callback_query.bot.send_invoice(
            chat_id=user_id,
            title="Подписка на бот",
            description="Оплата подписки на 30 дней",
            provider_token="your_ober_payment_provider_token",
            currency="RUB",
            prices=[LabeledPrice(label="Подписка", amount=10000)],
            reply_markup=payment_keyboard,
            payload=f"subscription:{user_id}",
        )
        await callback_query.answer()


async def on_successful_payment(message: types.Message):
    user_id = message.from_user.id
    await process_successful_payment(user_id)
    await message.reply(
        "Оплата успешно проведена. "
        "Теперь вы можете пользоваться ботом в течение 30 дней."
    )


    # Вызов функции для обработки оплаты через Тинькофф
    # await process_payment(user_id, 'tinkoff')

async def process_payment_tinkoff(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await process_successful_payment(user_id)
    await callback_query.message.reply(
        "Оплата успешно проведена. "
        "Теперь вы можете пользоваться ботом в течение 30 дней."
    )


def register_handlers(dp):
    dp.register_message_handler(on_start, Command("start"))
    dp.register_message_handler(
        on_message, content_types=types.ContentTypes.TEXT)
    dp.register_callback_query_handler(
        on_callback_query, state=SubscriptionStates.waiting_for_payment)
    dp.register_message_handler(
        on_successful_payment,
        content_types=types.ContentTypes.SUCCESSFUL_PAYMENT
    )
    dp.register_callback_query_handler(
        process_payment_tinkoff,
        lambda c: c.data.startswith('pay_tinkoff:') or c.data.startswith('pay_obereg:')
    )
