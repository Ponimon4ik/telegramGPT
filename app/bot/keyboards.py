from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_reset_context_keyboard(text: str):
    reset_context_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text,
                    callback_data='reset_context'
                )
            ],
        ],
    )
    return reset_context_keyboard
