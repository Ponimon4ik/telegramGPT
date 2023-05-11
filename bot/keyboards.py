from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

reset_context_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🧹Сбросить контекст диалога",
                callback_data='reset_context'
            )
        ],
    ],
)
