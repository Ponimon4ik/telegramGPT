from aiogram.filters.state import State, StatesGroup


class ChatContext(StatesGroup):
    dialog = State()
