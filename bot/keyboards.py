from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_payment_keyboard(user_id: int):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text="Оплатить через Тинькофф Pay",
        callback_data=f"pay_tinkoff:{user_id}")
    )
    markup.add(InlineKeyboardButton(
        text="Оплатить через Cбер Pay",
        callback_data=f"pay_cber:{user_id}")
    )
    return markup
