from aiogram.dispatcher.filters.state import State, StatesGroup


class SubscriptionStates(StatesGroup):
    waiting_for_payment = State()
