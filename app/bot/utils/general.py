from aiogram.fsm.context import FSMContext

from bot.states import ChatContext


async def set_state_if_not_exist(state: FSMContext):
    check_state = await state.get_state()
    if not check_state:
        await state.set_state(ChatContext.dialog)